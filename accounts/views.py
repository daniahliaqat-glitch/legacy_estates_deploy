from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from .models import Agent
from .forms import PropertyForm, PropertyImageForm
from properties.models import Property


def agent_login(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('accounts:dashboard')
        messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')


def agent_logout(request):
    logout(request)
    messages.success(request, "You've been logged out.")
    return redirect('properties:home')


def agent_list(request):
    agents = Agent.objects.filter(is_active_agent=True).select_related('user')
    return render(request, 'accounts/agent_list.html', {'agents': agents})


def agent_detail(request, pk):
    agent = get_object_or_404(Agent.objects.select_related('user'), pk=pk, is_active_agent=True)
    listings = (
        Property.objects.filter(agent=agent, status='available')
        .prefetch_related('images')
        .order_by('-created_at')
    )
    return render(request, 'accounts/agent_detail.html', {'agent': agent, 'listings': listings})


@login_required
def dashboard(request):
    """Agent/staff dashboard: shows their own listings + quick stats.
    Superusers/staff without an Agent profile see all properties."""
    try:
        agent = request.user.agent_profile
        listings = Property.objects.filter(agent=agent).prefetch_related('images')
    except Agent.DoesNotExist:
        agent = None
        if request.user.is_staff:
            listings = Property.objects.all().prefetch_related('images')
        else:
            listings = Property.objects.none()

    listings = listings.order_by('-created_at')
    paginator = Paginator(listings, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    stats = {
        'total': listings.count(),
        'available': listings.filter(status='available').count(),
        'pending': listings.filter(status='pending').count(),
        'sold_or_rented': listings.filter(status__in=['sold', 'rented']).count(),
    }

    context = {'agent': agent, 'page_obj': page_obj, 'stats': stats}
    return render(request, 'accounts/dashboard.html', context)


@login_required
def property_create(request):
    try:
        agent = request.user.agent_profile
    except Agent.DoesNotExist:
        agent = None
        if not request.user.is_staff:
            messages.error(request, 'Only agents or staff can add listings.')
            return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = PropertyForm(request.POST)
        image_form = PropertyImageForm(request.POST, request.FILES)
        if form.is_valid():
            prop = form.save(commit=False)
            prop.agent = agent
            prop.save()
            form.save_m2m()

            if request.FILES.get('image'):
                if image_form.is_valid():
                    img = image_form.save(commit=False)
                    img.property = prop
                    img.is_primary = True
                    img.save()

            messages.success(request, f'"{prop.title}" was created successfully.')
            return redirect('accounts:dashboard')
    else:
        form = PropertyForm()
        image_form = PropertyImageForm()

    return render(request, 'accounts/property_form.html', {
        'form': form, 'image_form': image_form, 'is_edit': False,
    })


@login_required
def property_edit(request, pk):
    prop = get_object_or_404(Property, pk=pk)

    # Permission check: only the assigned agent or staff can edit
    try:
        agent = request.user.agent_profile
    except Agent.DoesNotExist:
        agent = None

    if not request.user.is_staff and prop.agent_id != getattr(agent, 'pk', None):
        messages.error(request, "You don't have permission to edit this listing.")
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=prop)
        image_form = PropertyImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            if request.FILES.get('image') and image_form.is_valid():
                img = image_form.save(commit=False)
                img.property = prop
                img.save()
            messages.success(request, f'"{prop.title}" was updated.')
            return redirect('accounts:dashboard')
    else:
        form = PropertyForm(instance=prop)
        image_form = PropertyImageForm()

    return render(request, 'accounts/property_form.html', {
        'form': form, 'image_form': image_form, 'is_edit': True, 'property': prop,
    })


@login_required
def property_delete(request, pk):
    prop = get_object_or_404(Property, pk=pk)

    try:
        agent = request.user.agent_profile
    except Agent.DoesNotExist:
        agent = None

    if not request.user.is_staff and prop.agent_id != getattr(agent, 'pk', None):
        messages.error(request, "You don't have permission to delete this listing.")
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        title = prop.title
        prop.delete()
        messages.success(request, f'"{title}" was deleted.')
        return redirect('accounts:dashboard')

    return render(request, 'accounts/property_confirm_delete.html', {'property': prop})
