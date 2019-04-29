from django.shortcuts import get_object_or_404
from django.contrib.auth.signals import user_logged_in
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status,viewsets
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


class PostAPIView(viewsets.ViewSet):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        post = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        user = jwt.decode(request.auth, settings.SECRET_KEY)
        user_id = user['user_id']        
        serializer_data = request.data
        serializer_data.update({'user': user_id})
        serializer = self.serializer_class(data=serializer_data)
        serializer.is_valid(raise_exception=True)   
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action in ('update', 'create'):
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class UserPostApi(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    serializer_class = PostSerializer    

    def retrieve(self, user_id, request):
        queryset = Posts.objects.filter(user_id=user_id)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

   

#like/unlike funcrional
@api_view(['POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, ])
def post_like(request, post_id): 
    #only authenticated
    user_id = jwt.decode(request.auth, settings.SECRET_KEY)['user_id']
    try:
        post = Posts.objects.get(id=post_id)
    except ObjectDoesNotExist:
        return Response({'Error':'Not post by this id'}, status.HTTP_400_BAD_REQUEST)

    try:
        like = Likes.objects.get(user_id=user_id, post_id=post_id)        
    except ObjectDoesNotExist:
        like = None
        
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


@api_view(['GET'])
@permission_classes([AllowAny, ])
def get_likes_by_post_id(request, post_id):   
    likes = Likes.objects.filter(post_id=post_id)    
    if likes:        
        serializer = LikeSerializer(likes, many= True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({}, status=status.HTTP_200_OK)


