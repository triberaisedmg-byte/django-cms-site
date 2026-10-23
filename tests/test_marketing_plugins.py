"""
Tests verifying custom Django CMS plugins for TribeRaised marketing components.
"""

import pytest
from cms.plugin_pool import plugin_pool
from django.template.loader import render_to_string

from apps.marketing_cms.models import (
    CtaBannerPluginModel,
    FeatureCardPluginModel,
    FeatureGridPluginModel,
    GalleryItemPluginModel,
    GalleryPluginModel,
    HeroBannerPluginModel,
    TestimonialPluginModel,
)


def test_plugins_registered_in_cms():
    """Verify all marketing plugins are registered in the CMS plugin pool."""
    registered = [p.__name__ for p in plugin_pool.get_all_plugins()]
    assert "HeroBannerPlugin" in registered
    assert "FeatureGridPlugin" in registered
    assert "FeatureCardPlugin" in registered
    assert "GalleryPlugin" in registered
    assert "GalleryItemPlugin" in registered
    assert "TestimonialPlugin" in registered
    assert "CtaBannerPlugin" in registered


@pytest.mark.django_db
def test_hero_banner_plugin_rendering():
    """Verify HeroBannerPlugin renders expected HTML, headline, and CTAs."""
    hero = HeroBannerPluginModel.objects.create(
        headline="Empowering Neurodivergent Families",
        highlight_text="Through Safe Spaces",
        subheading="Join our safe, sensory-friendly community ecosystem.",
        primary_cta_text="Launch Profile",
        primary_cta_url="https://profile.triberaised.com",
        secondary_cta_text="Visit Forum",
        secondary_cta_url="https://forum.triberaised.com",
    )
    html = render_to_string("cms_plugins/hero_plugin.html", {"instance": hero})
    assert "Empowering Neurodivergent Families" in html
    assert "Through Safe Spaces" in html
    assert "Launch Profile" in html
    assert "https://profile.triberaised.com" in html
    assert "Visit Forum" in html


@pytest.mark.django_db
def test_feature_card_plugin_rendering():
    """Verify FeatureCardPluginModel renders with accent colors and icons."""
    card = FeatureCardPluginModel.objects.create(
        title="Safe Family Circles",
        badge="Live",
        description="Private workspaces for families with end-to-end encryption.",
        icon_name="profile",
        accent_color="teal",
        link_text="Learn More",
        link_url="/solutions/profiles/",
    )
    html = render_to_string("cms_plugins/feature_card_plugin.html", {"instance": card})
    assert "Safe Family Circles" in html
    assert "Live" in html
    assert "Private workspaces" in html
    assert "Learn More" in html


@pytest.mark.django_db
def test_gallery_item_plugin_rendering():
    """Verify GalleryItemPluginModel renders image, caption, and fallback."""
    item = GalleryItemPluginModel.objects.create(
        image_url="https://storage.googleapis.com/triberaised-marketing/preview.png",
        alt_text="Profile Hub Interface",
        caption="Modern family profile manager",
        badge="Web App",
    )
    html = render_to_string("cms_plugins/gallery_item_plugin.html", {"instance": item})
    assert "https://storage.googleapis.com/triberaised-marketing/preview.png" in html
    assert "Profile Hub Interface" in html
    assert "Modern family profile manager" in html
    assert "Web App" in html


@pytest.mark.django_db
def test_testimonial_plugin_rendering():
    """Verify TestimonialPluginModel renders quote, author, and rating stars."""
    testimonial = TestimonialPluginModel.objects.create(
        quote="TribeRaised gave our family a calm, judgment-free space.",
        author_name="Elena R.",
        author_role="Mother of two neurodivergent teens",
        tag="Parent Story",
        rating_stars=5,
    )
    html = render_to_string("cms_plugins/testimonial_plugin.html", {"instance": testimonial})
    assert "TribeRaised gave our family a calm" in html
    assert "Elena R." in html
    assert "Mother of two neurodivergent teens" in html
    assert "Parent Story" in html


@pytest.mark.django_db
def test_cta_banner_plugin_rendering():
    """Verify CtaBannerPluginModel renders conversion headlines and CTA links."""
    banner = CtaBannerPluginModel.objects.create(
        headline="Ready to Find Your Tribe?",
        description="Join thousands of families who trust TribeRaised.",
        cta_text="Create Free Account",
        cta_url="https://profile.triberaised.com/signup",
        secondary_cta_text="Read Safe Forum",
        secondary_cta_url="https://forum.triberaised.com",
    )
    html = render_to_string("cms_plugins/cta_banner_plugin.html", {"instance": banner})
    assert "Ready to Find Your Tribe?" in html
    assert "Create Free Account" in html
    assert "https://profile.triberaised.com/signup" in html
