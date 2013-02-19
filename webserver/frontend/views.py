# Create your views here.
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponseNotFound
import datetime
import hashlib
import json
import types
import controls
def statistic_all(request):
    return HttpResponse("hello world !")

def analysis_all(request):
    return HttpResponse("hello world !")

def statistic_market(request):
    return HttpResponse("hello world !")

def statistic_app(request):
    return HttpResponse("hello world !")

def statistic_game(request):
    return HttpResponse("hello world !")
