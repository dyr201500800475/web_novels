from django.contrib import admin
from .models import ReadNum, ReadDetail

@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
	list_display = ('content_object', 'read_num')

@admin.register(ReadDetail)
class ReadDetailAdmin(admin.ModelAdmin):
	list_display = ('content_object', 'read_num', 'date')