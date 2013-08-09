from django.db import models
from django.contrib import admin
from kudosapp.models import Kudos, Employee

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name', 'dept', 'location', 'email')
    search_fields = ('first_name','last_name', 'dept', 'location', 'email')

class KudosAdmin(admin.ModelAdmin):
    list_display = ('subject', 'body', 'from_employee', 'to_employee', 'tags', 'created')
    search_fields = ('subject', 'body', 'from_employee', 'to_employee', 'tags', 'created')
    list_filter = ('flagged',)


admin.site.register(Kudos, KudosAdmin)
admin.site.register(Employee, EmployeeAdmin)
