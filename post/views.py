from rest_framework import generics
from .models import Posts
from .serializers import PostSerilyzer



class ListPostView(generics.ListAPIView):
    
    serializer_class = PostSerilyzer

    def get_queryset(self):
        queryset = Posts.objects.all()
        if self.kwargs['user_id']:
            user_id = self.kwargs['user_id']
            queryset = queryset.filter(post__user_id=user_id)
        return queryset


