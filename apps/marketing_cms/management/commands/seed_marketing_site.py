"""
Management command to idempotently scaffold the initial TribeRaised marketing site
page tree, CMS plugins, placeholder media, and navigation hierarchy.
"""

from cms.api import add_plugin, create_page
from cms.models import Page, PageContent
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = "Idempotently seed default TribeRaised marketing pages and CMS plugins"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Starting TribeRaised marketing site seed..."))

        # 1. Ensure system admin user exists for page creation attribution
        User = get_user_model()
        admin_user, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@triberaised.com",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created:
            admin_user.set_password("admin")
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created admin user (admin / admin)."))

        # 2. Build or update pages
        home_page = self._seed_home_page(admin_user)
        about_page = self._seed_about_page(admin_user)
        solutions_page = self._seed_solutions_page(admin_user)
        contact_page = self._seed_contact_page(admin_user)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully seeded marketing page tree:\n"
                f" - Home (is_home=True)\n"
                f" - About Us (/about/)\n"
                f" - Solutions (/solutions/)\n"
                f" - Contact (/contact/)\n"
            )
        )

    def _get_or_create_page(self, title, slug, template="base.html", is_home=False):
        """Retrieve existing page by slug or create a new one."""
        page = Page.objects.filter(urls__slug=slug).first()
        if page:
            if is_home and not page.is_home:
                page.set_as_homepage()
            return page, False

        page = create_page(
            title=title,
            template=template,
            language="en",
            slug=slug,
            in_navigation=True,
        )
        if is_home:
            page.set_as_homepage()
        return page, True

    def _seed_home_page(self, user):
        page, _ = self._get_or_create_page("Home", "home", is_home=True)
        ph = page.get_placeholders("en").filter(slot="content").first()
        if not ph:
            return page

        if ph.get_plugins().exists():
            self.stdout.write("Home page already has plugins, skipping.")
            return page

        # Hero Banner
        add_plugin(
            ph,
            "HeroBannerPlugin",
            "en",
            headline="Empowering Neurodivergent Families",
            highlight_text="Through Shared Understanding",
            subheading="A safe, community-governed digital ecosystem combining private family profiles, sensory-friendly collaboration, and authenticated peer forums.",
            badge_text="Neurodivergent-Led Ecosystem",
            primary_cta_text="Launch Profile Hub",
            primary_cta_url="https://profile.triberaised.com",
            secondary_cta_text="Visit Safe Forum",
            secondary_cta_url="https://forum.triberaised.com",
            background_gradient="indigo_teal",
        )

        # Features Grid
        grid = add_plugin(
            ph,
            "FeatureGridPlugin",
            "en",
            section_badge="Ecosystem Apps & Capabilities",
            section_title="Purpose-Built for Sensory Comfort & Family Privacy",
            section_subtitle="Explore interconnected tools designed to reduce cognitive friction, support executive function, and protect family sovereignty.",
            columns=3,
        )

        # Feature Cards
        add_plugin(
            ph,
            "FeatureCardPlugin",
            "en",
            target=grid,
            title="TribeRaised Profile Hub",
            badge="Identity & Circles",
            description="Manage private family circles, sensory profiles, and dependent care preferences in a secure, non-commercial environment.",
            icon_name="profile",
            accent_color="indigo",
            link_text="Launch Profile Portal",
            link_url="https://profile.triberaised.com",
        )

        add_plugin(
            ph,
            "FeatureCardPlugin",
            "en",
            target=grid,
            title="Safe Community Forum",
            badge="Moderated Space",
            description="Engage in peer-to-peer discussions with transparent, neurodiversity-affirming moderation rules and zero advertising.",
            icon_name="forum",
            accent_color="teal",
            link_text="Explore Discussions",
            link_url="https://forum.triberaised.com",
        )

        add_plugin(
            ph,
            "FeatureCardPlugin",
            "en",
            target=grid,
            title="Sensory-Friendly UX",
            badge="Cognitive Accessibility",
            description="Soft contrast palettes, persistent dark/light preferences, and calm layouts designed to prevent sensory overload.",
            icon_name="heart",
            accent_color="amber",
            link_text="View Guidelines",
            link_url="/about/",
        )

        add_plugin(
            ph,
            "FeatureCardPlugin",
            "en",
            target=grid,
            title="Zero Commercial Profiling",
            badge="Privacy First",
            description="Your family's health, routines, and identity data are never monetized, tracked across the web, or sold to third parties.",
            icon_name="privacy",
            accent_color="sage",
            link_text="Read Privacy Policy",
            link_url="/privacy/",
        )

        add_plugin(
            ph,
            "FeatureCardPlugin",
            "en",
            target=grid,
            title="Universal Mobile App",
            badge="Daily Companion",
            description="Visual schedules, sensory check-ins, and shared routines available across desktop web, iOS, and Android.",
            icon_name="app",
            accent_color="indigo",
            link_text="Download App",
            link_url="https://app.triberaised.com",
        )

        add_plugin(
            ph,
            "FeatureCardPlugin",
            "en",
            target=grid,
            title="Shared Family Calendar",
            badge="Routine Support",
            description="Collaborative visual calendars supporting multi-caregiver coordination and school transition planning.",
            icon_name="calendar",
            accent_color="teal",
            link_text="Learn More",
            link_url="/solutions/",
        )

        # Image Gallery Showcase
        gallery = add_plugin(
            ph,
            "GalleryPlugin",
            "en",
            title="Designed for Clarity and Calm",
            subtitle="Take a look at the interfaces and tools built for neurodivergent households.",
            layout="grid",
        )

        add_plugin(
            ph,
            "GalleryItemPlugin",
            "en",
            target=gallery,
            image_url="/static/images/marketing/profile_hub_preview.svg",
            alt_text="Profile Hub Interface Screenshot",
            caption="Profile Hub: Private Family Circles and Dependent Management",
            badge="Web Portal",
        )

        add_plugin(
            ph,
            "GalleryItemPlugin",
            "en",
            target=gallery,
            image_url="/static/images/marketing/safe_forum_preview.svg",
            alt_text="Safe Forum Interface Screenshot",
            caption="Safe Forum: Constructive, algorithm-free community conversations",
            badge="Safe Space",
        )

        add_plugin(
            ph,
            "GalleryItemPlugin",
            "en",
            target=gallery,
            image_url="/static/images/marketing/family_circles_preview.svg",
            alt_text="Family Circles Architecture Screenshot",
            caption="Caregiver Access: Granular permissions for therapists, educators, and family",
            badge="Security",
        )

        # Community Story / Testimonial
        add_plugin(
            ph,
            "TestimonialPlugin",
            "en",
            quote="TribeRaised gave our family a calm, judgment-free space to connect with other neurodivergent families who truly understand our day-to-day journey.",
            author_name="Sarah & David M.",
            author_role="Parents of Autistic & ADHD Children",
            tag="Family Story",
            rating_stars=5,
        )

        # Call To Action Banner
        add_plugin(
            ph,
            "CtaBannerPlugin",
            "en",
            headline="Ready to Find Your Tribe?",
            description="Join thousands of neurodivergent families who rely on TribeRaised for genuine belonging, shared support, and total privacy.",
            cta_text="Launch Free Profile",
            cta_url="https://profile.triberaised.com",
            secondary_cta_text="Visit Safe Forum",
            secondary_cta_url="https://forum.triberaised.com",
            style="indigo",
        )

        self.stdout.write("Scaffolded Home page plugins.")
        return page

    def _seed_about_page(self, user):
        page, _ = self._get_or_create_page("About Us", "about")
        ph = page.get_placeholders("en").filter(slot="content").first()
        if not ph:
            return page

        if ph.get_plugins().exists():
            self.stdout.write("About Us page already has plugins, skipping.")
            return page

        add_plugin(
            ph,
            "HeroBannerPlugin",
            "en",
            headline="Built by Neurodivergent Families,",
            highlight_text="For Neurodivergent Families",
            subheading="We believe digital spaces should nurture rather than overwhelm. TribeRaised provides tools and community spaces designed from the ground up for sensory comfort, executive function, and psychological safety.",
            badge_text="Our Mission & Philosophy",
            primary_cta_text="Join the Tribe",
            primary_cta_url="https://profile.triberaised.com",
            secondary_cta_text="Read Forum Principles",
            secondary_cta_url="https://forum.triberaised.com",
            background_gradient="teal_sage",
        )

        grid = add_plugin(
            ph,
            "FeatureGridPlugin",
            "en",
            section_badge="Core Values",
            section_title="What Sets TribeRaised Apart",
            section_subtitle="Our founding principles guide every technical, design, and governance decision.",
            columns=3,
        )

        add_plugin(
            ph,
            "FeatureCardPlugin",
            "en",
            target=grid,
            title="Sensory-Friendly Architecture",
            badge="WCAG 2.1 AA",
            description="Muted contrast palettes, gentle animations, and cognitive load reduction built into every interface.",
            icon_name="heart",
            accent_color="teal",
        )

        add_plugin(
            ph,
            "FeatureCardPlugin",
            "en",
            target=grid,
            title="Community Governance",
            badge="Grassroots",
            description="Platform policies and moderation standards are guided by lived neurodivergent experiences, not corporate advertiser incentives.",
            icon_name="forum",
            accent_color="indigo",
        )

        add_plugin(
            ph,
            "FeatureCardPlugin",
            "en",
            target=grid,
            title="Zero Behavioral Profiling",
            badge="Ethical Tech",
            description="No behavioral ad targeting. No harvesting of dependent health records. Complete export and deletion rights at any time.",
            icon_name="privacy",
            accent_color="sage",
        )

        add_plugin(
            ph,
            "TestimonialPlugin",
            "en",
            quote="Finally an app that respects sensory limits instead of bombarding parents with high-stress alerts and ads.",
            author_name="Marcus K.",
            author_role="Adult Autistic Advocate & Parent",
            tag="Advocate Perspective",
            rating_stars=5,
        )

        self.stdout.write("Scaffolded About Us page plugins.")
        return page

    def _seed_solutions_page(self, user):
        page, _ = self._get_or_create_page("Solutions", "solutions")
        ph = page.get_placeholders("en").filter(slot="content").first()
        if not ph:
            return page

        if ph.get_plugins().exists():
            self.stdout.write("Solutions page already has plugins, skipping.")
            return page

        add_plugin(
            ph,
            "HeroBannerPlugin",
            "en",
            headline="A Unified Digital Ecosystem",
            highlight_text="For Every Step of Your Journey",
            subheading="Explore our interconnected suite of applications built on open standards, single sign-on federated identity, and accessible UX.",
            badge_text="Platform Architecture",
            primary_cta_text="Explore Profile Portal",
            primary_cta_url="https://profile.triberaised.com",
            secondary_cta_text="Community Forum",
            secondary_cta_url="https://forum.triberaised.com",
            background_gradient="indigo_teal",
        )

        gallery = add_plugin(
            ph,
            "GalleryPlugin",
            "en",
            title="Interactive App Previews",
            subtitle="See how TribeRaised apps integrate across web and mobile.",
            layout="grid",
        )

        add_plugin(
            ph,
            "GalleryItemPlugin",
            "en",
            target=gallery,
            image_url="/static/images/marketing/mobile_app_preview.svg",
            alt_text="Universal Mobile App Screenshot",
            caption="Universal Mobile App: Visual routine cards and sensory limit trackers",
            badge="Flutter Client",
        )

        add_plugin(
            ph,
            "GalleryItemPlugin",
            "en",
            target=gallery,
            image_url="/static/images/marketing/family_circles_preview.svg",
            alt_text="Caregiver Circle Permissions",
            caption="Granular access controls for therapists, educators, and family members",
            badge="Access Control",
        )

        add_plugin(
            ph,
            "CtaBannerPlugin",
            "en",
            headline="Get Started with TribeRaised Today",
            description="Create your secure family profile in minutes. Free, open, and community governed.",
            cta_text="Create Free Account",
            cta_url="https://profile.triberaised.com",
            style="teal",
        )

        self.stdout.write("Scaffolded Solutions page plugins.")
        return page

    def _seed_contact_page(self, user):
        page, _ = self._get_or_create_page("Contact", "contact")
        ph = page.get_placeholders("en").filter(slot="content").first()
        if not ph:
            return page

        if ph.get_plugins().exists():
            self.stdout.write("Contact page already has plugins, skipping.")
            return page

        add_plugin(
            ph,
            "HeroBannerPlugin",
            "en",
            headline="Connect with TribeRaised",
            highlight_text="We Are Here to Listen",
            subheading="Have feedback, need accessibility accommodations, or interested in contributing to open source development? Reach out to our team.",
            badge_text="Support & Feedback",
            primary_cta_text="Community Forum Support",
            primary_cta_url="https://forum.triberaised.com",
            secondary_cta_text="Profile Hub Help",
            secondary_cta_url="https://profile.triberaised.com",
            background_gradient="amber_indigo",
        )

        add_plugin(
            ph,
            "CtaBannerPlugin",
            "en",
            headline="Join Our Open Community",
            description="Participate in discussions, request features, and help shape the future of sensory-friendly tools.",
            cta_text="Visit Community Forum",
            cta_url="https://forum.triberaised.com",
            style="night",
        )

        self.stdout.write("Scaffolded Contact page plugins.")
        return page
