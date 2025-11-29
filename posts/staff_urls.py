from django.urls import path
from posts.views import staff_views

urlpatterns = [
    path("", staff_views.dashboard, name="staff_dashboard"),
    
    path('posts', staff_views.post_list, name='staff_posts'),
    path('posts/create/', staff_views.post_create, name='staff_post_create'),
    path('posts/<int:id>/edit/', staff_views.post_edit, name='staff_post_edit'),
    path('posts/<int:id>/delete/', staff_views.post_delete, name='staff_post_delete'),
    
    # path("posts/", staff_views.post_list, name="staff_post_list"),
    # path("posts/create/", staff_views.post_create, name="staff_post_create"),
    # path("posts/<int:id>/edit/", staff_views.post_edit, name="staff_post_edit"),
    
    path('categories', staff_views.categories, name="staff_categories"),
    path('categories/create/', staff_views.create_category, name="create_category"),
    path('categories/<int:id>/edit/', staff_views.edit_category, name="edit_category"),
    path('categories/<int:id>/delete/', staff_views.delete_category, name="delete_category"),
    
    path('comments', staff_views.comment_list, name='staff_comments'),
    path('comments/<int:id>/delete/', staff_views.comment_delete, name='staff_comment_delete'),

    path("users/", staff_views.user_list, name="staff_user_list"),
    path("users/create/", staff_views.user_create, name="staff_user_create"),
    path("users/<int:id>/edit/", staff_views.user_edit, name="staff_user_edit"),
    path("users/<int:id>/delete/", staff_views.user_delete, name="staff_user_delete"),
    
]
