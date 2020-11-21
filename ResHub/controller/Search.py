from haystack.query import SearchQuerySet
from django.http import JsonResponse
from ResModel.models import Paper
import json
from django.core import serializers
import time

def search_keywords(request):
    p_abstract = request.GET.get('PaperAbstract')
    page = request.GET.get('page') # 页数
    per_page = request.GET.get('PerPage') #每页的数量

    res = SearchQuerySet().filter(PaperAbstract=p_abstract).values('object')

    l = []

    for r in res:
        p = r['object']
        j = {
            'PaperTitle': p.PaperTitle
        }
        l.append(j)

    return JsonResponse({'num': res.count(), 'result': l })