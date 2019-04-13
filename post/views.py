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
from .models import Posts, Likes
from user.models import User
from .serializers import PostSerilyzer



@api_view(['GET'])
@permission_classes([AllowAny, ])
def get_all_posts(request):
    try:
        posts = Posts.objects.all()
        serializer = PostSerilyzer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        Response({'Exception': str(e)})

@api_view(['GET'])
@permission_classes([AllowAny, ])
def get_user_posts(request, user_id):
    posts = Posts.objects.filter(user_id=user_id)
    if posts:
       serializer = PostSerilyzer(posts, many=True)
       return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'error':'No posts by this user_id'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([AllowAny, ])
def get_post_by_id(request, post_id):
    post = Posts.objects.get(id=post_id)
    if post:        
        serializer = PostSerilyzer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'error':'No posts by this id'}, status=status.HTTP_404_NOT_FOUND)

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
   


@api_view(['POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, ])
def post_like(request, post_id): 
    user_id = jwt.decode(request.auth, settings.SECRET_KEY)['user_id']
    like = Likes.objects.get(user_id=user_id, post_id=post_id)
    if like:
        like.delete()
        Response({'Unlike':
        {'user_id':user_id,'post_id':post_id}
        })
    else:
        like = Likes(user_id=user_id, post_id=post_id)
        like.save()
        Response({'Like':
        {'user_id':user_id,'post_id':post_id}
        })
