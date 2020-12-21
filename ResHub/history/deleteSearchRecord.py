from django.http import JsonResponse
from ResModel.models import Browse, Search


def deleteSearchRecord(request):
    try:
        if request.method == "GET":
            userId = request.GET.get('userId')
            deletId = request.GET.get('Id')
            if userId is not None:
                deletlist = deletId.split(',')
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
                index = 0
                for i in deletlist:
                    j = Search.objects.get(UserEmail_id=userId, id=i)
                    if(j is None):
                        res['succeed'] = False
                        return JsonResponse(res)
                    temp = str(j.id)
                    j.delete()
                    list.append(temp)
                    index = index + 1
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
