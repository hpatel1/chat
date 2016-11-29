from rest_framework.generics import GenericAPIView
from rest_framework import mixins, status
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chat.generics import *
from .models import *
from .serializers import *


class ChatView(GenericAPIView, mixins.ListModelMixin):
    serializer_class = ChatRoomSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return ChatRoom.objects.all().filter(users__in=[user])

    def get(self, request, *args, **kwargs):
        """
        Get list of chat happend till now.
        """
        return self.list(request, *args, **kwargs)
        # user.received_messages.all().values_list()


class MessageView(GenericAPIView, mixins.ListModelMixin):
    serializer_class = MessageSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    
    def get(self, request, room=None, *args, **kwargs):
        """
        Get list of chat happend till now.
        """
        messages = Message.objects.all().filter(room=room)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SendMessageView(GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def post(self, request, room=None):
        """
        Send message
        ---

        parameter_strategy : False

        parameters:
            - name: message
              type: string
              paramType: form
        """
        user = request.user
        data = dict()
        data['message'] = request.data.get('message', '')
        data['room'] = room
        data['from_user'] = user.id
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)