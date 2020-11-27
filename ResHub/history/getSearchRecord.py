from django.http import JsonResponse
from ResModel.models import Search


def getSearchRecord(request):
    try:
        if request.method == "GET":
            userId = request.GET.get('userId')
            if userId is not None:
                res = {}
                list = []
                Search = Search.objects.filter(UserEmail=userId)
                for i in Search:
                    temp = {}
                    temp.append(i.SearchContent)
                    temp.append(i.SearchTime)
                    list.append(temp)
                res['len'] = Search.len()
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
