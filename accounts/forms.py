from django import forms
from properties.models import Property, PropertyImage, PropertyFeature


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'description', 'property_type', 'listing_type', 'status',
            'price', 'address_line', 'city', 'state', 'zip_code',
            'bedrooms', 'bathrooms', 'area_sqft', 'lot_size_sqft',
            'year_built', 'parking_spaces', 'features', 'is_featured',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 5}),
            'property_type': forms.Select(attrs={'class': 'form-input'}),
            'listing_type': forms.Select(attrs={'class': 'form-input'}),
            'status': forms.Select(attrs={'class': 'form-input'}),
            'price': forms.NumberInput(attrs={'class': 'form-input'}),
            'address_line': forms.TextInput(attrs={'class': 'form-input'}),
            'city': forms.TextInput(attrs={'class': 'form-input'}),
            'state': forms.TextInput(attrs={'class': 'form-input'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-input'}),
            'bedrooms': forms.NumberInput(attrs={'class': 'form-input'}),
            'bathrooms': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.5'}),
            'area_sqft': forms.NumberInput(attrs={'class': 'form-input'}),
            'lot_size_sqft': forms.NumberInput(attrs={'class': 'form-input'}),
            'year_built': forms.NumberInput(attrs={'class': 'form-input'}),
            'parking_spaces': forms.NumberInput(attrs={'class': 'form-input'}),
            'features': forms.CheckboxSelectMultiple(),
        }


class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image', 'caption', 'is_primary']
        widgets = {
            'caption': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Optional caption'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cover photo is optional at the HTML/form level — views.py only
        # processes this form when a file was actually provided.
        self.fields['image'].required = False
