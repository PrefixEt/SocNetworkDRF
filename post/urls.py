from django.urls import path
from .views import UserPostApi, PostAPIView, post_like, get_likes_by_post_id

urlpatterns=[
    path('all/', PostAPIView.as_view({'get':'list'}), name='posts-all'),
    path('create/',  PostAPIView.as_view({'post':'create'}), name='post-create'),  
    path('id/<int:post_id>/', PostAPIView.as_view({'get':'retrieve'}), name='post-by-id'),
    path('user/<int:user_id>/',  UserPostApi.as_view({'get':'retrieve'}), name='user-post'), 
    path('id/<int:post_id>/like/', post_like, name='post-like'),
    path('id/<int:post_id>/likes_list/', get_likes_by_post_id, name='post-like-list'),
    ]

    