from django.urls import path
from .views import CreateUsersAPIView, UserRetrieveUpdateAPIView, autentification_user, get_user

urlpatterns=[
    path('all/', get_user, name='user-all'),
    path('id/<int:user_id>', get_user, name='user-by-id'),
    path('create/', CreateUsersAPIView.as_view()),
    path('update/', UserRetrieveUpdateAPIView.as_view()),
    path('obtain_token/', autentification_user, name='auth-login') 
]