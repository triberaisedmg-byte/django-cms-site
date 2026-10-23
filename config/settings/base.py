"""
Base settings for TribeRaised Django CMS Marketing Site.
These settings are shared across all environments (local, staging, production).
"""

from pathlib import Path
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Initialize django-environ
env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, "insecure-placeholder-key-triberaised-base"),
    ALLOWED_HOSTS=(list, ["localhost", "127.0.0.1"]),
    SITE_ID=(int, 1),
    USE_SQLITE=(bool, False),
    PORT=(int, 8000),
)

# Read .env file if it exists
env_file = BASE_DIR / ".env"
if env_file.exists():
    environ.Env.read_env(env_file)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = env("ALLOWED_HOSTS")

# Site ID required by django.contrib.sites and django CMS
SITE_ID = env("SITE_ID")

# Application definition
INSTALLED_APPS = [
    # django CMS Admin Style must be placed before django.contrib.admin
    "djangocms_admin_style",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # Third-party utilities
    "sekizai",
    "treebeard",
    # django CMS Core
    "cms",
    "menus",
    # CMS Plugins
    "djangocms_text_ckeditor",
    # Project Apps
    "apps.core",
    "apps.marketing_cms",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "apps.core.middleware.SecurityHeadersMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    # django CMS middleware
    "cms.middleware.user.CurrentUserMiddleware",
    "cms.middleware.page.CurrentPageMiddleware",
    "cms.middleware.toolbar.ToolbarMiddleware",
    "cms.middleware.language.LanguageCookieMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                # django CMS & Sekizai context processors
                "sekizai.context_processors.sekizai",
                "cms.context_processors.cms_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# Database Configuration
# PostgreSQL by default; SQLite fallback when USE_SQLITE is True or DATABASE_URL specifies sqlite
USE_SQLITE = env.bool("USE_SQLITE", default=False)

if USE_SQLITE:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    # Build default postgres URL from environment components if DATABASE_URL is not explicitly set
    pg_user = env("POSTGRES_USER", default="postgres")
    pg_password = env("POSTGRES_PASSWORD", default="postgres")
    pg_host = env("POSTGRES_HOST", default="localhost")
    pg_port = env("POSTGRES_PORT", default="5432")
    pg_db = env("POSTGRES_DB", default="triberaised_cms")
    default_db_url = f"postgres://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}"

    DATABASES = {
        "default": env.db("DATABASE_URL", default=default_db_url),
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization & Localization
LANGUAGE_CODE = env("LANGUAGE_CODE", default="en")
TIME_ZONE = env("TIME_ZONE", default="UTC")
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ("en", "English"),
]

# Static files (CSS, JavaScript, Images)
STATIC_URL = env("STATIC_URL", default="/static/")
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Media files (User uploads / CMS assets)
USE_GCS_MEDIA = env.bool("USE_GCS_MEDIA", default=False)
GS_BUCKET_NAME = env.str("GS_BUCKET_NAME", default="")

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
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
else:
    MEDIA_URL = env("MEDIA_URL", default="/media/")
    MEDIA_ROOT = BASE_DIR / "media"
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# django CMS 4 Configuration
CMS_CONFIRM_VERSION4 = True

CMS_TEMPLATES = [
    ("base.html", "Default"),
    ("cms/fullwidth.html", "Full Width"),
]

CMS_PERMISSION = True

# Frame options for django CMS toolbar / edit mode
X_FRAME_OPTIONS = "SAMEORIGIN"
