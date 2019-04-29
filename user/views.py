from django.shortcuts import render, get_object_or_404
from django.contrib.auth.signals import user_logged_in
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
from rest_framework_jwt.utils import jwt_payload_handler, jwt
from api import settings
from .serializers import UserSerializer
from .models import User


class UserAPIView(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, user_id=None, pk=None): 
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

    def update(self, request, user_id=None, pk=None):
        serializer_data = request.data.get('user', {})
 
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save() 
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get_permissions(self):
        if self.action == 'update':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


@api_view(['POST'])
@permission_classes([AllowAny, ])
def autentification_user(request): 
    try:
        email = request.data['email']
        password = request.data['password']
        try:
            user = User.objects.get(email=email, password=password)    
        except ObjectDoesNotExist:
            user=None
        if user:
            try:
                payload = jwt_payload_handler(user)
                token = jwt.encode(payload, settings.SECRET_KEY)
                user_details = {
                    'name': '%s %s' % (user.first_name, user.last_name),
                    'token': token
                }
                user_logged_in.send(sender=user.__class__, request=request, user=user)
                return Response(user_details, status=status.HTTP_200_OK)
            except Exception as e:
                raise e
        else:
            res={'error':'can not authenticate'}
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)
    except KeyError:
        res ={'error':'please provide a email and a password'}
        return Response(res)
