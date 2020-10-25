
from django.urls import path
from rest_auth import views as rest_auth_views
from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token

urlpatterns = [

    path(
        'login/',
        rest_auth_views.LoginView.as_view(),
        name='rest_login',
    ),

    path('token/refresh/', refresh_jwt_token),
    path('token/verify/', verify_jwt_token),

    path(
        'logout/',
        rest_auth_views.LogoutView.as_view(),
        name='rest_logout',
    ),
    path(
        'password/change/',
        rest_auth_views.PasswordChangeView.as_view(),
        name='rest_password_change',
    ),
    path(
        'password/reset/',
        rest_auth_views.PasswordResetView.as_view(),
        name='rest_password_reset',
    ),
    path(
        'password/reset/confirm/',
        rest_auth_views.PasswordResetConfirmView.as_view(),
        name='rest_password_reset_confirm',
    ),
]

