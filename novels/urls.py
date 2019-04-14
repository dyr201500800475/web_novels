from django.urls import path
from . import views

app_name = 'novels'

urlpatterns = [
    path('type<int:type_pk>/', views.type, name="type"),
    path('novel_detail<int:novel_pk>', views.novel_detail, name="novel_detail"),
]
