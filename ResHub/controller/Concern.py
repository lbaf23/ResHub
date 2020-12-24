import json

from django.http import JsonResponse
from ResModel.models import Concern, Researcher, HubUser


def get_my_concern(request):
    if request.method == "GET":
        UserEmail = request.GET.get("UserEmail")
        if UserEmail is not None:
            concern = Concern.objects.filter(UserEmail_id=UserEmail).order_by("ConcernTime")
            concernlist = list(concern)
            if len(concernlist) == 0:
                return JsonResponse({
                    "status": 4,
                    "message": "列表为空"
                })
            retconcernList = []
            for i in concernlist:
                j = {}
                researcher = Researcher.objects.filter(ResId=i.ResearchId_id).first()
                if researcher.UserEmail is not None:
                    user = HubUser.objects.filter(UserEmail=researcher.UserEmail_id).first()
                    j['name'] = user.UserName
                    j['headImage'] = user.UserImage
                    j['userEmail'] = user.UserEmail
                    j['id'] = researcher.ResId
                    j['label'] = user.UserIntroduction
                else :
                    j['name'] = researcher.ResName
                    j['headImage'] = "head00.jpg"
                    j['userEmail'] = " "
                    j['id'] = researcher.ResId
                    j['label'] = " "
                retconcernList.append(j)

            return JsonResponse({
                "status": 1,
                "ConcernList": retconcernList,
                "message": "已经返回关注列表",
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


def cancel_concern(request):
    if request.method == "POST":
        UserEmail = request.POST.get("UserEmail")
        ResearchId = request.POST.get("ResearchId")
        if UserEmail is not None and ResearchId is not None:
            concern = Concern.objects.filter(UserEmail_id=UserEmail, ResearchId_id=ResearchId).first()
            concern.delete()
            return JsonResponse({
                "status": 1,
                "message": "取消关注成功",
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


def add_concern(request):
    if request.method == "POST":
        UserEmail = request.POST.get("UserEmail")
        ResearchId = request.POST.get("ResearchId")
        if UserEmail is not None and ResearchId is not None:
            concern = Concern.objects.filter(UserEmail_id=UserEmail, ResearchId_id=ResearchId).first()
            if concern is None:
                concern1 = Concern(UserEmail_id=UserEmail,ResearchId_id=ResearchId)
                concern1.save()
                return JsonResponse({
                    "status": 1,
                    "message": "关注成功",
                }, safe=False)
            else:
                return JsonResponse({
                    "status": 3,
                    "message": "不能重复关注",
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
