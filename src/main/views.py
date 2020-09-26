from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.http import HttpResponse, Http404, JsonResponse
from django.db import connection, connections
from django.db.utils import OperationalError
from django.utils import timezone

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from django.utils import timezone

from rest_framework import routers, serializers, viewsets, status
from rest_framework.response import Response
from datetime import datetime
import json, urllib, os, time

import xsetting.util as util


def index(request):
  return render(request, 'main/index.html', locals())
