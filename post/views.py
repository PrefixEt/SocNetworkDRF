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
from .serializers import PostSerializer, LikeSerializer


#simple functions for posts
@api_view(['GET'])
@permission_classes([AllowAny, ])
def get_all_posts(request):
    try:
        posts = Posts.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        Response({'Exception': str(e)})

@api_view(['GET'])
@permission_classes([AllowAny, ])
def get_user_posts(request, user_id):
    posts = Posts.objects.filter(user_id=user_id)
    if posts:
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'error':'No posts by this user_id'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([AllowAny, ])
def get_post_by_id(request, post_id):
    try:
        post = Posts.objects.get(id=post_id)
    except:
        post = None
  
    if post:        
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'error':'No posts by this id'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([AllowAny, ])
def get_likes_by_post_id(request, post_id):   
    likes = Likes.objects.filter(post_id=post_id)    
    if likes:        
        serializer = LikeSerializer(likes, many= True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({}, status=status.HTTP_200_OK)



#class for create posts
class CreatePost(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer
    

    def post(self, request):
        user = jwt.decode(request.auth, settings.SECRET_KEY)
        user_id = user['user_id']        
        serializer_data = request.data
        serializer_data.update({'user': user_id})
        serializer = PostSerializer(data=serializer_data)
        serializer.is_valid(raise_exception=True)   
        serializer.save()
        return Response(serializer.data)
   

#like/unlike funcrional
@api_view(['POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, ])
def post_like(request, post_id): 
    user_id = jwt.decode(request.auth, settings.SECRET_KEY)['user_id']
    try:
        post = Posts.objects.get(id=post_id)
    except:
        post= None
    try:
        like = Likes.objects.get(user_id=user_id, post_id=post_id)
        
    except:
        like = None
    if not post:
        return Response({'Error':'Not post by this id'})
    if like:
        like.delete()
        return Response({'Unlike':
        {'user_id':user_id,'post_id':post_id}
        })
    else:
        like = Likes(user_id=user_id, post_id=post_id)
        like.save()
        return Response({'Like':
        {'user_id':user_id,'post_id':post_id}
        })


