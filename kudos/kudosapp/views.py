# Create your views here.

from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404


def home(request):
    y = 7
    data = {}
    data['y'] = y
    return render_to_response('home.html', data, context_instance=RequestContext(request))
