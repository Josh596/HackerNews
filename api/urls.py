from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.getPost),
    path('post/create', views.addPost),
    path('post/update', views.updatePost),
    path('post/delete', views.deletePost),
]