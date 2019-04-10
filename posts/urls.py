from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('create/', views.create, name='create'),
    path('', views.feed, name='feed'),
]