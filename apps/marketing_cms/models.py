"""
Custom CMS Plugin models for TribeRaised marketing website.
"""

from cms.models.pluginmodel import CMSPlugin
from django.db import models


class HeroBannerPluginModel(CMSPlugin):
    """
    Hero banner with headline, mission statement, primary/secondary CTAs,
    badge, and optional background gradient styling.
    """

    GRADIENT_CHOICES = [
        ("indigo_teal", "Indigo & Calming Teal (Default)"),
        ("teal_sage", "Calming Teal & Sage"),
        ("amber_indigo", "Warm Amber & Indigo"),
        ("subtle_night", "Dark Slate Spectrum"),
    ]

    headline = models.CharField(
        max_length=255,
        default="Empowering Neurodivergent Families",
        help_text="Primary headline displayed prominently at the top of the hero.",
    )
    highlight_text = models.CharField(
        max_length=150,
        blank=True,
        default="Through Shared Understanding",
        help_text="Optional gradient-highlighted phrase appended to or within the headline.",
    )
    subheading = models.TextField(
        default="A safe, community-governed digital ecosystem combining private family profiles, sensory-friendly collaboration, and authenticated peer forums.",
        help_text="Mission statement or introductory paragraph below the headline.",
    )
    badge_text = models.CharField(
        max_length=100,
        blank=True,
        default="Neurodivergent-Led Ecosystem",
        help_text="Small pill badge displayed above the main headline.",
    )
    primary_cta_text = models.CharField(
        max_length=100,
        default="Launch Profile Hub",
        help_text="Label for the primary call-to-action button.",
    )
    primary_cta_url = models.CharField(
        max_length=255,
        default="https://profile.triberaised.com",
        help_text="Destination URL for the primary button.",
    )
    secondary_cta_text = models.CharField(
        max_length=100,
        blank=True,
        default="Visit Safe Forum",
        help_text="Label for the optional secondary call-to-action button.",
    )
    secondary_cta_url = models.CharField(
        max_length=255,
        blank=True,
        default="https://forum.triberaised.com",
        help_text="Destination URL for the secondary button.",
    )
    background_gradient = models.CharField(
        max_length=50,
        choices=GRADIENT_CHOICES,
        default="indigo_teal",
        help_text="Background visual accent theme.",
    )

    def __str__(self):
        return f"Hero Banner: {self.headline[:50]}"


class FeatureGridPluginModel(CMSPlugin):
    """
    Container grid for showcasing features and TribeRaised apps.
    """

    COLUMN_CHOICES = [
        (2, "2 Columns (Tablet/Desktop)"),
        (3, "3 Columns (Desktop Default)"),
        (4, "4 Columns (Wide Viewports)"),
    ]

    section_badge = models.CharField(
        max_length=100,
        blank=True,
        default="Core Capabilities",
        help_text="Small badge tag above section title.",
    )
    section_title = models.CharField(
        max_length=255,
        default="Built Specifically for Neurodiversity",
        help_text="Section title for the features grid.",
    )
    section_subtitle = models.TextField(
        blank=True,
        default="Explore the purpose-built tools designed with sensory considerations, executive function support, and family privacy at the core.",
        help_text="Introductory text describing the feature collection.",
    )
    columns = models.PositiveSmallIntegerField(
        choices=COLUMN_CHOICES,
        default=3,
        help_text="Number of cards per row on desktop screens.",
    )

    def __str__(self):
        return f"Features Grid: {self.section_title[:50]}"


class FeatureCardPluginModel(CMSPlugin):
    """
    Individual feature card placed within a FeatureGridPlugin.
    """

    ICON_CHOICES = [
        ("profile", "Profile Hub (Identity & Family Circles)"),
        ("forum", "Safe Forum (Moderated Peer Discussions)"),
        ("app", "Mobile App (Sensory-Friendly Daily Companion)"),
        ("privacy", "Zero Profiling (Strict Privacy & Encryption)"),
        ("calendar", "Shared Family Routine & Visual Calendar"),
        ("heart", "Peer Solidarity & Advocacy"),
    ]

    ACCENT_CHOICES = [
        ("indigo", "Indigo (Nurturing)"),
        ("teal", "Calm Teal (Sensory-Restorative)"),
        ("amber", "Warm Amber (Energizing)"),
        ("sage", "Sage Emerald (Grounded)"),
    ]

    title = models.CharField(
        max_length=150,
        help_text="Card headline / feature name.",
    )
    badge = models.CharField(
        max_length=50,
        blank=True,
        help_text="Optional status or category badge (e.g. 'Live', 'Privacy First').",
    )
    description = models.TextField(
        help_text="Clear explanation of the feature and how it benefits families.",
    )
    icon_name = models.CharField(
        max_length=50,
        choices=ICON_CHOICES,
        default="profile",
        help_text="Visual icon to display.",
    )
    accent_color = models.CharField(
        max_length=50,
        choices=ACCENT_CHOICES,
        default="indigo",
        help_text="Color scheme for the icon badge and hover border.",
    )
    link_text = models.CharField(
        max_length=100,
        blank=True,
        help_text="Optional link label (e.g. 'Learn More').",
    )
    link_url = models.CharField(
        max_length=255,
        blank=True,
        help_text="Destination URL if card is clickable.",
    )

    def __str__(self):
        return f"Feature Card: {self.title[:40]}"


class GalleryPluginModel(CMSPlugin):
    """
    Visual image gallery and app showcase container.
    """

    LAYOUT_CHOICES = [
        ("grid", "Responsive Image Grid (2-3 columns)"),
        ("showcase", "Single Large Spotlight with Thumbnails"),
    ]

    title = models.CharField(
        max_length=200,
        default="A Look Inside TribeRaised",
        help_text="Section title for the gallery.",
    )
    subtitle = models.TextField(
        blank=True,
        default="Thoughtful, clutter-free interfaces designed to reduce cognitive load and sensory overwhelm.",
        help_text="Subheading describing the visual showcase.",
    )
    layout = models.CharField(
        max_length=50,
        choices=LAYOUT_CHOICES,
        default="grid",
    )

    def __str__(self):
        return f"Gallery: {self.title[:50]}"


class GalleryItemPluginModel(CMSPlugin):
    """
    Individual image item in a gallery showcase.
    """

    image_url = models.CharField(
        max_length=500,
        help_text="Direct URL, static path, or GCS object URL for this image.",
    )
    alt_text = models.CharField(
        max_length=255,
        default="TribeRaised Application Screenshot",
        help_text="Descriptive alternative text for accessibility (WCAG AA).",
    )
    caption = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional image caption displayed under or on hover.",
    )
    badge = models.CharField(
        max_length=50,
        blank=True,
        help_text="Optional tag (e.g. 'Dark Mode', 'Mobile UI').",
    )

    def __str__(self):
        return f"Gallery Item: {self.alt_text[:40]}"


class TestimonialPluginModel(CMSPlugin):
    """
    Community story and sensory-friendly quote card.
    """

    __test__ = False

    quote = models.TextField(
        help_text="Quote from a community member or advocate.",
    )
    author_name = models.CharField(
        max_length=100,
        default="Sarah M.",
        help_text="Name or pseudonym of the author.",
    )
    author_role = models.CharField(
        max_length=100,
        blank=True,
        default="Parent of Autistic & ADHD Children",
        help_text="Role, background, or community relation.",
    )
    tag = models.CharField(
        max_length=50,
        blank=True,
        default="Family Experience",
        help_text="Topic tag (e.g. 'Safe Space', 'Parenting Journey').",
    )
    rating_stars = models.PositiveSmallIntegerField(
        default=5,
        help_text="Number of stars (1 to 5) to display.",
    )

    def __str__(self):
        return f"Testimonial from {self.author_name}"


class CtaBannerPluginModel(CMSPlugin):
    """
    Full-width conversion banner routing visitors into authentication.
    """

    STYLE_CHOICES = [
        ("indigo", "Deep Indigo Gradient"),
        ("teal", "Calm Teal Gradient"),
        ("night", "Night Slate Gradient"),
    ]

    headline = models.CharField(
        max_length=255,
        default="Ready to Find Your Tribe?",
        help_text="Banner headline.",
    )
    description = models.TextField(
        default="Join thousands of neurodivergent individuals and families who rely on TribeRaised for genuine belonging, shared support, and total privacy.",
        help_text="Supporting body text.",
    )
    cta_text = models.CharField(
        max_length=100,
        default="Get Started Free",
        help_text="Primary button label.",
    )
    cta_url = models.CharField(
        max_length=255,
        default="https://profile.triberaised.com",
        help_text="Primary button destination URL.",
    )
    secondary_cta_text = models.CharField(
        max_length=100,
        blank=True,
        default="Explore Safe Forum",
        help_text="Secondary button label.",
    )
    secondary_cta_url = models.CharField(
        max_length=255,
        blank=True,
        default="https://forum.triberaised.com",
        help_text="Secondary button destination URL.",
    )
    style = models.CharField(
        max_length=50,
        choices=STYLE_CHOICES,
        default="indigo",
        help_text="Color styling for the conversion banner.",
    )

    def __str__(self):
        return f"CTA Banner: {self.headline[:50]}"
