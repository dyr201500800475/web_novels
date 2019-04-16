from django.shortcuts import render

from novels.models import Novel, NovelInfo
from novels.views import get_novels_common_data

def get_novel_info_by_author(keywords):
	novels_list = []
	novels_info = NovelInfo.objects.filter(author__contains=keywords)
	for novel_info in novels_info:
		novels_list.append(novel_info.novel)
	return novels_list

def search(request):
	context = {}
	keywords = request.GET.get('search_content', '')
	print(request.GET)
	if keywords != '':
		if Novel.objects.filter(novel_name__contains=keywords).exists():
			novels_list = Novel.objects.filter(novel_name__contains=keywords)
			context = get_novels_common_data(request, novels_list)
		elif NovelInfo.objects.filter(author__contains=keywords).exists():
			novels_list = get_novel_info_by_author(keywords)
			context = get_novels_common_data(request, novels_list)
		else:
			context = {}
	context['keywords'] = keywords
	context['url'] = "/search/?search_content=%s" % keywords
	return render(request, 'search/search.html', context)
