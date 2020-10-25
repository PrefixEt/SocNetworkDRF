from rest_framework import serializers
from users.models import User
from users.serializers import UserSerializer

from .models import Posts, Likes


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Posts
        fields = '__all__'


class UserInLikes(UserSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class LikeSerializer(serializers.ModelSerializer):
    user = UserInLikes(read_only=True)
    link = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-by-id', lookup_field='user_id')
    
    class Meta:
        model = Likes
        fields = ('user_id', 'user', 'link')







