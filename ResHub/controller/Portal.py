import json

from django.http import JsonResponse

from ResHub.createResId import tid_maker
from ResHub.redispool import r
from ResModel.models import Researcher, HubUser, Appeal


def catch_portal(request):
    if request.method == "POST":
        UserEmail = request.POST.get("UserEmail")
        ResEmail = request.POST.get("ResEmail")
        id = request.POST.get("ResId")
        if id is not None:
            Portal = Researcher.objects.filter(ResId=id).first()
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
                "message": "没有输入ResId"
            })
    else:
        return JsonResponse({
            "status": 4,
            "message": "请求方法错误"
        })


def new_portal(request):
    if request.method == "POST":
        resId= tid_maker()
        userEmail = request.POST.get("UserEmail")
        resEmail = request.POST.get("ResEmail")
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
    if request.method == "POST":
        resId = request.POST.get("ReserchId")
        resEmail = request.POST.get("ResEmail")
        userEmail = request.POST.get("UserEmail")
        conTent = request.POST.get("ConTent")
        if resId is not None and resEmail is not None and userEmail is not None:
            user = HubUser.objects.filter(UserEmail=userEmail).first()
            researcher = Researcher.objects.filter(ResId=resId).first()
            appeal = Appeal.objects.filter(ResearchId_id=researcher, UserEmail_id=user, AppealState=0).first()
            if appeal is not None:
                return JsonResponse({
                    "status": 1,
                    "message": "请勿重复提交同一申诉！",
                }, safe=False)
            if researcher is None:
                return JsonResponse({
                    "status": 2,
                    "message": "申诉的门户不存在！",
                }, safe=False)
            if researcher.IsClaim == 0:
                return JsonResponse({
                    "status": 3,
                    "message": "该门户未被认领！",
                }, safe=False)
            Appeal.objects.create(ResearchId_id=researcher.ResId, UserEmail_id=user.UserEmail, content=conTent ,AppealState=0)
            return JsonResponse({
                "status": 4,
                "message": "提交申诉成功！"
            })
        else:
            return JsonResponse({
                "status": 5,
                "message": "请求参数错误"
            })
    else:
        return JsonResponse({
            "status": 6,
            "message": "请求方法错误"
        })
