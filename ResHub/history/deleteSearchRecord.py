from django.http import JsonResponse
from ResModel.models import Browse, Search


def deleteSearchRecord(request):
    try:
        if request.method == "GET":
            userId = request.GET.get('userId')
            if userId is not None:
                res = {}
                list = []
                browse = Search.objects.filter(UserEmail_id=userId).all()
                len = browse.__len__()
                if(len == 0):
                    return JsonResponse({
                        "status": 0,
                        "message": "Nothing",
                        "succeed": False
                    })
                for i in browse:
                    temp = str(i.id)
                    i.delete()
                    list.append(temp)
                res['len'] = browse.__len__()
                res['userId'] = userId
                res['list'] = list
                res['succeed'] = True
                return JsonResponse(res)
            else:
                return JsonResponse({
                    "status": 2,
                    "message": "请求参数错误",
                    "succeed": False
                })
        else:
            return JsonResponse({
                "status": 3,
                "message": "请求方法错误",
                "succeed": False
            })
    except Exception as e:
        return JsonResponse({
            "status": 4,
            "message": str(e),
            "succeed": False
        })
