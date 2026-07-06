from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactMessageForm


def contact(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent. We'll get back to you soon.")
            return redirect('inquiries:contact')
    else:
        form = ContactMessageForm()

    return render(request, 'inquiries/contact.html', {'form': form})
