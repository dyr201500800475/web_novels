import random

from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from novels.models import Novel,NovelInfo,NovelType
from likes.models import LikeCount, LikeRecord

def get_novels_info(novels):
	novels_info = []
	for novel in novels:
		novel_info = NovelInfo.objects.get(novel=novel)
		novels_info.append(novel_info)
	return novels_info

def index(request):
	context = {}
	# 获取推荐小说信息
	start_id = random.randint(234, 2832)
	novels = Novel.objects.all().order_by("novel_name")[start_id:start_id + 12]
	novels_info = get_novels_info(novels)

	# 获取"精彩推荐"部分小说信息
	novels_types_info = []
	for i in range(1, 6):
		novel_type = NovelType.objects.get(pk=i)
		novels_with_type = Novel.objects.filter(novel_type=novel_type)[:6]
		novels_with_type_info = get_novels_info(novels_with_type)
		novels_types_info.append(novels_with_type_info)

	# 获取"最近更新"部分小说信息
	novels_last_update = NovelInfo.objects.all().order_by("-last_update_time")[:18]

	# 获取"点赞排行"部分小说信息
	content_type = ContentType.objects.get(model='novel')
	novels_like_list = LikeCount.objects.filter(content_type=content_type, liked_num__gt=0).order_by("-liked_num")[:18]
	
	context['novels_info'] = novels_info
	context['novels_types_info'] = novels_types_info
	context['novels_last_update'] = novels_last_update
	context['novels_like_list'] = novels_like_list
	return render(request, 'index.html', context)

def base(request):
	return render(request, 'base.html')