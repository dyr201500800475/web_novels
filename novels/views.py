from django.shortcuts import render
from django.core.paginator import Paginator
from django.conf import settings
from django.http import HttpResponse

from .models import NovelType, Novel, NovelInfo
from read_statistics.utils import read_statistics_once_read


def get_novels_common_data(request, novels_all_list):
	paginator = Paginator(novels_all_list, settings.EACH_PAGE_BLOGS_NUMBER)
	page_num = request.GET.get('page', 1) # 获取页码参数
	page_of_novels = paginator.get_page(page_num)  # get_page方法可以方式page_num参数无效
	current_page_num = page_of_novels.number  # 获取当前选中的页码
	# 获取显示页码的范围，当前页和前后各两页
	left_range = list(range(max(current_page_num - 2, 1), current_page_num))
	right_range = list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))
	page_range = left_range + right_range
	# 加上省略页标记
	if page_range[0] - 1 >= 2:
		page_range.insert(0, '...')
	if paginator.num_pages - page_range[-1] >= 2:
		page_range.append('...')
	# 加上首页和尾页
	if page_range[0] != 1:
		page_range.insert(0, 1)
	if page_range[-1] != paginator.num_pages:
		page_range.append(paginator.num_pages)
	
	novels_info = get_novels_info(page_of_novels.object_list)

	context = {}
	context['novels_info'] = novels_info
	context['page_of_novels'] = page_of_novels
	context['page_range'] = page_range
	return context

def get_novels_info(novels):
	novels_info = []
	for novel in novels:
		novel_info = NovelInfo.objects.get(novel=novel)
		novels_info.append(novel_info)
	return novels_info

def type(request, type_pk):
	novel_type = NovelType.objects.get(pk=type_pk)
	novels_all_list = Novel.objects.filter(novel_type=novel_type)
	context = get_novels_common_data(request, novels_all_list)
	context['novel_type'] = novel_type
	return render(request, "novels/novel_type.html", context)

def novel_detail(request, novel_pk):
	context = {}
	novel = Novel.objects.get(pk=novel_pk)
	novel_info = NovelInfo.objects.get(novel=novel)
	read_cookie_key = read_statistics_once_read(request, novel)

	context['novel'] = novel
	context['novel_info'] = novel_info
	context['novel_type'] = novel.novel_type
	response = render(request, "novels/novel_detail.html", context)
	response.set_cookie(read_cookie_key, 'true')
	return response