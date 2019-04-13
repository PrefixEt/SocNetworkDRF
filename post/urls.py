from django.urls import path
from .views import CreatePost, post_like, get_all_posts, get_user_posts, get_post_by_id

urlpatterns=[
    path('all', get_all_posts, name='posts-all'),
    path('create/',  CreatePost.as_view(), name='post-create'),  
    path('user/<int:user_id>',  get_user_posts, name='user-post'), 
    path('id/<int:post_id>/', get_post_by_id, name='post-by-id'),
    path('id/<int:post_id>/like', post_like, name='post-like'),
    ]

    