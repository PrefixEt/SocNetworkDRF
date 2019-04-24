from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from .views import UserAPIView, autentification_user

urlpatterns=[
    path('all/', UserAPIView.as_view({'get':'list'}), name='user-all'),
    path('id/<int:user_id>', UserAPIView.as_view({'get':'retrieve'}), name='user-by-id'),
    path('create/', UserAPIView.as_view({'post':'create'}), name='user-create'),
    path('id/<int:user_id>/update/', UserAPIView.as_view({'put':'update'}), name='user-update'),
    path('obtain_token/', autentification_user, name='auth-login') 
]