"""
Core application configuration.
"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Configuration for Core application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"
    verbose_name = "Core"
