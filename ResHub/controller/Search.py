from haystack.query import SearchQuerySet, SQ
from django.http import JsonResponse
import json
from ResModel.models import PaperAuthor, Project, Paper
import re

# 检索式解码
def exists_in_redis(s1):
    s1.sort()
    return s1


# boolType {1:AND ; 2:OR ; 3:NOT}
# type {1：主题；2：标题；3：作者；4：关键词；5：摘要; }
def search_el_indexes(res, key):
    for w in list(key):
        if not w.__contains__('boolType'):
            if w['type'] == '4':
                res = res.filter(PaperKeywords=w['words'])
            elif w['type'] == '1':
                res = res.filter(text=w['words'])
            elif w['type'] == '2':
                res = res.filter(PaperTitle=w['words'])
            elif w['type'] == '5':
                res = res.filter(PaperAbstract=w['words'])
            elif w['type'] == '3':
                res = res.filter(PaperAuthors=w['words'])
            elif w['type'] == 'PaperOrg':
                res = res.filter(PaperOrg=w['words'])
        else:
            if w['boolType'] == '1':
                if w['type'] == '4':
                    res = res.filter_and(PaperKeywords=w['words'])
                elif w['type'] == '1':
                    res = res.filter_and(text=w['words'])
                elif w['type'] == '2':
                    res = res.filter_and(PaperTitle=w['words'])
                elif w['type'] == '5':
                    res = res.filter_and(PaperAbstract=w['words'])
                elif w['type'] == '3':
                    res = res.filter_and(PaperAuthors=w['words'])
                elif w['type'] == 'PaperOrg':
                    res = res.filter_and(PaperOrg=w['words'])

            elif w['boolType'] == '2':
                if w['type'] == '4':
                    res = res.filter_or(PaperKeywords=w['words'])
                elif w['type'] == '1':
                    res = res.filter_or(text=w['words'])
                elif w['type'] == '2':
                    res = res.filter_or(PaperTitle=w['words'])
                elif w['type'] == '5':
                    res = res.filter_or(PaperAbstract=w['words'])
                elif w['type'] == '3':
                    res = res.filter_or(PaperAuthors=w['words'])
                elif w['type'] == 'PaperOrg':
                    res = res.filter_or(PaperOrg=w['words'])

            elif w['boolType'] == '3':
                if w['type'] == '4':
                    res = res.exclude(PaperKeywords=w['words'])
                elif w['type'] == '1':
                    res = res.exclude(text=w['words'])
                elif w['type'] == '2':
                    res = res.exclude(PaperTitle=w['words'])
                elif w['type'] == '5':
                    res = res.exclude(PaperAbstract=w['words'])
                elif w['type'] == '3':
                    res = res.exclude(PaperAuthors=w['words'])
                elif w['type'] == 'PaperOrg':
                    res = res.exclude(PaperOrg=w['words'])

            else:
                pass

    return res


def search_words(request):
    search_key = request.GET.get('keyWords')
    page = request.GET.get('page') # 页数
    per_page = request.GET.get('PerPage') #每页的数量

    start_year = int(request.GET.get('dateStart'))
    end_year = int(request.GET.get('dateEnd'))

    radio = request.GET.get('Redio') # 中英扩展 false true

    sk = json.loads(search_key)

    #if exists_in_redis(sk):
    #    pass
        # search from redis
        # ...

    # search by elasticsearch index
    qs = SearchQuerySet()
    res = search_el_indexes(qs, sk)


    # 过滤年份等数据并排序
    # order_by

    num = res.count()
    res = res.values('object')[(int(page)-1)*int(per_page): int(page)*int(per_page)]

    l = []

    for r in res:
        p = r['object']

        j = {
            'paperId': p.PaperId,
            'title': p.PaperTitle,
            'msg': p.PaperAbstract,
            'author': p.PaperAuthors,

        }
        l.append(j)

    return JsonResponse({'num': num, 'result': l})


def show_paper_info(request):
    pid = request.GET.get('paperId')
    pl = Paper.objects.filter(PaperId=pid)
    if len(pl) > 0:
        p = pl[0]
        alist = p.PaperAuthors.split(str="",)
        authorId = ['null']*len(alist)
        aulist = PaperAuthor.objects.filter(PaperId=p.PaperId)
        for a in aulist:
            authorId[int(a.ResearcherRank)] = a.ResearcherId

        return JsonResponse({
            'paperId': p.PaperId,
            'title': p.PaperTitle,
            'msg': p.PaperAbstract,
            'author': p.PaperAuthors,
            'authorId': authorId,

            'keyword': re.sub(r'[\[|\']','' , str(p.PaperKeywords)),
        })




def search_authors(request):
    search_key = request.GET.get('searchKey')
    page = request.GET.get('page') # 页数
    per_page = request.GET.get('PerPage') #每页的数量
    order_by = request.GET.get('orderBy')

    pass


def filter_search_words(request):
    pass
