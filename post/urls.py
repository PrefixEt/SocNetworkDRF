from django.urls import path
from .views import ListPostView

urlspatterns=[
    path('all', ListPostView.as_view(), name='posts-all')

    ]