import threading

from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail

from .models import Comment

# 检测到保存动作发生，发送站内消息通知
@receiver(post_save, sender=Comment)
def send_notification(sender, instance, **kwargs):
	if not instance.reply_to is None:
		recipient = instance.reply_to
		verb = '{0}回复了你的评论"{1}"'.format(
				instance.user.get_nickname_or_username(),
			 	strip_tags(instance.parent.text)
			)
		url = instance.content_object.get_url() + "#comment_" + str(instance.pk)
		notify.send(instance.user, recipient=recipient, verb=verb, action_object=instance, url=url)

# 发送邮件线程
class SendMail(threading.Thread):
	def __init__(self, subject, text, email, fail_silently=False):
		self.subject = subject
		self.text = text
		self.email = email
		self.fail_silently = fail_silently
		threading.Thread.__init__(self)
	def run(self):
		send_mail(
            self.subject, 
            '',
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently=self.fail_silently,
            html_message=self.text
        )

@receiver(post_save, sender=Comment)
def send_email(sender, instance, **kwargs):
	if not instance.parent is None:
		subject = '有人回复了你的评论'  # 邮件主题
		email = instance.reply_to.email  # 收件人
		if email != '':
			# 邮件内容
			context = {}
			context['comment_text'] = instance.text
			context['url'] = instance.content_object.get_url()
			text = render_to_string('comment/send_mail.html', context)
			send_mail = SendMail(subject, text, email)
			send_mail.start()