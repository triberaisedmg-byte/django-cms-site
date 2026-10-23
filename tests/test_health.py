"""
Tests for health check endpoints.
"""

import pytest
from django.test import Client


@pytest.mark.django_db
def test_healthz_endpoint():
    """Verify /healthz returns 200 OK and healthy status."""
    client = Client()
    response = client.get("/healthz")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
    assert data["service"] == "triberaised-django-cms"


@pytest.mark.django_db
def test_healthz_trailing_slash():
    """Verify /healthz/ also returns 200 OK."""
    client = Client()
    response = client.get("/healthz/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
