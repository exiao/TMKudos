from django.db import models
from django.contrib import admin
from kudosapp.models import Kudos, Employee

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name', 'dept', 'location', 'email')
    search_fields = ('first_name','last_name', 'dept', 'location', 'email')

class KudosAdmin(admin.ModelAdmin):
    list_display = ('from_employee', 'to_employee', 'subject', 'body', 'tags', 'created')
    search_fields = ('from_employee', 'to_employee', 'subject', 'body', 'tags', 'created')

admin.site.register(Kudos, KudosAdmin)
admin.site.register(Employee, EmployeeAdmin)
