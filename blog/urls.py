from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('postComment', views.postComment, name='postComment'), # API to post a comment
    path('', views.blogHome, name='blogHome'),
    path('<str:slug>', views.blogPost, name='blogPost'),
]
