from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import CollectRecord

register = template.Library()


# 获取收藏状态
@register.simple_tag(takes_context=True)
def get_collect_status(context, obj):
	content_type = ContentType.objects.get_for_model(obj)
	user=context['user']
	if not user.is_authenticated:
		return ''
	if CollectRecord.objects.filter(content_type=content_type, object_id=obj.pk, user=user).exists():
		return 'active'
	else:
		return ''


# 返回收藏信息
@register.simple_tag(takes_context=True)
def get_collect_message(context, obj):
	content_type = ContentType.objects.get_for_model(obj)
	user=context['user']
	if not user.is_authenticated:
		return '加入书架+'
	if CollectRecord.objects.filter(content_type=content_type, object_id=obj.pk, user=user).exists():
		return '已收藏'
	else:
		return '加入书架+'