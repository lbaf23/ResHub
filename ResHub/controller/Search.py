from haystack.query import SearchQuerySet
from django.http import JsonResponse
from ResModel.models import Paper
import json
from django.core import serializers
import time
import re

# 检索式解码
def decode_search_words(s1):
    s1 = re.sub(r"\s+", "", s1)
    s = s1.split(';')
    s.sort()
    li = []
    for w in s:
        m1 = w.index(':')
        m2 = w.find('-')
        word = w[:m1]
        if m2 != -1:
            value = w[m1+1:m2]
            method = w[m2+1:]
        else:
            value = w[m1+1:]
            method = ''
        li.append({
            'word': word, 'value': value, 'method': method
        })
    return li

def search_words(request):
    words = request.GET.get('words')
    page = request.GET.get('page') # 页数
    per_page = request.GET.get('PerPage') #每页的数量

    key = decode_search_words(words)

    print(str(key))

    # 缓存没有，搜索
    res = SearchQuerySet()
    for w in key:
        if w['method'] == 'and':
            if w['word'] == 'PaperKeywords':
                res = res.filter_and(PaperKeywords=w['value'])
            elif w['word'] == 'PaperTitle':
                res = res.filter_and(PaperKeywords=w['value'])

        elif w['method'] == 'or':
            if w['word'] == 'PaperKeywords':
                res = res.filter_or(PaperKeywords=w['value'])
            elif w['word'] == 'PaperTitle':
                res = res.filter_or(PaperKeywords=w['value'])

        elif w['method'] == 'not':
            if w['word'] == 'PaperKeywords':
                res = res.filter_not(PaperKeywords=w['value'])
            elif w['word'] == 'PaperTitle':
                res = res.filter_not(PaperKeywords=w['value'])

        else:
            if w['word'] == 'PaperKeywords':
                res = res.filter(PaperKeywords=w['value'])
            elif w['word'] == 'PaperTitle':
                res = res.filter(PaperKeywords=w['value'])




    res = res.values('object')
    num = res.count()

    l = []

    for r in res:
        p = r['object']
        j = {
                   'PaperTitle': p.PaperTitle
        }
        l.append(j)

    return JsonResponse({'num':num, 'result': l })