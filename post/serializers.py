from rest_framework import serializers
from .models import Posts

class PostSerilyzer(serializers.Hyperlink):
    class Meta:
        model = Posts
        fields = '__all__'


