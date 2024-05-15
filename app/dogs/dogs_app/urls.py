#from django.shortcuts import url
from django.urls import path
from . import views

urlpatterns= [
    path("", views.home, name='home'),
    path("todos/", views.todos, name="Todos"),
    path("about/", views.about, name="about"),
    path("home/", views.home, name="home"),
    path("contact/", views.contact, name="contact"),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login')

]