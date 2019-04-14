import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from .models import ReadNum, ReadDetail

def read_statistics_once_read(request, obj):
	ct = ContentType.objects.get_for_model(obj)
	key = "%s_%s_read" % (ct.model, obj.pk)
	if not request.COOKIES.get(key):
		# 某一博客阅读数+1
		readNum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
		readNum.read_num += 1
		readNum.save()

		# 当天访问量+1
		date = timezone.now().date()
		readDetail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
		readDetail.read_num += 1
		readDetail.save()
	return key

# 分别获取前一周的访问量
def get_seven_days_read_data(content_type):
	today = timezone.now().date()
	dates = []
	read_nums = []
	for i in range(7, 0, -1):
		date = today - datetime.timedelta(days=i)
		dates.append(date.strftime('%m-%d'))
		read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
		result = read_details.aggregate(read_num_sum=Sum('read_num'))
		read_nums.append(result['read_num_sum'] or 0)
	return dates, read_nums
