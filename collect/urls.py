from django.urls import path
from . import views

app_name = "collect"

urlpatterns = [
	path('collect_change/', views.collect_change, name="collect_change"),
	path('my_collects/', views.my_collects, name="my_collects"),
	path('delete_collect<int:collect_pk>', views.delete_collect, name="delete_collect"),
]