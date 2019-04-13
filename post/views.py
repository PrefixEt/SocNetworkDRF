from django.shortcuts import render
from django.contrib.auth.signals import user_logged_in
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
from rest_framework_jwt.utils import jwt_payload_handler, jwt
from rest_framework.generics import RetrieveUpdateAPIView
from api import settings
from .models import Posts
from user.models import User
from .serializers import PostSerilyzer



class ListPostView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = PostSerilyzer

    def get(self):
        queryset = Posts.objects.all()        
        if self.kwargs['user_id']:
            user_id = self.kwargs['user_id']
            queryset = queryset.filter(post__user_id=user_id)
        
        queryset = [post for post in queryset]
        return Response(queryset)
    




class CreatePost(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerilyzer
    

    def post(self, request):
        user = jwt.decode(request.auth, settings.SECRET_KEY)
        user_id = user['user_id']
        
        serializer_data = request.data
        serializer_data.update({'user': user_id})
        serializer = PostSerilyzer(data=serializer_data)
        serializer.is_valid(raise_exception=True)   
        serializer.save()
        return Response(serializer.data)
   