"""
Development settings for TribeRaised Django CMS Marketing Site.
Suitable for local workstation development.
"""

from .base import *  # noqa: F401, F403
from .base import env

DEBUG = env.bool("DEBUG", default=True)

SECRET_KEY = env.str(
    "SECRET_KEY",
    default="django-insecure-triberaised-marketing-cms-local-dev-key",
)

ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    default=["localhost", "127.0.0.1", "0.0.0.0", "[::1]", "web"],
)

# Email Backend for local development
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Ensure debug-friendly CSRF origins for local ports
CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS",
    default=[
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:8001",
        "http://127.0.0.1:8001",
    ],
)
