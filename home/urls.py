from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [
    path("", views.index, name="home"),
    path("login", views.loginUser, name="login"),
    path("logout", views.logoutUser, name="logout"),
    path('signup', views.signup, name='signup'),
    path('create_encrypted_post', views.create_encrypted_post, name='create_encrypted_post'),
    path('view_encrypted_post', views.view_encrypted_post, name='view_encrypted_post'),
    path("about", views.about, name="about"),
    path("operators", views.operators, name="operators"),
    path("profile", views.profile, name="profile"),
    path("contact", views.contact, name="contact")
]
