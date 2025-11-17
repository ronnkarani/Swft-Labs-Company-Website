# models.py
from django.db import models
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import Truncator
from django.urls import reverse

# Hero Section
class Hero(models.Model):
    greeting =models.CharField(max_length=255, default="Hi 👋, welcome to")
    name = models.CharField(max_length=100)
    subtitle = RichTextUploadingField(max_length=1500, blank=True)
    image = models.ImageField(upload_to='hero/', blank=True, null=True)

    def __str__(self):
        return self.name

# About Section
class About(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextUploadingField()

    def __str__(self):
        return self.title
    

class OurStory(models.Model):
    title = models.CharField(max_length=255, default="Our Story")
    content = RichTextUploadingField()

    def __str__(self):
        return self.title


class WhyChooseUs(models.Model):
    title = models.CharField(max_length=255, default="Why Choose Us")
    points = RichTextUploadingField(help_text="Use bullet points or HTML list here")

    def __str__(self):
        return self.title

class Service(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    description = RichTextUploadingField()
    icon = models.CharField(max_length=50, help_text="Add emoji or icon code e.g., ⭐️, 💼, 🎖️")

    def __str__(self):
        return self.title

class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ("facebook", "Facebook"),
        ("twitter", "Twitter"),
        ("linkedin", "LinkedIn"),
        ("github", "GitHub"),
        ("instagram", "Instagram"),
        ("youtube", "YouTube"),
    ]

    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    url = models.URLField()

    def __str__(self):
        return f"{self.get_platform_display()} - {self.url}"


# Blog Category Model
class BlogCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# Project Category Model
class ProjectCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, null=True, blank=True)
    description = RichTextUploadingField()
    image = models.ImageField(upload_to='projects/')
    technologies = models.TextField()
    repo_url = models.URLField(blank=True, null=True)
    live_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)

    def get_absolute_url(self):
        return reverse("project_details", args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def tech_list(self):
        return [tech.strip() for tech in self.technologies.split(',')]
    
    def __str__(self):
        return self.title  

    def comment_count(self):
        return self.comments.count()

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    excerpt = models.TextField(blank=True)
    image = models.ImageField(upload_to='blogs/')
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True)
    content = RichTextUploadingField()    
    author = models.CharField(max_length=100, default="Ronny")
    created_at = models.DateField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)

    def get_absolute_url(self):
        return reverse("blog_detail", args=[self.slug])
    
    def save(self, *args, **kwargs):
        # Auto-generate slug if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Auto-generate excerpt from content (first 30 words by default)
        if not self.excerpt and self.content:
            self.excerpt = Truncator(self.content).words(30, truncate="...")

        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title
    
    def comment_count(self):
        return self.comments.count()

class Comment(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    # This will work for either a project or blog
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name="comments")
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE, null=True, blank=True, related_name="comments")

    def __str__(self):
        return f"Comment by {self.name}"

# FAQ Models
class FAQ(models.Model):
    question = models.CharField(max_length=255)

    def __str__(self):
        return self.question


class SubFAQ(models.Model):
    faq = models.ForeignKey(FAQ, on_delete=models.CASCADE, related_name='subquestions')
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return f"{self.question} (sub of {self.faq.question})"


# Testimonial Section
class Testimonial(models.Model):
    name = RichTextUploadingField(max_length=300)
    role = RichTextUploadingField(max_length=300, blank=True)
    content = RichTextUploadingField()
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    featured = models.BooleanField(default=False)
    rating = models.PositiveSmallIntegerField(default=5)


    def __str__(self):
        return self.name