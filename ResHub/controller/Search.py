import json
import re

import requests
from django.http import JsonResponse
from haystack.query import SearchQuerySet

from ResModel.models import PaperAuthor, Project, Paper, PaperReference, Patent, Collection
import time

# 检索式解码
def exists_in_redis(s1):
    s1.sort()
    return s1


def format_list(s):
    if s is None:
        return []
    return s.split(',')[:-1]


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
def search_el_indexes(res, key, radio, type):
    if type == 'paper':
        return search_paper_index(res, key, radio)
    elif type == 'project':
        return search_project_index(res, key, radio)
    elif type == 'patent':
        return search_patent_index(res, key, radio)
    else:
        return SearchQuerySet()


def search_patent_index(res, key, radio):
    for w in list(key):
        if not w.__contains__('boolType'):
            if w['type'] == '1' or w['type'] == '4':
                res = res.using('patent').filter(text=w['words'])
                if radio:
                    ow = translate_by_api(w['words'])
                    if ow != '':
                        res = res.using('patent').filter_or(text=ow)

            elif w['type'] == '2':
                res = res.using('patent').filter(PatentTitle=w['words'])
                if radio:
                    ow = translate_by_api(w['words'])
                    if ow != '':
                        res = res.using('patent').filter_or(PatentTitle=ow)

            elif w['type'] == '5':
                res = res.using('patent').filter(PatentAbstract=w['words'])
                if radio:
                    ow = translate_by_api(w['words'])
                    if ow != '':
                        res = res.using('patent').filter_or(PatentAbstract=ow)

            elif w['type'] == '3':
                res = res.using('patent').filter(PatentAuthor=w['words'])
                if radio:
                    ow = translate_by_api(w['words'])
                    if ow != '':
                        res = res.using('patent').filter_or(PatentAuthor=ow)

            elif w['type'] == 'PaperOrg':
                res = res.using('patent').filter(PatentCompany=w['words'])
                if radio:
                    ow = translate_by_api(w['words'])
                    if ow != '':
                        res = res.using('patent').filter_or(PatentCompany=ow)

        else:
            if w['boolType'] == '1':
                if w['type'] == '1' or w['type'] == '4':
                    res = res.using('patent').filter_and(text=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.using('patent').filter_or(text=ow)

                elif w['type'] == '2':
                    res = res.using('patent').filter_and(PatentTitle=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.using('patent').filter_or(PatentTitle=ow)

                elif w['type'] == '5':
                    res = res.using('patent').filter_and(PatentAbstract=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.using('patent').filter_or(PatentAbstract=ow)

                elif w['type'] == '3':
                    res = res.using('patent').filter_and(PatentAuthor=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.using('patent').filter_or(PatentAuthor=ow)

                elif w['type'] == 'PaperOrg':
                    res = res.using('patent').filter_and(PatentCompany=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.using('patent').filter_or(PatentCompany=ow)

            elif w['boolType'] == '2':
                if w['type'] == '1' or w['type'] == '4':
                    res = res.using('patent').filter_or(text=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.using('patent').filter_or(text=ow)

                elif w['type'] == '2':
                    res = res.using('patent').filter_or(PatentTitle=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.using('patent').filter_or(PatentTitle=ow)

                elif w['type'] == '5':
                    res = res.using('patent').filter_or(PatentAbstract=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.using('patent').filter_or(PatentAbstract=ow)

                elif w['type'] == '3':
                    res = res.using('patent').filter_or(PatentAuthor=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.using('patent').filter_or(PatentAuthor=ow)

                elif w['type'] == 'PaperOrg':
                    res = res.using('patent').filter_or(PatentCompany=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.using('patent').filter_or(PatentCompany=ow)

            elif w['boolType'] == '3':
                if w['type'] == '1' or w['type'] == '4':
                    res = res.using('patent').exclude(text=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.using('patent').exclude(text=ow)

                elif w['type'] == '2':
                    res = res.using('patent').exclude(PatentTitle=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.using('patent').exclude(PatentTitle=ow)

                elif w['type'] == '5':
                    res = res.using('patent').exclude(PatentAbstract=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.using('patent').exclude(PatentAbstract=ow)

                elif w['type'] == '3':
                    res = res.using('patent').exclude(PatentAuthor=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.using('patent').exclude(PatentAuthor=ow)

                elif w['type'] == 'PaperOrg':
                    res = res.using('patent').exclude(PatentCompany=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.using('patent').exclude(PatentCompany=ow)

            else:
                pass

    return res


def search_project_index(res, key, radio):
    for w in list(key):
        if not w.__contains__('boolType'):
            if w['type'] == '4':
                res = res.using('project').filter(SubjectHeadingCN=w['words']).filter_or(SubjectHeadingEN=w['words'])
                if radio:
                    ow = translate_by_api(w['words'])
                    if ow != '':
                        res = res.using('project').filter_or(SubjectHeadingCN=ow).filter_or(SubjectHeadingEN=ow)
            elif w['type'] == '1':
                res = res.using('project').filter(text=w['words'])
                if radio:
                    ow = translate_by_api(w['words'])
                    if ow != '':
                        res = res.using('project').filter_or(text=ow)

            elif w['type'] == '2':
                res = res.using('project').filter(ProjectTitle=w['words'])
                if radio:
                    ow = translate_by_api(w['words'])
                    if ow != '':
                        res = res.using('project').filter_or(ProjectTitle=ow)

            elif w['type'] == '5':
                res = res.using('project').filter(ZhAbstract=w['words']). \
                    filter_or(EnAbstract=w['words']).filter_or(FinalAbstract=w['words'])
                if radio:
                    ow = translate_by_api(w['words'])
                    if ow != '':
                        res = res.using('project').filter_or(PaperAbstract=ow). \
                            filter_or(EnAbstract=ow).filter_or(FinalAbstract=ow)

            elif w['type'] == '3':
                res = res.using('project').filter(ProjectLeader=w['words'])
                if radio:
                    ow = translate_by_api(w['words'])
                    if ow != '':
                        res = res.using('project').filter_or(ProjectLeader=ow)

            elif w['type'] == 'PaperOrg':
                res = res.using('project').filter(SupportUnits=w['words'])
                if radio:
                    ow = translate_by_api(w['words'])
                    if ow != '':
                        res = res.using('project').filter_or(SupportUnits=ow)

        else:
            if w['boolType'] == '1':
                if w['type'] == '4':
                    res = res.using('project').filter_and(SubjectHeadingCN=w['words']).filter_or(
                        SubjectHeadingEN=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.using('project').filter_and(SubjectHeadingEN=ow).filter_or(SubjectHeadingEN=ow)

                elif w['type'] == '1':
                    res = res.using('project').filter_and(text=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.using('project').filter_or(text=ow)

                elif w['type'] == '2':
                    res = res.using('project').filter_and(ProjectTitle=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.using('project').filter_or(ProjectTitle=ow)

                elif w['type'] == '5':
                    res = res.using('project').filter_and(ZhAbstract=w['words']). \
                        filter_or(EnAbstract=w['words']).filter_or(FinalAbstract=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.using('project').filter_and(EnAbstract=w['words']). \
                                filter_or(ZhAbstract=w['words']).filter_or(FinalAbstract=w['words'])

                elif w['type'] == '3':
                    res = res.using('project').filter_and(ProjectLeader=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.using('project').filter_or(ProjectLeader=ow)

                elif w['type'] == 'PaperOrg':
                    res = res.using('project').filter_and(SupportUnits=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.using('project').filter_or(SupportUnits=ow)

            elif w['boolType'] == '2':
                if w['type'] == '4':
                    res = res.using('project').filter_or(SubjectHeadingCN=w['words']).filter_or(
                        SubjectHeadingEN=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.using('project').filter_or(SubjectHeadingCN=ow).filter_or(SubjectHeadingEN=ow)

                elif w['type'] == '1':
                    res = res.using('project').filter_or(text=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.using('project').filter_or(text=ow)

                elif w['type'] == '2':
                    res = res.using('project').filter_or(ProjectTitle=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.using('project').filter_or(ProjectTitle=ow)

                elif w['type'] == '5':
                    res = res.using('project').filter_or(ZhAbstract=w['words']). \
                        filter_or(EnAbstract=w['words']).filter_or(FinalAbstract=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.using('project').filter_or(ZhAbstract=ow). \
                                filter_or(EnAbstract=ow).filter_or(FinalAbstract=ow)

                elif w['type'] == '3':
                    res = res.using('project').filter_or(ProjectLeader=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.using('project').filter_or(ProjectLeader=ow)

                elif w['type'] == 'PaperOrg':
                    res = res.using('project').filter_or(SupportUnits=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.using('project').filter_or(SupportUnits=ow)

            elif w['boolType'] == '3':
                if w['type'] == '4':
                    res = res.using('project').exclude(SubjectHeadingCN=w['words']).exclude(SubjectHeadingEN=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.using('project').exclude(SubjectHeadingCN=ow).exclude(SubjectHeadingEN=ow)

                elif w['type'] == '1':
                    res = res.using('project').exclude(text=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.using('project').exclude(text=ow)

                elif w['type'] == '2':
                    res = res.using('project').exclude(ProjectTitle=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.using('project').exclude(ProjectTitle=ow)

                elif w['type'] == '5':
                    res = res.using('project').exclude(ZhAbstract=w['words']) \
                        .exclude(EnAbstract=w['words']).exclude(FinalAbstract=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.using('project').exclude(ZhAbstract=ow). \
                                exclude(EnAbstract=ow).exclude(FinalAbstract=ow)

                elif w['type'] == '3':
                    res = res.using('project').exclude(ProjectLeader=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.using('project').exclude(ProjectLeader=ow)

                elif w['type'] == 'PaperOrg':
                    res = res.using('project').exclude(SupportUnits=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.using('project').exclude(SupportUnits=ow)

            else:
                pass

    return res


def search_paper_index(res, key, radio):
    for w in list(key):
        if not w.__contains__('boolType'):
            if w['type'] == '4':
                res = res.filter(PaperKeywords=w['words'])
                if radio:
                    ow = translate_by_api(w['words'])
                    if ow != '':
                        res = res.filter_or(PaperKeywords=ow)
            elif w['type'] == '1':
                res = res.filter(text=w['words'])
                if radio:
                    ow = translate_by_api(w['words'])
                    if ow != '':
                        print(ow)
                        res = res.filter_or(text=ow)

            elif w['type'] == '2':
                res = res.filter(PaperTitle=w['words'])
                if radio:
                    ow = translate_by_api(w['words'])
                    if ow != '':
                        res = res.filter_or(PaperTitle=ow)

            elif w['type'] == '5':
                res = res.filter(PaperAbstract=w['words'])
                if radio:
                    ow = translate_by_api(w['words'])
                    if ow != '':
                        res = res.filter_or(PaperAbstract=ow)

            elif w['type'] == '3':
                res = res.filter(PaperAuthors=w['words'])
                if radio:
                    ow = translate_by_api(w['words'])
                    if ow != '':
                        res = res.filter_or(PaperAuthors=ow)

            elif w['type'] == 'PaperOrg':
                res = res.filter(PaperOrg=w['words'])
                if radio:
                    ow = translate_by_api(w['words'])
                    if ow != '':
                        res = res.filter_or(PaperOrg=ow)

        else:
            if w['boolType'] == '1':
                if w['type'] == '4':
                    res = res.filter_and(PaperKeywords=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.filter_or(PaperKeywords=ow)

                elif w['type'] == '1':
                    res = res.filter_and(text=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.filter_or(text=ow)

                elif w['type'] == '2':
                    res = res.filter_and(PaperTitle=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.filter_or(PaperTitle=ow)

                elif w['type'] == '5':
                    res = res.filter_and(PaperAbstract=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.filter_or(PaperAbstract=ow)

                elif w['type'] == '3':
                    res = res.filter_and(PaperAuthors=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.filter_or(PaperAuthors=ow)

                elif w['type'] == 'PaperOrg':
                    res = res.filter_and(PaperOrg=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.filter_or(PaperOrg=ow)

            elif w['boolType'] == '2':
                if w['type'] == '4':
                    res = res.filter_or(PaperKeywords=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.filter_or(PaperKeywords=ow)

                elif w['type'] == '1':
                    res = res.filter_or(text=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.filter_or(text=ow)

                elif w['type'] == '2':
                    res = res.filter_or(PaperTitle=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.filter_or(PaperTitle=ow)

                elif w['type'] == '5':
                    res = res.filter_or(PaperAbstract=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.filter_or(PaperAbstract=ow)

                elif w['type'] == '3':
                    res = res.filter_or(PaperAuthors=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.filter_or(PaperAuthors=ow)

                elif w['type'] == 'PaperOrg':
                    res = res.filter_or(PaperOrg=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.filter_or(PaperOrg=ow)

            elif w['boolType'] == '3':
                if w['type'] == '4':
                    res = res.exclude(PaperKeywords=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.exclude(PaperKeywords=ow)

                elif w['type'] == '1':
                    res = res.exclude(text=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.exclude(text=ow)

                elif w['type'] == '2':
                    res = res.exclude(PaperTitle=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.exclude(PaperTitle=ow)

                elif w['type'] == '5':
                    res = res.exclude(PaperAbstract=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.exclude(PaperAbstract=ow)

                elif w['type'] == '3':
                    res = res.exclude(PaperAuthors=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.exclude(PaperAuthors=ow)

                elif w['type'] == 'PaperOrg':
                    res = res.exclude(PaperOrg=w['words'])
                    if radio:
                        ow = translate_by_api(w['words'])
                        if ow != '':
                            res = res.exclude(PaperOrg=ow)

            else:
                pass

    return res


def search_words(request):
    search_key = request.GET.get('keyWords')
    try:
        page = int(request.GET.get('page'))  # 页数
    except Exception:
        page = 1

    try:
        per_page = int(request.GET.get('PerPage'))  # 每页的数量
    except Exception:
        per_page = 10

    # 0 默认 1 时间 2 被引次数
    sort = request.GET.get('sort')
    # 奇数 降序  偶数 升序
    howToSort = request.GET.get('howToSort')

    start_year = int(request.GET.get('dateStart'))
    end_year = int(request.GET.get('dateEnd'))
    type = request.GET.get('type')

    radio = True if request.GET.get('Radio') == 'true' else False  # 中英扩展 false true

    sk = json.loads(search_key)

    # if exists_in_redis(sk):
    #    pass
    # search from redis
    # ...

    # search by elasticsearch index
    t1 = time.time()
    qs = SearchQuerySet()
    res = search_el_indexes(qs, sk, radio, type)

    num = res.count()
    if sort == 1:
        if howToSort%2 == 0:
            res = res.order_by('-PaperTime')
        else:
            res = res.order_by('PaperTime')
    elif sort == 2:
        if howToSort%2 == 0:
            res = res.order_by('-PaperCitation')
        else:
            res = res.order_by('PaperCitation')

    t2 = time.time()
    print(t2-t1)
    res = res.values('object')[(page - 1) * per_page: page * per_page]
    t3 = time.time()
    print(t3-t2)

    l = []

    if type == 'paper':
        for r in res:
            p = r['object']
            kw = re.sub(r'[\[|\'|\]|,]', '', str(p.PaperKeywords))
            kw = re.sub(r' ', ',', kw)
            j = {
                'link': re.sub(r'[\[|\]|\'| ]', '', p.PaperUrl).split(','),
                'paperId': p.PaperId,
                'title': p.PaperTitle,
                'msg': '' if p.PaperAbstract is None else p.PaperAbstract,
                'author': format_list(p.PaperAuthors),
                'authorOrg': format_list(p.PaperOrg),
                'keywords': kw
            }
            l.append(j)

    elif type == 'project':
        for r in res:
            p = r['object']
            j = {
                'link': [p.ProjectUrl],
                'paperId': p.ProjectId,
                'title': p.ProjectTitle,
                'zhAbstract': p.ZhAbstract,
                'enAbstract': p.EnAbstract,
                'finalAbstract': p.FinalAbstract,
                'author': p.ProjectLeader,
                'authorTitle': p.ProjectLeaderTitle,
                'zhKeywords': p.SubjectHeadingCN,
                'enKeywords': p.SubjectHeadingEN
            }
            l.append(j)
    elif type == 'patent':
        for r in res:
            p = r['object']
            j = {
                'link': [p.PatentUrl],
                'paperId': p.PatentId,
                'title': p.PatentTitle,
                'abstract': '' if p.PatentAbstract is None else p.PatentAbstract,
                'author': p.PatentAuthor,
                'authorOrg': p.PatentCompany,
            }
            l.append(j)

    return JsonResponse({'num': num, 'result': l})


def show_paper_info(request):
    pid = request.POST.get('id')
    uid = request.POST.get('userId')
    type = request.POST.get('type')

    if type == 'paper':
        pl = Paper.objects.filter(PaperId=pid)
        if len(pl) > 0:
            p = pl[0]
            alist = p.PaperAuthors
            olist = p.PaperOrg
            if alist != None:
                alist = alist[:-1].split(",")
            else:
                alist = []

            if olist != None:
                olist = olist[:-1].split(",")
            else:
                olist = []

            authorId = [''] * len(alist)
            aulist = PaperAuthor.objects.filter(PaperId_id=p.PaperId)
            for a in aulist:
                authorId[int(a.ResearcherRank)] = a.ResearcherId_id

            refs = PaperReference.objects.filter(PaperId_id=pid)
            reft = []
            refi = []
            for r in refs:
                reft.append(Paper.objects.get(PaperId=r.RePaperId).PaperTitle)
                refi.append(r.RePaperId_id)

            ct = ''
            if uid == '':
                cs = False
            else:
                c = Collection.objects.filter(UserEmail=pid).filter(PaperId=pid)
                if len(c) > 0:
                    cs = True
                    ct = c.CollectionTime
                else:
                    cs = False

            return JsonResponse({
                'paperId': p.PaperId,
                'title': p.PaperTitle,
                'msg': '' if p.PaperAbstract is None else p.PaperAbstract,
                'author': alist,
                'authorId': authorId,
                'authorOrg': olist,
                'paperDoi': '' if p.PaperDoi is None else p.PaperDoi,
                'link': re.sub(r'[\[|\]|\'| ]', '', p.PaperUrl).split(','),
                'collectionSum': p.CollectionNum,
                'viewSum': p.ReadNum,
                'paperTime': 0 if p.PaperTime is None else p.PaperTime,
                'citation': 0 if p.PaperCitation is None else p.PaperCitation,
                'paperStart': 0 if p.PaperStart is None else p.PaperStart,
                'paperEnd': 0 if p.PaperEnd is None else p.PaperEnd,
                'paperLang': '' if p.PaperLang is None else p.PaperLang,
                'paperVolume': '' if p.PaperVolume is None else p.PaperVolume,
                'paperIssue': '' if p.PaperIssue is None else p.PaperIssue,
                'paperPublisher': '' if p.PaperPublisher is None else p.PaperPublisher,
                'paperFos': [] if p.PaperFos is None else re.sub(r'[\[|\]|\'| ]', '', p.PaperFos).split(','),
                'paperVenue': '' if p.PaperVenue is None else p.PaperVenue,
                'keywords': re.sub(r'[\[|\'|\]]', '', str(p.PaperKeywords)),
                'reference': reft,
                'referenceLink': refi,
                'collectStatus': cs,
                'collectTime': ct
            })
    elif type == 'project':
        pl = Project.objects.filter(ProjectId=pid)
        if len(pl) > 0:
            project = pl[0]

            ct = ''
            if uid == '':
                cs = False
            else:
                c = Collection.objects.filter(UserEmail=pid).filter(ProjectId=pid)
                if len(c) > 0:
                    ct = c.CollectionTime
                    cs = True
                else:
                    cs = False

            return JsonResponse({
                'paperId': pid,
                'title': project.ProjectTitle,
                'zhAbstract': project.ZhAbstract,
                'enAbstract': project.EnAbstract,
                'finalAbstract': project.FinalAbstract,
                'enKeywords': project.SubjectHeadingEN,
                'zhKeywords': project.SubjectHeadingCN,
                'period': project.StudyPeriod,
                'category': project.ProjectCategory,
                'year': project.GrantYear,
                'author': project.ProjectLeader,
                'authorId': '',
                'authorTitle': project.ProjectLeaderTitle,
                'fund': project.Funding,
                'support': project.SupportUnits,
                'collectStatus': cs,
                'collectionSum': project.CollectionNum,
                'viewSum': project.ReadNum,
                'link': [project.ProjectUrl],
                'collectTime': ct,
                'subject': project.Subject
            })
        else:
            pass
    elif type == 'patent':
        pl = Patent.objects.filter(PatentId=pid)
        if len(pl) > 0:
            patent = pl[0]
            ct = ''
            if uid == '':
                cs = False
            else:
                c = Collection.objects.filter(UserEmail=pid).filter(PatentId=pid)
                if len(c) > 0:
                    ct = c.CollectionTime
                    cs = True
                else:
                    cs = False

            return JsonResponse({
                'id': pid,
                'paperId': pid,
                'title': patent.PatentTitle,
                'abstract': patent.PatentAbstract,
                'date': patent.PatentDate,
                'author': patent.PatentAuthor,
                'authorId': '',
                'collectStatus': cs,
                'collectionSum': patent.CollectionNum,
                'viewSum': patent.ReadNum,
                'link': [patent.PatentUrl],
                'collectTime': ct,
                'institution': patent.PatentCompany
            })
        else:
            pass


def search_authors(request):
    search_name = str(request.GET.get('name'))
    try:
        page = int(request.GET.get('page'))  # 页数
    except Exception:
        page = 1
    try:
        per_page = int(request.GET.get('PerPage'))  # 每页的数量
    except Exception:
        per_page = 10
    order_by = request.GET.get('orderBy')

    radio = True if request.GET.get('Radio') == 'true' else False

    res = SearchQuerySet().using('researcher').filter(text=search_name)
    print(len(res))
    if radio:
        t = translate_by_api(search_name)
        if t != '':
            res = res.using('researcher').filter_or(text=t)
    num = res.count()
    res = res.values('object')[(page - 1) * per_page: page * per_page]
    l = []
    for r in res:
        rh = r['object']
        l.append({
            'id': rh.ResId,
            'name': rh.ResName,
            'ResEmail': rh.ResEmail,
            'CitedNum': rh.CitedNum,
            'LiteratureNum': rh.LiteratureNum,
            'Institution': rh.InstitutionName
        })

    return JsonResponse({'num': num, 'result': l})


def filter_search_words(request):
    pass


def fast_search(request):
    name = request.GET.get('name')
    body = {"query": {"match": {"text": name}}}
    t1 = time.time()
    data = json.loads(requests.get('http://127.0.0.1:9200/paper_index/_search', data=json.dumps(body)).content)
    t2 = time.time()
    print(t2-t1)
    hits = data['hits']
    num = hits['total']
    l = hits['hits']
    res = []
    for i in l:
        id = i['_source']['django_id']
        title = i['_source']['PaperTitle']
        try:
            msg = i['_source']['PaperAbstract']
        except Exception:
            msg = ''
        try:
            author = format_list(i['_source']['PaperAuthors'])
        except Exception:
            author = []
        try:
            org = format_list(i['_source']['PaperOrg'])
        except Exception:
            org = []
        try:
            key = re.sub(r' ', ',', re.sub(r'[\[|\'|\]|,]', '', str(i['_source']['PaperKeywords'])))
        except Exception:
            key = ''
        #try:
            #p = Paper.objects.get(PaperId=id)
        #except Exception:
            #print(id)
            #continue

        res.append({
            #'link': re.sub(r'[\[|\]|\'| ]', '', p.PaperUrl).split(','),
            'paperId': id,
            'title': title,
            'msg': msg,
            'author': author,
            'authorOrg': org,
            'keywords':  key
        })
    t3 = time.time()
    print(t3-t2)
    return JsonResponse({'num': num, 'result': res})

