from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist
from .models import CollectRecord


# 返回正确操作的JSON数据
def SuccessResponse():
    data = {}
    data['status'] = 'SUCCESS'
    return JsonResponse(data)


# 返回错误操作的JSON数据
def ErrorResponse(code, message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)


# 收藏操作逻辑函数
def collect_change(request):
    # 获取数据
    user = request.user
    # 如果用户没有登录
    if not user.is_authenticated:
        return ErrorResponse(400, '您还没有登录')

    content_type = request.GET.get('content_type')
    object_id = request.GET.get('object_id')

    try:
        # 获取要收藏的对象
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return ErrorResponse(401, '点赞对象不存在')

    # 判断是否已经收藏过
    is_collect = request.GET.get('is_collect')

    # 如果还没有收藏过
    if is_collect == 'true':
        # 要进行收藏，检查是否有收藏记录
        collect_record, created = CollectRecord.objects.get_or_create(content_type=content_type,
                                                                      object_id=object_id,
                                                                      user=user)
        if created:
            # 刚创建好收藏记录
            return SuccessResponse()
        else:
            # 已经收藏过，不能重复收藏
            return ErrorResponse(402, '不能重复收藏')
        # 取消收藏
    else:
        # 如果存在收藏记录，则删除这条记录
        if CollectRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            collect_record = CollectRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
            collect_record.delete()
            return SuccessResponse()
        # 如果不存在收藏记录，则返回错误
        else:
            return ErrorResponse(403, '还没有收藏过，不能取消')



def my_collects(request):
    context = {}
    user = request.user
    collect_records = CollectRecord.objects.filter(user=user).order_by("-collected_time")
    context['collect_records'] = collect_records
    return render(request, 'collect/my_collects.html', context)

def delete_collect(request, collect_pk):
    if CollectRecord.objects.filter(pk=collect_pk).exists():
        collect_record = CollectRecord.objects.get(pk=collect_pk)
        collect_record.delete()
        return redirect('collect:my_collects')