
from rest_framework import routers

from users import views

router = routers.DefaultRouter()

router.register(
    'me', views.UserAPIViewSet,
    basename='me',
)


urlpatterns = [] + router.urls
