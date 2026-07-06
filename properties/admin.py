from django.contrib import admin
from django.utils.html import format_html
from .models import Property, PropertyImage, PropertyFeature


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    fields = ('image', 'preview', 'caption', 'is_primary', 'order')
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.pk and obj.image:
            return format_html('<img src="{}" style="height:60px;border-radius:4px;" />', obj.image.url)
        return '—'
    preview.short_description = 'Preview'


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'property_type', 'listing_type', 'status',
        'formatted_price', 'city', 'agent', 'is_featured', 'created_at',
    )
    list_filter = ('property_type', 'listing_type', 'status', 'is_featured', 'city')
    search_fields = ('title', 'description', 'city', 'address_line', 'zip_code')
    list_editable = ('is_featured', 'status')
    autocomplete_fields = ('agent',)
    filter_horizontal = ('features',)
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    inlines = [PropertyImageInline]
    list_per_page = 25

    fieldsets = (
        ('Basics', {
            'fields': ('title', 'slug', 'description', 'property_type', 'listing_type', 'status', 'is_featured')
        }),
        ('Pricing', {'fields': ('price',)}),
        ('Location', {
            'fields': ('address_line', 'city', 'state', 'zip_code', 'latitude', 'longitude')
        }),
        ('Specs', {
            'fields': ('bedrooms', 'bathrooms', 'area_sqft', 'lot_size_sqft', 'year_built', 'parking_spaces')
        }),
        ('Features & Agent', {'fields': ('features', 'agent')}),
        ('Meta', {'fields': ('created_at', 'updated_at')}),
    )

    def formatted_price(self, obj):
        suffix = '/mo' if obj.is_for_rent else ''
        return f'${obj.price:,.0f}{suffix}'
    formatted_price.short_description = 'Price'


@admin.register(PropertyFeature)
class PropertyFeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name',)
