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
                        "result": False
                    })
                else:
                    HubUser.objects.filter(UserEmail=mailAddress).update(
                        UserPassword=newPassword)
                    # temp.UserPassword = newPassword
                    # temp.save()
                    return JsonResponse({
                        "status": 1,
                        "result": True
                    })
            else:
                return JsonResponse({
                    "status": 2,
                    "result": False
                })
        else:
            return JsonResponse({
                "status": 3,
                "result": False
            })
    except Exception as e:
        return JsonResponse({
            "status": 4,
            "result": False
        })
