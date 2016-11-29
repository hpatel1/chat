from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from .models import User

admin.site.register(User)