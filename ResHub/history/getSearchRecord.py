from django.http import JsonResponse
from ResModel.models import Search
import re


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
                    string = str(i.SearchTime)
                    cock = string.split(' ')
                    temp['SearchTime'] = cock[0]
                    temp['id'] = str(i.id)
                    temp['searchList'] = i.SearchList
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
