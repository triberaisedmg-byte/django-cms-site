"""
Media storage backend and responsive image processing configuration.
Supports Google Cloud Storage (GCS) with ADC for production,
and graceful fallback to local FileSystemStorage or MinIO for local development.
"""

import os
from storages.backends.gcloud import GoogleCloudStorage


class TribeRaisedGCSMediaStorage(GoogleCloudStorage):
    """
    Custom Google Cloud Storage backend for user & admin media uploads.
    Optimized for public CDN delivery (Cloudflare) and Google Cloud Run.
    """

    bucket_name = os.getenv("GS_BUCKET_NAME", "triberaised-marketing-media")
    location = os.getenv("GS_MEDIA_PREFIX", "media")
    file_overwrite = False
    # Set default_acl to None to enforce GCP Uniform Bucket-Level Access (security best practice)
    default_acl = None
    # Public HTTPS URLs (no temporary query string tokens)
    querystring_auth = False
    # Long-lived immutable caching headers for Cloudflare / browser edge caches
    cache_control = os.getenv("GS_CACHE_CONTROL", "public, max-age=31536000, immutable")
    # Custom CDN domain if specified (e.g., media.triberaised.com)
    custom_endpoint = os.getenv("GS_CUSTOM_ENDPOINT", None)


# ------------------------------------------------------------------------------
# Responsive Image Breakpoint & Thumbnailing Pipeline Specifications
# ------------------------------------------------------------------------------
RESPONSIVE_IMAGE_SPECS = {
    "thumbnail": {"width": 150, "height": 150, "quality": 85, "format": "WEBP"},
    "sm": {"width": 360, "height": 240, "quality": 85, "format": "WEBP"},
    "md": {"width": 720, "height": 480, "quality": 85, "format": "WEBP"},
    "lg": {"width": 1280, "height": 720, "quality": 88, "format": "WEBP"},
    "retina": {"width": 1920, "height": 1080, "quality": 90, "format": "WEBP"},
}

# Supported modern formats
ALLOWED_IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "webp", "avif", "svg", "gif"]
