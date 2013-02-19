# Create your views here.
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseRedirect
import datetime
import hashlib
import json
import types
import controls

def app(request,package):
    return HttpResponse("api")

def market(request,market):
    return HttpResponse("api")

def all(request):
    return HttpResponse("api")

