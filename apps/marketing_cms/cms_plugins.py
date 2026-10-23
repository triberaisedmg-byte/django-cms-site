"""
Django CMS Plugin registrations for TribeRaised marketing sections.
"""

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from .models import (
    CtaBannerPluginModel,
    FeatureCardPluginModel,
    FeatureGridPluginModel,
    GalleryItemPluginModel,
    GalleryPluginModel,
    HeroBannerPluginModel,
    TestimonialPluginModel,
)


@plugin_pool.register_plugin
class HeroBannerPlugin(CMSPluginBase):
    """
    Renders high-impact Hero Banner with TribeRaised branding, typography,
    and direct conversion CTAs.
    """

    model = HeroBannerPluginModel
    name = _("Hero Banner (TribeRaised)")
    render_template = "cms_plugins/hero_plugin.html"
    module = _("TribeRaised Marketing")
    cache = True

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context.update({"instance": instance})
        return context


@plugin_pool.register_plugin
class FeatureGridPlugin(CMSPluginBase):
    """
    Renders a responsive multi-column features grid.
    Can contain child FeatureCard plugins.
    """

    model = FeatureGridPluginModel
    name = _("Features Grid Container")
    render_template = "cms_plugins/features_grid_plugin.html"
    module = _("TribeRaised Marketing")
    allow_children = True
    child_classes = ["FeatureCardPlugin"]

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context.update({"instance": instance})
        return context


@plugin_pool.register_plugin
class FeatureCardPlugin(CMSPluginBase):
    """
    Individual feature card placed inside Features Grid.
    """

    model = FeatureCardPluginModel
    name = _("Feature Card")
    render_template = "cms_plugins/feature_card_plugin.html"
    module = _("TribeRaised Marketing")
    require_parent = True
    parent_classes = ["FeatureGridPlugin"]

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context.update({"instance": instance})
        return context


@plugin_pool.register_plugin
class GalleryPlugin(CMSPluginBase):
    """
    App showcase and responsive media gallery container.
    """

    model = GalleryPluginModel
    name = _("Image Gallery Showcase")
    render_template = "cms_plugins/gallery_plugin.html"
    module = _("TribeRaised Marketing")
    allow_children = True
    child_classes = ["GalleryItemPlugin"]

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context.update({"instance": instance})
        return context


@plugin_pool.register_plugin
class GalleryItemPlugin(CMSPluginBase):
    """
    Single screenshot or image inside Gallery Showcase.
    """

    model = GalleryItemPluginModel
    name = _("Gallery Image Item")
    render_template = "cms_plugins/gallery_item_plugin.html"
    module = _("TribeRaised Marketing")
    require_parent = True
    parent_classes = ["GalleryPlugin"]

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context.update({"instance": instance})
        return context


@plugin_pool.register_plugin
class TestimonialPlugin(CMSPluginBase):
    """
    Renders a sensory-friendly community quote card.
    """

    model = TestimonialPluginModel
    name = _("Community Story / Testimonial")
    render_template = "cms_plugins/testimonial_plugin.html"
    module = _("TribeRaised Marketing")
    cache = True

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context.update({"instance": instance})
        return context


@plugin_pool.register_plugin
class CtaBannerPlugin(CMSPluginBase):
    """
    Full-width conversion banner routing visitors into authentication.
    """

    model = CtaBannerPluginModel
    name = _("Call to Action Banner")
    render_template = "cms_plugins/cta_banner_plugin.html"
    module = _("TribeRaised Marketing")
    cache = True

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context.update({"instance": instance})
        return context
