# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns, include

from .views import *


urlpatterns = [
    url(r'^$', ChatView.as_view(), name='chats'),
    url(r'^(?P<room>\d+)/message/$', MessageView.as_view(), name='messages'),    
    url(r'^(?P<room>\d+)/send/$', SendMessageView.as_view(), name='send_message'),
]
