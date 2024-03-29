from django.contrib import admin

from .models import Statement, Response

'''
This file is admin.py file:
    models should be register here to easy manage in
    http://localhost:8000/admin
    
'''

class StatementAdmin(admin.ModelAdmin):
    list_display = ('text', )
    list_filter = ('text', )
    search_fields = ('text', )

class ResponseAdmin(admin.ModelAdmin):
    list_display = ('statement', 'response', )
    search_fields = ['statement__text', 'response']

admin.site.register(Statement, StatementAdmin)
admin.site.register(Response, ResponseAdmin)
