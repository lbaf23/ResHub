import json
from django.http import JsonResponse
from pandas.core.dtypes.inference import is_number

from ResHub.createResId import tid_maker
from ResHub.redispool import r
from ResModel.models import Researcher, HubUser
from django_redis import get_redis_connection


def catch_portal(request):
    if request.method == "POST":
        data = json.loads(request.body)
        UserEmail = data.get("UserEmail")
        ResEmail = data.get("ResEmail")
        id = int(data.get("id"))
        code = int(data.get('code'))
        if r.get(ResEmail) is None or code != int(r.get(ResEmail)):
            return JsonResponse({
                "status": 0,
                "message": "验证码错误",
            })
        if id is not None:
            Portal = Researcher.objects.filter(id=id).first()
            if Portal.IsClaim == 0:
                Portal.IsClaim = 1
                Portal.ResEmail = ResEmail
                Portal.UserEmail = HubUser.objects.filter(UserEmail=UserEmail).first()
                Portal.save()
                return JsonResponse({
                    "status": 1,
                    "message": "门户认领成功",
                }, safe=False)
            else:
                return JsonResponse({
                    "status": 2,
                    "message": "该门户已被认领",
                }, safe=False)
        else:
            return JsonResponse({
                "status": 3,
                "message": "该门户不存在"
            })
    else:
        return JsonResponse({
            "status": 4,
            "message": "请求方法错误"
        })


def new_portal(request):
    if request.method == "POST":
        data = json.loads(request.body)
        resId= tid_maker()
        userEmail = data.get("UserEmail")
        resEmail = data.get("ResEmail")
        code = int(data.get('code'))
        if r.get(resEmail) is None or code != int(r.get(resEmail)):
            return JsonResponse({
                "status": 0,
                "message": "验证码错误",
            })
        if userEmail is not None and resEmail is not None:
            resemail_exists = Researcher.objects.filter(ResEmail=resEmail)
            if resemail_exists.exists():
                return JsonResponse({
                    "status": 1,
                    "message": "该教育邮箱已被使用",
                }, safe=False)
            user = HubUser.objects.filter(UserEmail=userEmail).first()
            Researcher.objects.create(ResId=resId, UserEmail=user, IsClaim=1, ResEmail=resEmail)
            return JsonResponse({
                "status": 2,
                "message": "创建门户成功"
            })
        else:
            return JsonResponse({
                "status": 3,
                "message": "请求参数错误"
            })
    else:
        return JsonResponse({
            "status": 4,
            "message": "请求方法错误"
        })


def appeal_portal(request):
    return JsonResponse({
        "status": 4,
        "message": "请求方法错误"
    })