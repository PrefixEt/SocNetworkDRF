from django.urls import path
from .views import CreateUsersAPIView

urlpatterns=[
    path('create/', CreateUsersAPIView.as_view()),
]