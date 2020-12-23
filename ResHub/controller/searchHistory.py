import json
import datetime
from django.http import JsonResponse

from ResModel.models import Search
from ResModel.models import HubUser,hotwords

def add_search_history(request):
    user_id = request.POST.get('userId')
    keyword = request.POST.get('keyWords')
    succeed = True
    user=HubUser.objects.get(UserEmail=user_id)
    u = Search(UserEmail=user,SearchContent=keyword,SearchTime=datetime.datetime.now())
    u.save()
    key =hotwords.objects.filter(word=keyword)
    if(len(key)==0):
        hot = hotwords(word=keyword,value=1)
        hot.save()
    else:
        value = key[0].value
        hotwords.objects.filter(word=keyword).update(value=value+1)
    return JsonResponse({'result':succeed})

def return_hot_words(request):
    hot=hotwords.objects.filter(value__gt=100).order_by("value")
    word={}
    value={}
    for i in range(0,len(hot)):
        word[i]=hot[i].word
        value[i]=hot[i].value
        if i>40:
            break
    return JsonResponse({'word':word,"value":value})
