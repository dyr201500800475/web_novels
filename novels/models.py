from django.db import models
from django.urls import reverse
from read_statistics.models import ReadNumExpandMethod

# Create your models here.

class NovelType(models.Model):
	type_name = models.CharField(max_length=50)

	def __str__(self):
		return self.type_name 

class Novel(models.Model, ReadNumExpandMethod):
	novel_type = models.ForeignKey(NovelType, on_delete=models.CASCADE)
	novel_name = models.CharField(max_length=50)
	novel_url = models.CharField(max_length=255)

	def __str__(self):
		return "<Novel: %s>" % self.novel_name

	def get_url(self):
		return reverse('novels:novel_detail', kwargs={'novel_pk': self.pk})


class NovelInfo(models.Model):
	novel = models.ForeignKey(Novel, on_delete=models.CASCADE)
	author = models.CharField(max_length=50)
	image = models.CharField(max_length=255)
	state = models.CharField(max_length=20)
	description = models.TextField()
	last_update_time = models.CharField(max_length=255)
	read_url = models.CharField(max_length=255)