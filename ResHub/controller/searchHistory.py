import json
import datetime,re
from django.http import JsonResponse

from ResModel.models import Search
from ResModel.models import HubUser,hotwords,Paper,Researcher

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
    hotWords=list()
    for i in range(0,len(hot)):
        word=hot[i].word
        value=hot[i].value
        j={'name':word,'value':value}
        hotWords.append(j)
        if i>39:
            break
    return JsonResponse({'hotWords':hotWords})

def get_hot(request):
    hot=hotwords.objects.filter(value__gt=100).order_by("-value")
    paper = Paper.objects.filter(ReadNum__gt=1000).order_by("-ReadNum")
    res = Researcher.objects.filter(CitedNum__gt=100).order_by("-VisitNum")
    hotWords=list()
    p=list()
    su=list()
    sc=list()
    sn=list()
    for i in range(0,len(hot)):
        word=hot[i].word
        value=hot[i].value
        j={'name':word,'value':value}
        hotWords.append(j)
        if i>19:
            break
    for i in range(0,len(paper)):
        j={
            'title':paper[i].PaperTitle,
            'link':re.sub(r'[\[|\]|\'| ]','',paper[i].PaperUrl).split(',')[0]
        }
        p.append(j)
        if i>11:
            break
    for i in range(0,len(res)):
        su[i]=res[i].CitedNum
        sc[i]=res[i].LiteratureNum
        sn[i]=res[i].ResName
        if i>11:
            break
    return JsonResponse({'hotSearach':hotWords,'scholarUsed':su,'scholarCited':sc,'paperTable':p,'scholarName':sn})
