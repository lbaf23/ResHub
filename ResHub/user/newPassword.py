from django.http import HttpResponse, JsonResponse
from ResModel.models import HubUser


def newPassword(request):
    try:
        res = {}
        if request.method == "GET":
            mailAddress = request.GET.get('mailAddress')
            newPassword = request.GET.get('newPassword')
            if (mailAddress is not None) and (newPassword is not None):
                temp = HubUser.objects.get(UserEmail=mailAddress)
                if(temp is None):
                    return JsonResponse({
                        "status": 0,
                        "message": False
                    })
                else:
                    temp.UserPassword = newPassword
                    temp.save()
                    return JsonResponse({
                        "status": 1,
                        "message": True
                    })
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
    except Exception as e:
        return JsonResponse({
            "status": 4,
            "message": str(e)
        })
