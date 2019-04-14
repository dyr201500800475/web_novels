from django.contrib import admin
from .models import NovelType

@admin.register(NovelType)
class NovelTypeAdmin(admin.ModelAdmin):
	list_display = ('id', 'type_name')
