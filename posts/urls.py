from django.urls import path
from django.urls import re_path
from . import  views



urlpatterns = [
    path('', views.home, name='home'),
    path('manage', views.manage, name='manage'),

    path('posts/create/', views.post_create, name='post_create'),
    path('blogs/<slug:slug>/', views.post_detail, name='post_detail'),
    path('posts/<int:id>/edit/', views.post_edit, name='post_edit'),
    path('posts/<int:id>/delete/', views.post_delete, name='post_delete'),

    path('post/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/add_reply/', views.add_reply, name='add_reply'),
    
    # re_path(r'^.*$', views.custom_404),
    # path("dj-admin", view)
]

