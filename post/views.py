from rest_framework import generics
from django.http import Http404
from django.shortcuts import get_object_or_404
from .models import Posts
from .serializers import PostSerilyzer



class ListPostView(generics.ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerilyzer



class ListPostUsers(generics.ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerilyzer

    def get_object(self):
        queryset=self.filter_queryset(self.get_queryset())
        if 'user_id' in self.request.query_params:
            filter_kwargs={'id': self.request.query_params['user_id']}
        else:
            raise Http404('Missing required parameters')

        obj=get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, obj)

        return obj
        
