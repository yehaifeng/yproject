# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
import datetime

# Create your views here.
def index(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    #return HttpResponse(html)
    return render(request, 'base.html')
