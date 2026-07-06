from django.contrib import admin
from .models import Inquiry, ContactMessage


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'property', 'email', 'phone', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'phone', 'property__title', 'message')
    list_editable = ('status',)
    readonly_fields = ('property', 'name', 'email', 'phone', 'message', 'created_at')
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Inquiry', {'fields': ('property', 'name', 'email', 'phone', 'message', 'created_at')}),
        ('Follow-up', {'fields': ('status', 'internal_notes')}),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'email', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_editable = ('is_read',)
    readonly_fields = ('name', 'email', 'phone', 'subject', 'message', 'created_at')
