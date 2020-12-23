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
                helplist = []
                browse = Search.objects.filter(UserEmail_id=userId).all()
                len = browse.__len__()
                if(len == 0):
                    return JsonResponse({
                        "status": 0,
                        "message": "Nothing",
                        "succeed": False
                    })
                index = 0
                temp_this = browse[0]

                for i in deletlist:
                    k = int(i)
                    flag = 0
                    for j in browse:
                        if(k == j.id):
                            helplist.append(j)
                            flag = 1
                            break
                    if(flag == 0):
                        res['succeed'] = False
                        return JsonResponse(res)

                for i in helplist:
                    i.delete()

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
