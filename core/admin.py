from django.contrib import admin
from django.utils.html import strip_tags
from .models import (
    Project, BlogPost, SocialLink, Hero, About, Testimonial,
    Service, OurStory, WhyChooseUs, BlogCategory, ProjectCategory
)

# Helper to strip HTML safely in list display
def clean_text(text):
    return strip_tags(text)[:80] + ("..." if len(strip_tags(text)) > 80 else "")


# --------------------------
# HERO ADMIN
# --------------------------
@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ('name', 'clean_greeting', 'clean_subtitle')

    def clean_greeting(self, obj):
        return clean_text(obj.greeting)
    clean_greeting.short_description = "Greeting"

    def clean_subtitle(self, obj):
        return clean_text(obj.subtitle)
    clean_subtitle.short_description = "Subtitle"


# --------------------------
# ABOUT ADMIN
# --------------------------
@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('title',)


# --------------------------
# OUR STORY ADMIN
# --------------------------
@admin.register(OurStory)
class OurStoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'clean_content')

    def clean_content(self, obj):
        return clean_text(obj.content)
    clean_content.short_description = "Content"


# --------------------------
# WHY CHOOSE US ADMIN
# --------------------------
@admin.register(WhyChooseUs)
class WhyChooseUsAdmin(admin.ModelAdmin):
    list_display = ('title', 'clean_points')

    def clean_points(self, obj):
        return clean_text(obj.points)
    clean_points.short_description = "Points"


# --------------------------
# SERVICES ADMIN
# --------------------------
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "subtitle", "clean_description")
    search_fields = ("title", "subtitle", "description")

    def clean_description(self, obj):
        return clean_text(obj.description)
    clean_description.short_description = "Description"


# --------------------------
# TESTIMONIAL ADMIN
# --------------------------
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('clean_name', 'clean_role', 'clean_content', 'featured', 'rating')
    list_filter = ('featured', 'rating')
    search_fields = ('name', 'role', 'content')

    def clean_name(self, obj):
        """Strip HTML from name"""
        text = strip_tags(obj.name)
        return text
    clean_name.short_description = "Name"

    def clean_role(self, obj):
        """Strip HTML from role"""
        text = strip_tags(obj.role)
        return text
    clean_role.short_description = "Role"

    def clean_content(self, obj):
        """Strip HTML from content and truncate for display"""
        text = strip_tags(obj.content)
        return text[:80] + ("..." if len(text) > 80 else "")
    clean_content.short_description = "Content"
# --------------------------
# SOCIAL LINK ADMIN
# --------------------------
@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("platform", "url")


# --------------------------
# BLOG CATEGORY ADMIN
# --------------------------
@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug")


# --------------------------
# PROJECT CATEGORY ADMIN
# --------------------------
@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug")


# --------------------------
# BLOG POST ADMIN
# --------------------------
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "category", "created_at")
    list_filter = ("category",)


# --------------------------
# PROJECT ADMIN
# --------------------------
admin.site.register(Project)
