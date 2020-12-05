from ResModel.models import HubUser
from django.http import HttpResponse, JsonResponse


def identity_check(request):
    uid = request.POST.get('userId')
    pwd = request.POST.get('password')
    u = HubUser.objects.filter(UserEmail=uid).filter(UserPassword=pwd)
    res = u.__len__() > 0
    return JsonResponse({'result': res})


def bandwidth_test(request):
    return JsonResponse({'result': '1111' * 1024*16})
