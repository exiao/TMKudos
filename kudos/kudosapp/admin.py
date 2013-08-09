from django.db import models
from django.contrib import admin
from kudosapp.models import Kudos, Employee

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name', 'dept', 'location', 'email')
    search_fields = ('first_name','last_name', 'dept', 'location', 'email')

class KudosAdmin(admin.Admin):
    list_display = ()

admin.site.register(Kudos)
admin.site.register(Employee, EmployeeAdmin)
