from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.feed, name='feed'),
    path('create/', views.create, name='create'),
    path('<int:post_id>/delete/', views.delete, name='delete'),
    path('<int:post_id>/update/', views.update, name='update'),
    path('<int:post_id>/like/', views.like, name='like'),
    path('<int:post_id>/comment/create/', views.create_comment, name='create_comment'),
    path('<int:post_id>/comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]