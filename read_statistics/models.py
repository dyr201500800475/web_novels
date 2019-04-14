from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

class ReadNum(models.Model):
	read_num = models.IntegerField(default=0)

	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')
	

class ReadNumExpandMethod():
	def get_read_num(self):
		content_type = ContentType.objects.get_for_model(self)
		try:
			readnum = ReadNum.objects.get(content_type=content_type, object_id=self.pk)
			return readnum.read_num
		except Exception as e:
			return 0

class ReadDetail(models.Model):
	date = models.DateField(default=timezone.now)
	read_num = models.IntegerField(default=0)

	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')