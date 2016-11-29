# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns, include
from django.core.urlresolvers import reverse_lazy
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView
from django.contrib import admin
from django.conf.urls.static import static

# from .views import BroadcastChatView, UserChatView, GroupChatView
from authentication.views import *
from .views import index
from rest_framework import routers
import settings

admin.autodiscover()

router = routers.SimpleRouter()
router.register(r'user', UserViewSet)

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [    

    url(r'^admin/', include(admin.site.urls)),

    # Browseable Interactive API documentation
    url(r'^docs/', include('rest_framework_swagger.urls')),

    url(r'^$', index, name='index'),
    
    url(r'^api/v1/auth/login/$', LoginView.as_view(), name='login'),
    url(r'^api/v1/auth/logout/$', LogoutView.as_view(), name='logout'),

    # Chat related Urls
    url(r'^api/v1/chat/', include('messaging.urls')),
]

from messaging import consumers

channel_routing = {
    "websocket.connect": consumers.ws_connect,    
    "websocket.disconnect": consumers.ws_disconnect,
}