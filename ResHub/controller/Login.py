import json

from ResModel.models import HubUser
from django.http import HttpResponse, JsonResponse
from ResHub.redispool import r
from ResHub.sendMail import send_email
from ResModel.models import Researcher

def identity_check(request):
    uid = request.POST.get('userId')
    pwd = request.POST.get('password')
    print(uid, pwd)
    u = HubUser.objects.filter(UserEmail=uid).filter(UserPassword=pwd)
    if(u.__len__() > 0):
        id=u[0].UserEmail
        head=u[0].UserImage
        user = Researcher.objects.filter(ResEmail=id)
        if(user.__len__()>0):
            isPortal = True
            protalId = user[0].ResId
        else:
            isPortal = False
            protalId = None
        if(u[0].UserEmail == "root@root"):
            isAdministrator = True
        else:
            isAdministrator = False
        label = u[0].UserIntroduction
        return JsonResponse({'myId':id,'userHead':head,'isPortal':isPortal,'portalId':protalId,'isAdministrator':isAdministrator,'label':label,'result':True})

    else:
        return JsonResponse({'result': False})


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
    Code = int(code)
    correct = r.get(email)
    if(Code==correct):
        r.delete(str(email), Code)
        return JsonResponse({'result':result})
    else:
       result=False
       return JsonResponse({'result':result})


def passwordLost(request):
    if request.method == "GET":
        UserEmail = request.Get.get('mailAddress')
        if UserEmail is not None:
            send_email(UserEmail)
            result = True
            return JsonResponse({'result': result})
        else:
            result = False
            return JsonResponse({'result': result})

    else:
        result = False
        return JsonResponse({'result': result})
