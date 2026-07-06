from django.conf import settings
from django.db import models
from django.urls import reverse


class Agent(models.Model):
    """
    Extends Django's built-in User model with real-estate-agent specific
    profile data. Every Agent has exactly one linked User account, which is
    how they log in to manage their listings.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='agent_profile',
    )
    phone = models.CharField(max_length=20)
    headshot = models.ImageField(
        upload_to='agents/headshots/', blank=True, null=True
    )
    title = models.CharField(
        max_length=120,
        default='Real Estate Agent',
        help_text="e.g. 'Senior Agent', 'Luxury Specialist'",
    )
    bio = models.TextField(blank=True)
    years_experience = models.PositiveIntegerField(default=0)
    license_number = models.CharField(max_length=60, blank=True)
    is_active_agent = models.BooleanField(
        default=True,
        help_text='Inactive agents are hidden from public agent listings.',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-years_experience']

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    def get_absolute_url(self):
        return reverse('accounts:agent_detail', kwargs={'pk': self.pk})

    @property
    def active_listing_count(self):
        return self.properties.filter(status='available').count()
