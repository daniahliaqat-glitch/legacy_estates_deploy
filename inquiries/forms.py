from django import forms
from .models import Inquiry, ContactMessage


class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your full name', 'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'placeholder': 'you@example.com', 'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'placeholder': '(optional)', 'class': 'form-input'}),
            'message': forms.Textarea(attrs={
                'placeholder': "I'm interested in this property. Please contact me with more details.",
                'class': 'form-input', 'rows': 4,
            }),
        }


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your full name', 'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'placeholder': 'you@example.com', 'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'placeholder': '(optional)', 'class': 'form-input'}),
            'subject': forms.TextInput(attrs={'placeholder': "What's this about?", 'class': 'form-input'}),
            'message': forms.Textarea(attrs={'placeholder': 'Your message', 'class': 'form-input', 'rows': 5}),
        }
