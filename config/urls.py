"""
Root URL configuration for TribeRaised Marketing Site.
"""

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from apps.core.views import healthz

# Non-localized operational endpoints (probes, metrics)
urlpatterns = [
    path("healthz", healthz, name="healthz"),
    path("healthz/", healthz, name="healthz_slash"),
]

# Localized CMS and Admin routes
urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("", include("cms.urls")),
    prefix_default_language=False,
)

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
