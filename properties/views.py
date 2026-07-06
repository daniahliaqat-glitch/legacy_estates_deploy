from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator

from .models import Property, PropertyType, ListingType, PropertyFeature
from accounts.models import Agent
from inquiries.forms import InquiryForm


def home(request):
    featured = (
        Property.objects.filter(is_featured=True, status='available')
        .select_related('agent', 'agent__user')
        .prefetch_related('images')[:6]
    )
    recent = (
        Property.objects.filter(status='available')
        .select_related('agent', 'agent__user')
        .prefetch_related('images')[:8]
    )
    top_agents = Agent.objects.filter(is_active_agent=True)[:4]

    context = {
        'featured_properties': featured,
        'recent_properties': recent,
        'top_agents': top_agents,
        'property_types': PropertyType.choices,
        'listing_types': ListingType.choices,
    }
    return render(request, 'properties/home.html', context)


def property_list(request):
    qs = (
        Property.objects.filter(status='available')
        .select_related('agent', 'agent__user')
        .prefetch_related('images')
    )

    # --- Search & filters ---
    q = request.GET.get('q', '').strip()
    if q:
        qs = qs.filter(
            Q(title__icontains=q) | Q(city__icontains=q) |
            Q(address_line__icontains=q) | Q(zip_code__icontains=q)
        )

    listing_type = request.GET.get('listing_type', '')
    if listing_type in ListingType.values:
        qs = qs.filter(listing_type=listing_type)

    property_type = request.GET.get('property_type', '')
    if property_type in PropertyType.values:
        qs = qs.filter(property_type=property_type)

    min_price = request.GET.get('min_price', '')
    if min_price.isdigit():
        qs = qs.filter(price__gte=int(min_price))

    max_price = request.GET.get('max_price', '')
    if max_price.isdigit():
        qs = qs.filter(price__lte=int(max_price))

    bedrooms = request.GET.get('bedrooms', '')
    if bedrooms.isdigit():
        qs = qs.filter(bedrooms__gte=int(bedrooms))

    city = request.GET.get('city', '').strip()
    if city:
        qs = qs.filter(city__icontains=city)

    # --- Sorting ---
    sort = request.GET.get('sort', '-created_at')
    valid_sorts = {'-created_at', 'price', '-price', 'area_sqft', '-area_sqft'}
    if sort not in valid_sorts:
        sort = '-created_at'
    qs = qs.order_by(sort)

    paginator = Paginator(qs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'property_types': PropertyType.choices,
        'listing_types': ListingType.choices,
        'request_get': request.GET,
        'result_count': paginator.count,
    }
    return render(request, 'properties/property_list.html', context)


def property_detail(request, slug):
    property_obj = get_object_or_404(
        Property.objects.select_related('agent', 'agent__user').prefetch_related('images', 'features'),
        slug=slug,
    )

    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.property = property_obj
            inquiry.save()
            messages.success(
                request,
                "Thanks — your message has been sent. The agent will be in touch shortly."
            )
            return redirect(property_obj.get_absolute_url())
    else:
        form = InquiryForm()

    similar_properties = (
        Property.objects.filter(
            status='available', city=property_obj.city, property_type=property_obj.property_type
        )
        .exclude(pk=property_obj.pk)
        .prefetch_related('images')[:3]
    )

    context = {
        'property': property_obj,
        'form': form,
        'similar_properties': similar_properties,
    }
    return render(request, 'properties/property_detail.html', context)
