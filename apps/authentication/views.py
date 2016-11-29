from django.contrib.auth import authenticate, login, logout
from rest_framework import parsers, renderers, permissions, viewsets, status, views, exceptions
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from django.db import transaction

import json

from authentication.models import User
from authentication.serializers import AuthTokenSerializer, UserSerializer
from chat import settings
from chat.generics import *


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            User.objects.create_user(**serializer.validated_data)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad request',
            'message': 'User could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, username=None, **kwargs):
        """
        ---
        omit_serializer: True

        parameters:
        - name: body
          paramType: body
          description: '{"first_name":"","last_name":"", "password":"", "confirm_password":""}'
        """
        serializer = self.serializer_class(self.request.user, data=request.data, partial=True)
        if serializer.is_valid():
            isntance = self.get_object() 
            user = User.objects.update(isntance, request.data)
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({
            'status': 'Bad request',
            'message': 'User could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)

class LoginView(views.APIView):
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    authentication_classes = []
    api_view = ['POST']

    def post(self, request, format=None):
        """
        ** Login to portal using your credentials**

        ** It will Provide Authentication token to access secured APIs\
        if given username and password are matched in database.**
        ---
        request_serializer: AuthTokenSerializer
        omit_serializer: False

        type:
            token:
                required: true
                type: string

        consumes:
            - application/json

        produces:
            - application/json
        """
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = AuthToken.objects.create(user=user)
        return Response({'token': token})


class LogoutView(views.APIView):
    permission_classes = (IsAuthenticated, permissions.IsAuthenticated)
    authentication_classes = [TokenAuthentication]
    api_view = ['POST', ]

    def post(self, request, format=None):
        """
        ## Logout your User
        """
        request._auth.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)