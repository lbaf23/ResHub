import json

from django.http import JsonResponse

from ResModel.models import Browse


def browse_history(request):
    if request.method == "GET":
        data = json.loads(request.body)
        userEmailId = data.get("userEmailId")
        if userEmailId is not None:
            History = Browse.objects.filter(UserEmail=userEmailId).order_by("BrowseTime")
            HistoryList = list(History)
            if len(HistoryList)==0:
                return JsonResponse({
                    "status": 4,
                    "message": "列表为空"
                })
            retLiteratureId = []
            retTimeList = []
            cnt = 0
            for i in HistoryList:
                retLiteratureId.append(i.LiteratureId)
                retTimeList.append(i.BrowseTime)
                cnt += 1
            return JsonResponse({
                "status": 1,
                "LiteratureIdlist":retLiteratureId,
                "timelist": retTimeList,
                "message": "已经返回浏览记录列表",
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