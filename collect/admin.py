from django.contrib import admin
from .models import CollectRecord

@admin.register(CollectRecord)
class CollectRecordAdmin(admin.ModelAdmin):
	list_display = ('id', 'content_object', 'user', 'collected_time')