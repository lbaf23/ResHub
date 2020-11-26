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
    s = s1.split(',')
    s.sort()
    li = []
    for w in s:
        try:
            m1 = w.index(':')
            m2 = w.find('-')
            word = w[:m1]
            if m2 != -1:
                value = w[m1+1:m2]
                method = w[m2+1:]
            else:
                value = w[m1+1:]
                method = ''
            if method == '':
                li.insert(0, {'word': word, 'value': value, 'method': method})
            else:
                li.append({
                    'word': word, 'value': value, 'method': method
                })
        except Exception:
            pass
    return li

def search_el_indexes(key):
    res = SearchQuerySet()
    for w in key:
        if w['method'] == 'and':
            if w['word'] == 'PaperKeywords':
                res = res.filter_and(PaperKeywords=w['value'])
            elif w['word'] == 'PaperTitle':
                res = res.filter_and(PaperTitle=w['value'])
            elif w['word'] == 'PaperAbstract':
                res = res.filter_and(PaperAbstract=w['value'])
            elif w['word'] == 'PaperAuthors':
                res = res.filter_and(PaperAuthors=w['value'])
            elif w['word'] == 'PaperOrg':
                res = res.filter_and(PaperOrg=w['value'])

        elif w['method'] == 'or':
            if w['word'] == 'PaperKeywords':
                res = res.filter_or(PaperKeywords=w['value'])
            elif w['word'] == 'PaperTitle':
                res = res.filter_or(PaperTitle=w['value'])
            elif w['word'] == 'PaperAbstract':
                res = res.filter_or(PaperAbstract=w['value'])
            elif w['word'] == 'PaperAuthors':
                res = res.filter_or(PaperAuthors=w['value'])
            elif w['word'] == 'PaperOrg':
                res = res.filter_or(PaperOrg=w['value'])

        elif w['method'] == 'not':
            if w['word'] == 'PaperKeywords':
                res = res.filter_not(PaperKeywords=w['value'])
            elif w['word'] == 'PaperTitle':
                res = res.filter_not(PaperTitle=w['value'])
            elif w['word'] == 'PaperAbstract':
                res = res.filter_not(PaperAbstract=w['value'])
            elif w['word'] == 'PaperAuthors':
                res = res.filter_not(PaperAuthors=w['value'])
            elif w['word'] == 'PaperOrg':
                res = res.filter_not(PaperOrg=w['value'])

        else:
            if w['word'] == 'PaperKeywords':
                res = res.filter(PaperKeywords=w['value'])
            elif w['word'] == 'PaperTitle':
                res = res.filter(PaperTitle=w['value'])
            elif w['word'] == 'PaperAbstract':
                res = res.filter(PaperAbstract=w['value'])
            elif w['word'] == 'PaperAuthors':
                res = res.filter(PaperAuthors=w['value'])
            elif w['word'] == 'PaperOrg':
                res = res.filter(PaperOrg=w['value'])

    return res

def search_words(request):
    words = request.GET.get('words')
    page = request.GET.get('page') # 页数
    per_page = request.GET.get('PerPage') #每页的数量
    order_by = request.GET.get('orderBy')

    key = decode_search_words(words)

    print(str(key))

    # search from redis
    # ...

    # search by elasticsearch index
    res = search_el_indexes(key)
    # order_by

    num = res.count()
    res = res.values('object')[(int(page)-1)*int(per_page) : int(page)*int(per_page)]

    l = []

    for r in res:
        p = r['object']
        j = {
                   'PaperTitle': p.PaperTitle
        }
        l.append(j)

    return JsonResponse({'num':num, 'result': l })

