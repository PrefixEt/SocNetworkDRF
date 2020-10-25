from django.urls import path
from .views import UserPostApi, PostAPIView, post_like, get_likes_by_post_id


post_list = PostAPIView.as_view({
    'get': 'list',
    'post': 'create',
})

post_detail = PostAPIView.as_view({'get':'retrieve'})


urlpatterns=[
    path('post_manager', post_list, name='posts-all'),
    path('post_manager',  post_list, name='post-create'),  
    path('post_manager/id/<int:pk>', post_detail, name='post-by-id'),
    path('user_id/<int:user_id>',  UserPostApi.as_view({'get':'retrieve'}), name='user-post'), 
    path('post_manager/id/<int:post_id>/like', post_like, name='post-like'),
    path('likes_list/<int:post_id>', get_likes_by_post_id, name='post-like-list'),
    ]

    