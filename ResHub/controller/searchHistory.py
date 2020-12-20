import json
import datetime
from django.http import JsonResponse

from ResModel.models import Search

def add_search_history(request):
    user_id = request.POST.get('userId')
    keyword = request.POST.get('keyWords')
    succeed = True
    u = Search(UserEmail=user_id,SearchContent=keyword,SearchTime=datetime.datetime.now())
    u.save()
    return JsonResponse({'result':succeed})

