#from django.shortcuts import url
from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from django.contrib.auth import views as auth_views

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
]