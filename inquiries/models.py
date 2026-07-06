from django.db import models
from properties.models import Property


class InquiryStatus(models.TextChoices):
    NEW = 'new', 'New'
    CONTACTED = 'contacted', 'Contacted'
    CLOSED = 'closed', 'Closed'


class Inquiry(models.Model):
    """
    A message from a (non-logged-in) buyer or seller about a specific
    property. The assigned agent (or admin, if unassigned) follows up
    using the contact details given here — no account needed to send one.
    """

    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name='inquiries'
    )
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()

    status = models.CharField(
        max_length=10, choices=InquiryStatus.choices, default=InquiryStatus.NEW
    )
    internal_notes = models.TextField(
        blank=True, help_text='Private notes for agent/admin use only.'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Inquiries'

    def __str__(self):
        return f'Inquiry from {self.name} about {self.property.title}'


class ContactMessage(models.Model):
    """General 'Contact Us' messages not tied to a specific property
    (e.g. someone wanting to list a property for sale, or a general
    question to the agency)."""

    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Message from {self.name}'
