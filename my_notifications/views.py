from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from notifications.models import Notification

# 查看站内消息
def my_notifications(request):
	return render(request, 'my_notifications/my_notifications.html')

# 查看具体某一条消息，并把它标记为已读
def my_notification(request, my_notification_pk):
	my_notification = get_object_or_404(Notification, pk=my_notification_pk)
	my_notification.unread = False
	my_notification.save()
	return redirect(my_notification.data['url'])

# 删除全部已读消息
def delete_my_read_notifications(request):
	notifications = request.user.notifications.read()
	notifications.delete()
	return redirect(reverse('my_notifications:my_notifications'))