# Create your views here.

from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from kudosapp.models import Kudos, Employee

def home(request):
    kudos_set = Kudos.objects.order_by("created")
    data = {}
    data['kudos_set'] = kudos_set
    return render_to_response('home.html', data, context_instance=RequestContext(request))
