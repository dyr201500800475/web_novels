from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.urls import  reverse
from notifications.signals import notify

# 检测到点赞动作发生，发送站内消息通知
@receiver(post_save, sender=User)
def send_notification(sender, instance, **kwargs):
	if kwargs['created'] == True:
		verb = '注册成功，更多精彩小说等你发现...'
		url = reverse('user:user_info')
		notify.send(instance, recipient=instance, verb=verb, action_object=instance, url=url)