from django import template
from ..models import NovelType

register = template.Library()

@register.simple_tag
def get_novel_type():
	return NovelType.objects.all()