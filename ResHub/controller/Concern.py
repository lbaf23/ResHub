import json

from django.http import JsonResponse
from ResModel.models import Concern,Researcher,HubUser


def get_my_concern(request):
    if request.method == "GET":
        data = json.loads(request.body)
        UserEmail = data.get("UserEmail")
        if UserEmail is not None:
            concern = Concern.objects.filter(UserEmail=UserEmail).order_by("ConcernTime")
            concernlist = list(concern)
            if len(concernlist) == 0:
                return JsonResponse({
                    "status": 4,
                    "message": "列表为空"
                })
            retconcernNameList = []
            retconcernEmailList = []
            retconcernHeadList = []
            cnt = 0
            for i in concernlist:
                researcher = Researcher.objects.filter(ResId=i.ResearchId_id).first()
                user = HubUser.objects.filter(UserEmail=researcher.UserEmail_id).first()
                retconcernNameList.append(user.UserName)
                retconcernEmailList.append(user.UserEmail)
                retconcernHeadList.append(user.UserImage)
                cnt += 1
            return JsonResponse({
                "status": 1,
                "NameList": retconcernNameList,
                "EmailList": retconcernEmailList,
                "HeadList": retconcernHeadList,
                "message": "已经返回关注者列表",
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
        data = json.loads(request.body)
        UserEmail = data.get("UserEmail")
        ResearchId = data.get("ResearchId")
        if UserEmail is not None and ResearchId is not None:
            concern = Concern.objects.filter(UserEmail=UserEmail,ResearchId=ResearchId).first()
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