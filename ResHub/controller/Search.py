from haystack.query import SearchQuerySet, SQ
from django.http import JsonResponse
import json
from ResModel.models import PaperAuthor, Project, Paper
import re
import requests


# 检索式解码
def exists_in_redis(s1):
    s1.sort()
    return s1


def translate_by_api(str):
    """
   input : str 需要翻译的字符串
   output：translation 翻译后的字符串
   有每小时1000次访问的限制
   """
    # API
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
    # 传输的参数， i为要翻译的内容
    key = {
        'type': "AUTO",
        'i': str,
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "ue": "UTF-8",
        "action": "FY_BY_CLICKBUTTON",
        "typoResult": "true"
    }
    # key 这个字典为发送给有道词典服务器的内容
    response = requests.post(url, data=key)
    # 判断服务器是否相应成功
    if response.status_code == 200:
        # 通过 json.loads 把返回的结果加载成 json 格式
        result = json.loads(response.text)
        #         print ("输入的词为：%s" % result['translateResult'][0][0]['src'])
        #         print ("翻译结果为：%s" % result['translateResult'][0][0]['tgt'])
        translation = result['translateResult'][0][0]['tgt']
        return translation
    else:
        # 相应失败就返回空
        return ''


# boolType {1:AND ; 2:OR ; 3:NOT}
# type {1：主题；2：标题；3：作者；4：关键词；5：摘要; }
def search_el_indexes(res, key, redio):
    for w in list(key):
        if not w.__contains__('boolType'):
            if w['type'] == '4':
                res = res.filter(PaperKeywords=w['words'])
                if redio:
                    ow = translate_by_api(w['words'])
                    if ow != '':
                        res = res.filter_or(PaperKeywords=ow)
            elif w['type'] == '1':
                res = res.filter(text=w['words'])
                if redio:
                    ow = translate_by_api(w['words'])
                    if ow != '':
                        res = res.filter_or(text=ow)

            elif w['type'] == '2':
                res = res.filter(PaperTitle=w['words'])
                if redio:
                    ow = translate_by_api(w['words'])
                    if ow != '':
                        res = res.filter_or(PaperTitle=ow)

            elif w['type'] == '5':
                res = res.filter(PaperAbstract=w['words'])
                if redio:
                    ow = translate_by_api(w['words'])
                    if ow != '':
                        res = res.filter_or(PaperAbstract=ow)

            elif w['type'] == '3':
                res = res.filter(PaperAuthors=w['words'])
                if redio:
                    ow = translate_by_api(w['words'])
                    if ow != '':
                        res = res.filter_or(PaperAuthors=ow)

            elif w['type'] == 'PaperOrg':
                res = res.filter(PaperOrg=w['words'])
                if redio:
                    ow = translate_by_api(w['words'])
                    if ow != '':
                        res = res.filter_or(PaperOrg=ow)

        else:
            if w['boolType'] == '1':
                if w['type'] == '4':
                    res = res.filter_and(PaperKeywords=w['words'])
                    if redio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.filter_or(PaperKeywords=ow)

                elif w['type'] == '1':
                    res = res.filter_and(text=w['words'])
                    if redio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.filter_or(text=ow)

                elif w['type'] == '2':
                    res = res.filter_and(PaperTitle=w['words'])
                    if redio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.filter_or(PaperTitle=ow)

                elif w['type'] == '5':
                    res = res.filter_and(PaperAbstract=w['words'])
                    if redio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.filter_or(PaperAbstract=ow)

                elif w['type'] == '3':
                    res = res.filter_and(PaperAuthors=w['words'])
                    if redio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.filter_or(PaperAuthors=ow)

                elif w['type'] == 'PaperOrg':
                    res = res.filter_and(PaperOrg=w['words'])
                    if redio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.filter_or(PaperOrg=ow)

            elif w['boolType'] == '2':
                if w['type'] == '4':
                    res = res.filter_or(PaperKeywords=w['words'])
                    if redio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.filter_or(PaperKeywords=ow)

                elif w['type'] == '1':
                    res = res.filter_or(text=w['words'])
                    if redio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.filter_or(text=ow)

                elif w['type'] == '2':
                    res = res.filter_or(PaperTitle=w['words'])
                    if redio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.filter_or(PaperTitle=ow)

                elif w['type'] == '5':
                    res = res.filter_or(PaperAbstract=w['words'])
                    if redio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.filter_or(PaperAbstract=ow)

                elif w['type'] == '3':
                    res = res.filter_or(PaperAuthors=w['words'])
                    if redio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.filter_or(PaperAuthors=ow)

                elif w['type'] == 'PaperOrg':
                    res = res.filter_or(PaperOrg=w['words'])
                    if redio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.filter_or(PaperOrg=ow)

            elif w['boolType'] == '3':
                if w['type'] == '4':
                    res = res.exclude(PaperKeywords=w['words'])
                    if redio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.exclude(PaperKeywords=ow)

                elif w['type'] == '1':
                    res = res.exclude(text=w['words'])
                    if redio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.exclude(text=ow)

                elif w['type'] == '2':
                    res = res.exclude(PaperTitle=w['words'])
                    if redio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.exclude(PaperTitle=ow)

                elif w['type'] == '5':
                    res = res.exclude(PaperAbstract=w['words'])
                    if redio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.exclude(PaperAbstract=ow)

                elif w['type'] == '3':
                    res = res.exclude(PaperAuthors=w['words'])
                    if redio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.exclude(PaperAuthors=ow)

                elif w['type'] == 'PaperOrg':
                    res = res.exclude(PaperOrg=w['words'])
                    if redio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.exclude(PaperOrg=ow)

            else:
                pass

    return res


def search_words(request):
    search_key = request.GET.get('keyWords')
    try:
        page = int(request.GET.get('page')) # 页数
    except Exception:
        page = 1

    try:
        per_page = int(request.GET.get('PerPage')) #每页的数量
    except Exception:
        per_page = 10

    start_year = int(request.GET.get('dateStart'))
    end_year = int(request.GET.get('dateEnd'))

    type = request.GET.get('type')

    radio = request.GET.get('Redio') # 中英扩展 false true

    sk = json.loads(search_key)

    #if exists_in_redis(sk):
    #    pass
        # search from redis
        # ...

    # search by elasticsearch index
    qs = SearchQuerySet()
    res = search_el_indexes(qs, sk, radio)

    num = res.count()
    res = res.values('object')[(page-1)*per_page: page*per_page]

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
