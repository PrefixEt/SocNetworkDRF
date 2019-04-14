from django.urls import path
from .views import CreateUsersAPIView, UserRetrieveUpdateAPIView, autentification_user, test_get_all_users

urlpatterns=[
    path('all/', test_get_all_users, name='user-all'),
    path('create/', CreateUsersAPIView.as_view()),
    path('update/', UserRetrieveUpdateAPIView.as_view()),
    path('obtain_token/', autentification_user, name='auth-login') 
]