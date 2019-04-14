from rest_framework import serializers
from user.models import User
from user.serializers import UserSerializer

from .models import Posts, Likes


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Posts
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Likes
        fields = ('user_id',)







