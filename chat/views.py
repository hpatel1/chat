# -*- coding: utf-8 -*-
from django.shortcuts import render

from authentication.models import User


def index(request):
    return render(request, 'index.html', {'user': User.objects.all()[0]})