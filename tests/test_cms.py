"""
Tests verifying Django CMS page tree, templates, and admin access.
"""

import pytest
from cms.api import create_page
from cms.models import Page
from django.test import Client


@pytest.mark.django_db
def test_cms_page_creation():
    """Verify that a CMS page can be created programmatically."""
    page = create_page(
        title="Test Marketing Home",
        template="base.html",
        language="en",
        slug="test-home",
    )
    assert page is not None
    assert Page.objects.count() >= 1


@pytest.mark.django_db
def test_admin_accessible(admin_user):
    """Verify admin login and access to the CMS page admin."""
    client = Client()
    client.force_login(admin_user)

    # Check main admin index
    res = client.get("/admin/")
    assert res.status_code == 200

    # Check CMS page admin endpoint (redirects to pagecontent list)
    res_page = client.get("/admin/cms/page/", follow=True)
    assert res_page.status_code == 200


@pytest.mark.django_db
def test_root_page_serves_html():
    """Verify the root endpoint serves valid HTML."""
    client = Client()
    response = client.get("/")
    assert response.status_code == 200
