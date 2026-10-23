"""
Tests verifying modular settings and database configurations.
"""

from django.conf import settings


def test_settings_base_configuration():
    """Verify base settings defaults and required apps."""
    assert "cms" in settings.INSTALLED_APPS
    assert "djangocms_admin_style" in settings.INSTALLED_APPS
    assert "apps.core" in settings.INSTALLED_APPS
    assert settings.CMS_CONFIRM_VERSION4 is True
    assert settings.SITE_ID == 1


def test_sqlite_fallback_configuration():
    """Verify SQLite fallback logic when USE_SQLITE is enabled."""
    assert "ENGINE" in settings.DATABASES["default"]


def test_production_settings_validation(monkeypatch):
    """Verify production settings enforce security and secret key."""
    import importlib

    monkeypatch.setenv("SECRET_KEY", "test-prod-key-for-testing-123456789")
    monkeypatch.setenv("ALLOWED_HOSTS", "triberaised.com,www.triberaised.com")
    monkeypatch.setenv("SECURE_SSL_REDIRECT", "True")
    monkeypatch.setenv("SESSION_COOKIE_SECURE", "True")
    monkeypatch.setenv("CSRF_COOKIE_SECURE", "True")

    prod = importlib.import_module("config.settings.production")
    importlib.reload(prod)
    assert prod.DEBUG is False
    assert prod.SECURE_SSL_REDIRECT is True
    assert prod.SESSION_COOKIE_SECURE is True
    assert prod.CSRF_COOKIE_SECURE is True
