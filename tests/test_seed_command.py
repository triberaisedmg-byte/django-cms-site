"""
Tests verifying the automated seed_marketing_site management command and page hierarchy.
"""

import pytest
from cms.models import Page
from django.core.management import call_command
from django.test import Client


@pytest.mark.django_db
def test_seed_marketing_site_command():
    """Verify seed_marketing_site idempotently creates the CMS tree and plugins."""
    # First execution
    call_command("seed_marketing_site")

    home_page = Page.objects.filter(urls__slug="home").first()
    assert home_page is not None
    assert home_page.is_home is True

    about_page = Page.objects.filter(urls__slug="about").first()
    assert about_page is not None

    solutions_page = Page.objects.filter(urls__slug="solutions").first()
    assert solutions_page is not None

    contact_page = Page.objects.filter(urls__slug="contact").first()
    assert contact_page is not None

    # Verify placeholder plugins on Home page
    ph = home_page.get_placeholders("en").filter(slot="content").first()
    assert ph is not None
    plugins = ph.get_plugins()
    assert plugins.count() >= 5

    # Second execution (must be idempotent)
    call_command("seed_marketing_site")


@pytest.mark.django_db
def test_seeded_pages_accessible_via_client():
    """Verify all seeded pages return 200 OK with expected content."""
    call_command("seed_marketing_site")
    client = Client()

    response = client.get("/")
    assert response.status_code == 200
    content = response.content.decode("utf-8")
    assert "Empowering Neurodivergent Families" in content
    assert "TribeRaised Profile Hub" in content
    assert "Safe Community Forum" in content

    res_about = client.get("/about/", follow=True)
    assert res_about.status_code == 200
    assert "Built by Neurodivergent Families" in res_about.content.decode("utf-8")

    res_solutions = client.get("/solutions/", follow=True)
    assert res_solutions.status_code == 200
    assert "A Unified Digital Ecosystem" in res_solutions.content.decode("utf-8")
