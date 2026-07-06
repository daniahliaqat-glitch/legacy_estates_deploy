from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from accounts.models import Agent


class PropertyType(models.TextChoices):
    HOUSE = 'house', 'House'
    APARTMENT = 'apartment', 'Apartment'
    PLOT = 'plot', 'Plot / Land'
    COMMERCIAL = 'commercial', 'Commercial'


class ListingType(models.TextChoices):
    SALE = 'sale', 'For Sale'
    RENT = 'rent', 'For Rent'


class PropertyStatus(models.TextChoices):
    AVAILABLE = 'available', 'Available'
    PENDING = 'pending', 'Pending'
    SOLD = 'sold', 'Sold'
    RENTED = 'rented', 'Rented'


class Property(models.Model):
    """A single property listing — house, apartment, plot, or commercial unit."""

    # Core info
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()

    property_type = models.CharField(
        max_length=20, choices=PropertyType.choices, default=PropertyType.HOUSE
    )
    listing_type = models.CharField(
        max_length=10, choices=ListingType.choices, default=ListingType.SALE
    )
    status = models.CharField(
        max_length=10, choices=PropertyStatus.choices, default=PropertyStatus.AVAILABLE
    )

    # Pricing — rent price is monthly when listing_type == rent
    price = models.DecimalField(max_digits=14, decimal_places=2)

    # Location
    address_line = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    # Specs — not all apply to every property_type (e.g. plots have no bedrooms)
    bedrooms = models.PositiveSmallIntegerField(blank=True, null=True)
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    area_sqft = models.PositiveIntegerField(help_text='Total area in square feet')
    lot_size_sqft = models.PositiveIntegerField(blank=True, null=True)
    year_built = models.PositiveSmallIntegerField(blank=True, null=True)
    parking_spaces = models.PositiveSmallIntegerField(default=0)

    # Relationships
    agent = models.ForeignKey(
        Agent, on_delete=models.SET_NULL, null=True, related_name='properties'
    )

    # Flags
    is_featured = models.BooleanField(
        default=False, help_text='Featured properties appear on the homepage.'
    )

    features = models.ManyToManyField(
        'PropertyFeature', blank=True, related_name='properties'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Properties'
        indexes = [
            models.Index(fields=['city']),
            models.Index(fields=['property_type']),
            models.Index(fields=['listing_type']),
            models.Index(fields=['status']),
            models.Index(fields=['price']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)[:200]
            slug = base_slug
            counter = 1
            while Property.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('properties:detail', kwargs={'slug': self.slug})

    @property
    def primary_image(self):
        img = self.images.filter(is_primary=True).first()
        return img or self.images.first()

    @property
    def is_for_rent(self):
        return self.listing_type == ListingType.RENT

    @property
    def full_address(self):
        parts = [self.address_line, self.city, self.state, self.zip_code]
        return ', '.join(p for p in parts if p)


class PropertyImage(models.Model):
    """Photo gallery for a property. One image may be marked primary (the
    card/hero thumbnail)."""

    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name='images'
    )
    image = models.ImageField(upload_to='properties/%Y/%m/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f'Image for {self.property.title}'


class PropertyFeature(models.Model):
    """Reusable amenity/feature tags, e.g. 'Swimming Pool', 'Garden',
    'Central AC' — assignable to many properties (many-to-many)."""

    name = models.CharField(max_length=80, unique=True)
    icon = models.CharField(
        max_length=50, blank=True,
        help_text="Optional icon keyword, e.g. 'pool', 'garage', 'wifi'",
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
