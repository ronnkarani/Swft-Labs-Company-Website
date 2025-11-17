from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', next_page='home'), name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('projects/', views.projects, name='projects'),
    path('projects/<slug:slug>/', views.project_detail, name='project_details'),
    path("suggestions/", views.suggestions, name="suggestions"),
    path('add-testimonial/', views.add_testimonial, name='add_testimonial'),
    path('contact/', views.contact, name='contact'),
]