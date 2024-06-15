#from django.shortcuts import url
from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns= [
    path("", views.home, name='home'),
    path("todos/", views.todos, name="Todos"),
    path("about/", views.about, name="about"),
    path("home/", views.home, name="home"),
    path("contact/", views.contact, name="contact"),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.custom_login, name='login'),
    path('accounts/logout/', views.logout, name='logout'),
    path("entries/", views.entries, name="entries"),
    #path('make_post/', views.make_post, name='make_post'),
    path('post_success/', views.post_success, name='post_success'),
    path('posts/', views.posts, name='posts'),
    
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)