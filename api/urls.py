"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_auth.registration.views import SocialAccountListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/authentication/', include('users.authentication_urls')),

    path('api/v1/social_authentication/social_accounts/', SocialAccountListView.as_view(), name='socialaccount_signup'),
    path('api/v1/social_authentication/', include('users.social_accounts_urls')),

    path('api/v1/registration/', include('rest_auth.registration.urls')),

    path('api/v1/users/', include('users.urls')),
    path('api/v1/posts/', include('posts.urls'))
]
