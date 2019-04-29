from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from .views import UserAPIView, autentification_user


user_list = UserAPIView.as_view({
    'get': 'list',
    'post': 'create',
})


user_detail = UserAPIView.as_view({
    'get': 'retrieve', 
    'put':'update'  
})

urlpatterns=[
    path('user-manager', user_list, name='user-all'),
    path('user-manager', user_list, name='user-create'),
    path('user-manager/<int:pk>', user_detail, name='user-by-id'),    
    path('user-manager/<int:pk>', user_detail, name='user-update'),
    path('login', autentification_user, name='auth-login') 
]