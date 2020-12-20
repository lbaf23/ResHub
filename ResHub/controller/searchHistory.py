import json
import datetime
from django.http import JsonResponse

from ResModel.models import Search
from ResModel.models import HubUser

def add_search_history(request):
    user_id = request.POST.get('userId')
    keyword = request.POST.get('keyWords')
    succeed = True
    user=HubUser.objects.get(UserEmail=user_id)
    u = Search(UserEmail=user,SearchContent=keyword,SearchTime=datetime.datetime.now())
    u.save()
    return JsonResponse({'result':succeed})

