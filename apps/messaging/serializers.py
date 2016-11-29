from django.contrib.auth import update_session_auth_hash, authenticate
from rest_framework import serializers, exceptions
from django.utils.translation import ugettext_lazy as _

from .models import *
from chat.serializers import DynamicFieldsModelSerializer

class ChatRoomSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = ChatRoom
        depth = 1


class MessageSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Message

    def create(self, validated_data):
        print validated_data
        return Message.objects.create(**validated_data)