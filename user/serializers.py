from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializers(serializers.ModelSerializer):
    model = User
    fields = (id, username , ema)

