from django.urls import path
from .views import ListPostView

urlpatterns=[
    path('all', ListPostView.as_view(), name='posts-all'),
    path('user/<int:user_id>',  ListPostView.as_view(), name='user-post')    
    ]

    