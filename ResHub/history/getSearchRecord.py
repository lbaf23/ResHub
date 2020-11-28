from django.http import JsonResponse
from ResModel.models import Search


def getSearchRecord(request):
    try:
        if request.method == "GET":
            userId = request.GET.get('userId')
            if userId is not None:
                res = {}
                list = []
                search = Search.objects.filter(UserEmail=userId)
                len = search.__len__()
                if(len == 0):
                    return JsonResponse({
                        "status": 0,
                        "message": "Nothing"
                    })
                for i in search:
                    temp = {}
                    temp['SearchContent'] = i.SearchContent
                    temp['SearchTime'] = str(i.SearchTime)
                    list.append(temp)
                res['len'] = search.__len__()
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
