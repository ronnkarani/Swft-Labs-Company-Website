# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import FAQ, Project, BlogPost, Comment, SocialLink, Hero, About, Testimonial, Service, OurStory, WhyChooseUs, BlogCategory, ProjectCategory
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def home(request):
    hero = Hero.objects.first()
    about = About.objects.all()
    our_story = OurStory.objects.first()
    why_choose = WhyChooseUs.objects.first()
    testimonials = Testimonial.objects.filter(featured=True)
    social_links = SocialLink.objects.all()
    services = Service.objects.all()
    projects = Project.objects.all().order_by('-created_at')[:4]
    blogs = BlogPost.objects.all().order_by('-created_at')[:4]
    blog_categories = BlogCategory.objects.all()
    project_categories = ProjectCategory.objects.all()

    pending_testimonials = 0
    if request.user.is_authenticated and request.user.is_staff:
        pending_testimonials = Testimonial.objects.filter(featured=False).count()

    # NEW: check if logged-in user has already submitted a testimonial
    has_testimonial = False
    if request.user.is_authenticated:
        has_testimonial = Testimonial.objects.filter(name=request.user.username).exists()

    return render(request, 'home.html', {
        'hero': hero,
        'about_sections': about,
        'our_story': our_story,
        'why_choose': why_choose,
        'services': services,
        'testimonials': testimonials,
        'social_links': social_links,
        'projects': projects,
        'blog_posts': blogs,
        'blog_categories': blog_categories,
        'project_categories': project_categories,
        'pending_testimonials': pending_testimonials,
        'has_testimonial': has_testimonial,  # 👈 ADDED
    })


def blog(request):
    category_slug = request.GET.get('category')
    query = request.GET.get('q')

    posts = BlogPost.objects.all().order_by('-created_at')

    # Filter by category
    if category_slug and category_slug != "all":
        posts = posts.filter(category__slug=category_slug)

    # Filter by search
    if query:
        posts = posts.filter(title__icontains=query)

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = BlogCategory.objects.all()

    return render(request, 'blog.html', {
        'blog_posts': page_obj,
        'categories': categories,
        'selected_category': category_slug,
        'query': query,
    })

def blog_detail(request, slug):
    blog = get_object_or_404(BlogPost, slug=slug)
    blog.views += 1
    blog.save()

    if request.method == "POST":
        if "like" in request.POST:
            blog.likes += 1
            blog.save()
            return redirect('blog_detail', slug=slug)

        elif "comment" in request.POST:
            name = request.POST.get("name")
            content = request.POST.get("content")
            if name and content:
                Comment.objects.create(name=name, content=content, blog=blog)
            return redirect('blog_detail', slug=slug)

    comments = blog.comments.all()
    return render(request, 'blog_details.html', {
        'post': blog,
        'comments': comments
    })

def projects(request):
    category_slug = request.GET.get('category')
    query = request.GET.get('q')

    projects = Project.objects.all().order_by('-created_at')

    # Filter by category
    if category_slug and category_slug != "all":
        projects = projects.filter(category__slug=category_slug)

    # Filter by search
    if query:
        projects = projects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    # Pagination
    paginator = Paginator(projects, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = ProjectCategory.objects.all()

    return render(request, 'projects.html', {
        'projects': page_obj,
        'categories': categories,
        'selected_category': category_slug,
        'query': query,
    })

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    project.views += 1
    project.save()

    if request.method == "POST":
        if "like" in request.POST:
            project.likes += 1
            project.save()
            return redirect('project_details', slug=slug)

        elif "comment" in request.POST:
            name = request.POST.get("name")
            content = request.POST.get("content")
            if name and content:
                Comment.objects.create(name=name, content=content, project=project)
            return redirect('project_details', slug=slug)

    comments = project.comments.all()
    return render(request, 'project_details.html', {
        'project': project,
        'comments': comments
    })

def suggestions(request):
    query = request.GET.get("q", "")
    type = request.GET.get("type", "")

    results = []

    if type == "blog":
        posts = BlogPost.objects.filter(title__icontains=query)[:5]
        results = [{"title": p.title, "url": p.get_absolute_url()} for p in posts]

    if type == "project":
        projects = Project.objects.filter(title__icontains=query)[:5]
        results = [{"title": p.title, "url": p.get_absolute_url()} for p in projects]

    return JsonResponse({"results": results})

def faqs(request):
    faq_list = FAQ.objects.all().order_by('id')
    paginator = Paginator(faq_list, 10)  # Show 10 FAQs per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "faqs.html", {"faqs": page_obj})


def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "🎉 Account created successfully! You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "❌ Something went wrong. Please check the form.")
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})

def contact(request):
    social_links = SocialLink.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        subject = f"New Contact Form Submission from {name}"
        body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        try:
            send_mail(
                subject,
                body,
                settings.EMAIL_HOST_USER,  # sender
                [settings.EMAIL_HOST_USER],  # receiver (your email)
                fail_silently=False,
            )
            messages.success(request, "✅ Your message has been sent successfully!")
        except Exception as e:
            messages.error(request, f"❌ Error sending message: {e}")

        return redirect("contact")

    return render(request, "contact.html",{"social_links": social_links,})


@login_required
def add_testimonial(request):
    if request.method == "POST":
        name = request.POST.get("name")
        role = request.POST.get("role")
        content = request.POST.get("content")
        rating = int(request.POST.get("rating", 5))
        image = request.FILES.get("image")

        Testimonial.objects.create(
            name=name,
            role=role,
            content=content,
            rating=rating,
            image=image
        )
        messages.success(request, "✅ Testimonial submitted! Wait for admin approval.")
        return redirect("home")
    return redirect("home")

# Messages for successful login
def on_login(sender, request, user, **kwargs):
    from django.contrib import messages
    messages.success(request, f"👋 Welcome back, {user.username}!")

user_logged_in.connect(on_login)

# Messages for failed login
def on_login_fail(sender, credentials, request, **kwargs):
    from django.contrib import messages
    messages.error(request, "❌ Incorrect username or password.")

user_login_failed.connect(on_login_fail)

# Messages for logout
def on_logout(sender, request, user, **kwargs):
    from django.contrib import messages
    messages.info(request, "👋 You have been logged out successfully.")

user_logged_out.connect(on_logout)