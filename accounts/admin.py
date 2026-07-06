from django.contrib import admin
from django.contrib.auth.models import User
from .models import Agent


class AgentInline(admin.StackedInline):
    model = Agent
    can_delete = False
    extra = 0


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'phone', 'years_experience', 'active_listing_count', 'is_active_agent')
    list_filter = ('is_active_agent', 'title')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone', 'license_number')
    autocomplete_fields = ('user',)
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Account', {'fields': ('user', 'is_active_agent')}),
        ('Profile', {'fields': ('title', 'headshot', 'bio', 'years_experience', 'license_number')}),
        ('Contact', {'fields': ('phone',)}),
        ('Meta', {'fields': ('created_at',)}),
    )
