"""
Tests verifying Google Cloud Storage (GCS) media backend,
fallback storage behavior, and responsive image pipeline configurations.
"""

import pytest
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from config.settings.storage import (
    ALLOWED_IMAGE_EXTENSIONS,
    RESPONSIVE_IMAGE_SPECS,
    TribeRaisedGCSMediaStorage,
)


def test_responsive_image_specifications():
    """Verify responsive image breakpoint definitions."""
    assert "sm" in RESPONSIVE_IMAGE_SPECS
    assert "md" in RESPONSIVE_IMAGE_SPECS
    assert "lg" in RESPONSIVE_IMAGE_SPECS
    assert "retina" in RESPONSIVE_IMAGE_SPECS

    assert RESPONSIVE_IMAGE_SPECS["sm"]["width"] == 360
    assert RESPONSIVE_IMAGE_SPECS["md"]["width"] == 720
    assert RESPONSIVE_IMAGE_SPECS["lg"]["width"] == 1280
    assert RESPONSIVE_IMAGE_SPECS["retina"]["width"] == 1920

    assert "webp" in ALLOWED_IMAGE_EXTENSIONS
    assert "avif" in ALLOWED_IMAGE_EXTENSIONS


def test_gcs_storage_configuration_attributes():
    """Verify TribeRaisedGCSMediaStorage settings enforce security and CDN caching."""
    storage = TribeRaisedGCSMediaStorage()
    assert storage.file_overwrite is False
    assert storage.default_acl is None  # Uniform Bucket-Level Access
    assert storage.querystring_auth is False  # Public CDN delivery without expiring signatures
    assert "max-age=31536000" in storage.cache_control


def test_local_storage_fallback():
    """Verify system defaults to FileSystemStorage when USE_GCS_MEDIA is false."""
    from django.core.files.storage import storages

    default_storage = storages["default"]
    # In local testing without USE_GCS_MEDIA=True, default storage should be FileSystemStorage
    assert isinstance(default_storage, FileSystemStorage)
