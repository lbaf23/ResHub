from django.http import JsonResponse
from ResModel.models import Browse


def deleteSearchRecord(request):
    try:
        if request.method == "GET":
            userId = request.GET.get('userId')
            if userId is not None:
                res = {}
                list = []
                browse = Browse.objects.filter(UserEmail=userId)
                len = browse.__len__()
                if(len == 0):
                    return JsonResponse({
                        "status": 0,
                        "message": "Nothing"
                    })
                for i in browse:
                    temp = i.id
                    i.delete()
                    list.append(temp)
                res['len'] = browse.__len__()
                res['list'] = list
                return JsonResponse({
                    "status": 1,
                    "message": res
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
