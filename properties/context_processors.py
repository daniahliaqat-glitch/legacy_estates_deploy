from django.conf import settings


def site_settings(request):
    """Makes site name/tagline available in every template without
    passing them explicitly from every view."""
    return {
        'SITE_NAME': getattr(settings, 'SITE_NAME', 'Legacy Estates'),
        'SITE_TAGLINE': getattr(settings, 'SITE_TAGLINE', ''),
    }
