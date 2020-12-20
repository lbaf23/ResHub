import json

from django.http import HttpResponse, JsonResponse
from ResModel.models import HubUser


def changeHead(request):
    if request.method == "POST":
        userEmail = request.GET.get("userId")
        userHead =  request.GET.get("url")
        if userEmail is not None and userHead is not None:
            user = HubUser.objects.filter(UserEmail=userEmail).first()
            user.UserImage = userHead
            user.save()
            return JsonResponse({
                "status": 1,
                "message": "更换头像成功",
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