import json

from django.http import JsonResponse

from ResModel.models import Search

def add_search_history(request):
    user_id = request.GET.get('userId')
    keyword = request.GET.get('keyWords')
    succeed = True
    u = Search(UserEmail=user_id,SearchContent=keyword)
    u.save()
    return JsonResponse({'result':succeed})

