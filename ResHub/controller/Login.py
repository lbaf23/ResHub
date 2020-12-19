import json

from ResModel.models import HubUser
from django.http import HttpResponse, JsonResponse
from ResHub.redispool import r
from ResHub.sendMail import send_email
def identity_check(request):
    uid = request.POST.get('userId')
    pwd = request.POST.get('password')
    u = HubUser.objects.filter(UserEmail=uid).filter(UserPassword=pwd)
    res = u.__len__() > 0
    return JsonResponse({'result': res})


def bandwidth_test(request):
    return JsonResponse({'result': '1111' * 1024*16})

def register(request):
    name = request.POST.get('userName')
    pwd = request.POST.get('password')
    address = request.POST.get('mailAddress')
    description = request.POST.get('userDescription')
    result = True
    u=HubUser.objects.filter(UserEmail=address)
    if(len(u)==0 and address!=None):
        user = HubUser(UserEmail=address,UserIntroduction=description,UserPassword=pwd,UserName=name)
        user.save()
    else:
        result=False
    return JsonResponse({'result':result})

def verification(request):
    email = request.GET.get('mailAddress')
    code = request.GET.get('verificationCode')
    result = True
    correct = r.get(email)
    print(email)
    print(correct)
    if(code==correct):
        return JsonResponse({'result':result})
    else:
        result=False
        return JsonResponse({'result':result})


def passwordLost(request):
    if request.method == "GET":
        UserEmail = request.GET.get('mailAddress')
        if UserEmail is not None:
            send_email(UserEmail)
            return JsonResponse({
                "status": 1,
                "message": "发送验证码成功",
            }, safe=False)
        else:
            return JsonResponse({
                "status": 2,
                "message": "请求参数错误"
            })
    else:
        return JsonResponse({
          "status": 3,
          "message": "请求方法错误"
        })
