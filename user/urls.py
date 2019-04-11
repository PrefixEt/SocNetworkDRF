from django.urls import path
from .views import CreateUsersAPIView, UserRetrieveUpdateAPIView, autentification_user

urlpatterns=[
    path('create/', CreateUsersAPIView.as_view()),
    path('update/', UserRetrieveUpdateAPIView.as_view()),
    path('obtain_token/', autentification_user) 
]