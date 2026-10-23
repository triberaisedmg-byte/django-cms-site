"""
Production settings for TribeRaised Django CMS Marketing Site.
Configured for Google Cloud Platform (Cloud Run) and containerized deployment.
"""

from .base import *  # noqa: F401, F403
from .base import env

DEBUG = False

# Secret key MUST be supplied via environment variable in production
SECRET_KEY = env("SECRET_KEY")

ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    default=["triberaised.com", "www.triberaised.com", "127.0.0.1", "localhost"],
)

# Reverse proxy SSL header (Google Cloud Run / Cloudflare)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# SSL & Security Redirects
SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=True)
# Cookie SameSite & Security
SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE", default=True)
CSRF_COOKIE_SECURE = env.bool("CSRF_COOKIE_SECURE", default=True)
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False  # Allows CMS frontend / AJAX CSRF handling
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"

# Referrer & Cross-Origin Policies
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"

# HTTP Strict Transport Security (HSTS)
SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=31536000)  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Browser Protection Headers
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# CSRF Trusted Origins for Cloud Run & custom domains
CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS",
    default=[
        "https://triberaised.com",
        "https://www.triberaised.com",
        "https://*.run.app",
    ],
)

# Google Cloud Storage (GCS) and WhiteNoise production storage
USE_GCS_MEDIA = env.bool("USE_GCS_MEDIA", default=True)
GS_BUCKET_NAME = env.str("GS_BUCKET_NAME", default="triberaised-marketing-media")

if USE_GCS_MEDIA and GS_BUCKET_NAME:
    MEDIA_URL = env.str(
        "MEDIA_URL",
        default=f"https://storage.googleapis.com/{GS_BUCKET_NAME}/media/",
    )
    STORAGES = {
        "default": {
            "BACKEND": "config.settings.storage.TribeRaisedGCSMediaStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
else:
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

# Production Logging to STDOUT for GCP Cloud Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "cms": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
