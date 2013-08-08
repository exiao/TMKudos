from django.db import models
from django.contrib import admin
from kudosapp.models import Kudos, Employee

admin.site.register(Kudos)
admin.site.register(Employee)
