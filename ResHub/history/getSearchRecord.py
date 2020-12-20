from django.http import JsonResponse
from ResModel.models import Search


def getSearchRecord(request):
    try:
        if request.method == "GET":
            userId = request.GET.get('userId')
            if userId is not None:
                res = {}
                list = []
                search = Search.objects.filter(UserEmail_id=userId)
                len = search.__len__()
                if(len == 0):
                    res['list'] = []
                    return JsonResponse(res)
                for i in search:
                    temp = {}
                    temp['SearchContent'] = i.SearchContent
                    temp['SearchTime'] = str(i.SearchTime)
                    temp['id'] = i.id
                    list.append(temp)
                res['len'] = search.__len__()
                res['list'] = list
                print(res['list'])
                return JsonResponse(res)
            else:
                res['list'] = []
                return JsonResponse(res)
        else:
            res['list'] = []
            return JsonResponse(res)
    except Exception as e:
        res['list'] = []
        return JsonResponse(res)
