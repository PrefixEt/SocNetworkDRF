from rest_framework import generics
from .models import Posts
from .serializers import PostSerilyzer



class ListPostView(generics.ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerilyzer



    