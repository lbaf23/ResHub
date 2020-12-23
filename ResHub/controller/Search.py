import json
import re

import requests
from django.http import JsonResponse
from haystack.query import SearchQuerySet

from ResModel.models import PaperAuthor, Project, Paper, PaperReference, Patent, Collection, Researcher
import time
from ResHub.controller.EsMid import Body, translate_by_api


# 检索式解码
def exists_in_redis(s1):
    s1.sort()
    return s1


def format_list(s):
    if s is None:
        return []
    return s.split(',')[:-1]



# boolType {1:AND ; 2:OR ; 3:NOT}
# type {1：主题；2：标题；3：作者；4：关键词；5：摘要; }


def search_patent_index(body, key, radio):
    for w in list(key):
        if not w.__contains__('boolType') or w['boolType'] == '1':
            if w['type'] == '1' or w['type'] == '4':
                body.add_must('text', w['words'], radio)
            elif w['type'] == '2':
                body.add_must('PatentTitle', w['words'], radio)
            elif w['type'] == '5':
                body.add_must('PatentAbstract', w['words'], radio)

            elif w['type'] == '3':
                body.add_must('PatentAuthor', w['words'], radio)
            elif w['type'] == 'PaperOrg':
                body.add_must('PatentCompany', w['words'], radio)

        else:
            if w['boolType'] == '2':
                if w['type'] == '1' or w['type'] == '4':
                    body.add_should('text', w['words'], radio)
                elif w['type'] == '2':
                    body.add_should('PatentTitle', w['words'], radio)
                elif w['type'] == '5':
                    body.add_should('PatentAbstract', w['words'], radio)
                elif w['type'] == '3':
                    body.add_should('PatentAuthor', w['words'], radio)
                elif w['type'] == 'PaperOrg':
                    body.add_should('PatentCompany', w['words'], radio)

            elif w['boolType'] == '3':
                if w['type'] == '1' or w['type'] == '4':
                    body.add_not('text', w['words'], radio)
                elif w['type'] == '2':
                    body.add_not('PatentTitle', w['words'], radio)
                elif w['type'] == '5':
                    body.add_not('PatentAbstract', w['words'], radio)
                elif w['type'] == '3':
                    body.add_not('PatentAuthor', w['words'], radio)
                elif w['type'] == 'PaperOrg':
                    body.add_not('PatentCompany', w['words'], radio)
            else:
                pass

    return body


def search_project_index(body, key, radio):
    for w in list(key):
        if not w.__contains__('boolType') or w['boolType'] == '1':
            if w['type'] == '4':
                body.add_must('SubjectHeadingCN', w['words'], radio)
                body.add_should('SubjectHeadingEN', w['words'], radio)
            elif w['type'] == '1':
                body.add_must('text', w['words'], radio)
            elif w['type'] == '2':
                body.add_must('ProjectTitle', w['words'], radio)
            elif w['type'] == '5':
                body.add_must('ZhAbstract', w['words'], radio)
                body.add_should('EnAbstract', w['words'], radio)
                body.add_should('FinalAbstract', w['words'], radio)

            elif w['type'] == '3':
                body.add_must('ProjectLeader', w['words'], radio)

            elif w['type'] == 'PaperOrg':
                body.add_must('SupportUnits', w['words'], radio)

        else:
            if w['boolType'] == '2':
                if w['type'] == '4':
                    body.add_should('SubjectHeadingCN', w['words'], radio)
                    body.add_should('SubjectHeadingEN', w['words'], radio)

                elif w['type'] == '1':
                    body.add_should('text', w['words'], radio)

                elif w['type'] == '2':
                    body.add_should('ProjectTitle', w['words'], radio)
                elif w['type'] == '5':
                    body.add_should('ZhAbstract', w['words'], radio)
                    body.add_should('FinalAbstract', w['words'], radio)
                    body.add_should('EnAbstract', w['words'], radio)
                elif w['type'] == '3':
                    body.add_should('ProjectLeader', w['words'], radio)

                elif w['type'] == 'PaperOrg':
                    body.add_should('SupportUnits', w['words'], radio)

            elif w['boolType'] == '3':
                if w['type'] == '4':
                    body.add_not('SubjectHeadingCN', w['words'], radio)
                    body.add_not('SubjectHeadingEN', w['words'], radio)

                elif w['type'] == '1':
                    body.add_not('text', w['words'], radio)
                elif w['type'] == '2':
                    body.add_not('ProjectTitle', w['words'], radio)
                elif w['type'] == '5':
                    body.add_not('ZhAbstract', w['words'], radio)
                    body.add_not('EnAbstract', w['words'], radio)
                    body.add_not('FinalAbstract', w['words'], radio)

                elif w['type'] == '3':
                    body.add_not('ProjectLeader', w['words'], radio)
                elif w['type'] == 'PaperOrg':
                    body.add_not('SupportUnits', w['words'], radio)
            else:
                pass

    return body


def search_paper_index(body, key, radio):
    for w in list(key):
        if not w.__contains__('boolType') or w['boolType'] == '1':
            if w['type'] == '4':
                body.add_must('PaperKeywords', w['words'], radio)
            elif w['type'] == '1':
                body.add_must('text', w['words'], radio)

            elif w['type'] == '2':
                body.add_must('PaperTitle', w['words'], radio)

            elif w['type'] == '5':
                body.add_must('PaperAbstract', w['words'], radio)

            elif w['type'] == '3':
                body.add_must('PaperAuthors', w['words'], radio)

            elif w['type'] == 'PaperOrg':
                body.add_must('PaperOrg', w['words'], radio)

        else:
            if w['boolType'] == '2':
                if w['type'] == '4':
                    body.add_should('PaperKeywords', w['words'], radio)

                elif w['type'] == '1':
                    body.add_should('text', w['words'], radio)

                elif w['type'] == '2':
                    body.add_should('PaperTitle', w['words'], radio)

                elif w['type'] == '5':
                    body.add_should('PaperAbstract', w['words'], radio)

                elif w['type'] == '3':
                    body.add_should('PaperAuthors', w['words'], radio)

                elif w['type'] == 'PaperOrg':
                    body.add_should('PaperOrg', w['words'], radio)

            elif w['boolType'] == '3':
                if w['type'] == '4':
                    body.add_should('PaperKeywords', w['words'], radio)

                elif w['type'] == '1':
                    body.add_should('text', w['words'], radio)

                elif w['type'] == '2':
                    body.add_should('PaperTitle', w['words'], radio)

                elif w['type'] == '5':
                    body.add_should('PaperAbstract', w['words'], radio)

                elif w['type'] == '3':
                    body.add_should('PaperAuthors', w['words'], radio)

                elif w['type'] == 'PaperOrg':
                    body.add_should('PaperOrg', w['words'], radio)

            else:
                pass

    return body


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
    try:
        order_by = int(request.GET.get('orderBy'))
    except Exception:
        order_by = 0

    radio = True if request.GET.get('Radio') == 'true' else False

    b = Body()
    b.add_must('text', search_name, radio)
    b.set_from_page(page-1)
    if order_by == 0:
        b.add_sort('LiteratureNum')
    else:
        b.add_sort('CitedNum')

    url = 'http://127.0.0.1:9200/researcher_index/_search'
    body = b.get_body()
    data = json.loads(requests.get(url, data=json.dumps(body)).content)

    hits = data['hits']
    num = hits['total']
    res = hits['hits']
    l=[]
    for r in res:
        id = r['_source']['django_id']
        rh = Researcher.objects.filter(ResId =id)
        l.append({
            'id': rh.ResId,
            'name': rh.ResName,
            'ResEmail': rh.ResEmail,
            'CitedNum': rh.CitedNum,
            'LiteratureNum': rh.LiteratureNum,
            'Institution': rh.InstitutionName
        })

    return JsonResponse({'num': num, 'result': l})


def fast_search(request):
    search_key = json.loads(request.GET.get('keyWords'))
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
    try:
        start_year = int(request.GET.get('dateStart'))
    except Exception:
        start_year = None
    try:
        end_year = int(request.GET.get('dateEnd'))
    except Exception:
        end_year = None
    type = request.GET.get('type')
    radio = True if request.GET.get('Radio') == 'true' else False  # 中英扩展 false true

    if type == 'paper':
        b = search_paper_index(Body(), search_key, radio)
        if start_year and end_year:
            b.add_range('PaperTime', start_year, end_year)
        if sort == 1:
            if howToSort%2 == 0:
                b.add_sort('PaperTime', False)
            else:
                b.add_sort('PaperTime', True)
        elif sort == 2:
            if howToSort%2 == 0:
                b.add_sort('PaperCitation', False)
            else:
                b.add_sort('PaperCitation', True)

        b.set_from_page(page-1)
        b.set_page_size(per_page)

        url = 'http://127.0.0.1:9200/paper_index/_search'
        body = b.get_body()
        data = json.loads(requests.get(url, data=json.dumps(body)).content)

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
            try:
                collectionSum = i['_source']['CollectionNum']
            except Exception:
                collectionSum = 0
            try:
                viewSum = i['_source']['ReadNum']
            except Exception:
                viewSum = 0

            try:
                citation = i['_source']['PaperCitation']
            except Exception:
                citation = 0

            try:
                year = i['_source']['PaperTime']
            except Exception:
                year = 0
            res.append({
                'paperId': id,
                'title': title,
                'msg': msg,
                'author': author,
                'authorOrg': org,
                'keywords':  key,
                'collectionSum': collectionSum,
                'viewSum': viewSum,
                'citation': citation,
                'year': year
            })

        return JsonResponse({'num': num, 'result': res})

    elif type == 'project':
        b = search_project_index(Body(), search_key, radio)
        if start_year and end_year:
            b.add_range('GrantYear', start_year, end_year)
        b.set_from_page(page-1)
        b.set_page_size(per_page)
        if sort == 1:
            if howToSort%2 == 0:
                b.add_sort('GrantYear', False)
            else:
                b.add_sort('GrantYear', True)


        url = 'http://127.0.0.1:9200/project_index/_search'
        body = b.get_body()
        data = json.loads(requests.get(url, data=json.dumps(body)).content)
        hits = data['hits']
        num = hits['total']
        l = hits['hits']
        res = []
        for i in l:
            id = i['_source']['django_id']
            title = i['_source']['ProjectTitle']
            try:
                msg = i['_source']['PaperAbstract']
            except Exception:
                msg = ''
            try:
                zhAbstract = i['_source']['ZhAbstract']
            except Exception:
                zhAbstract = ''
            try:
                enAbstract = i['_source']['EnAbstract']
            except Exception:
                enAbstract = ''
            try:
                finalAbstract = i['_source']['FinalAbstract']
            except Exception:
                finalAbstract = ''

            try:
                author = i['_source']['ProjectLeader']
            except Exception:
                author = ''

            try:
                org = i['_source']['SupportUnits']
            except Exception:
                org = ''

            try:
                zhKeywords = re.sub(r' ', ',', re.sub(r'[\[|\'|\]|,]', '', str(i['_source']['SubjectHeadingCN'])))
            except Exception:
                zhKeywords = ''
            try:
                enKeywords = re.sub(r' ', ',', re.sub(r'[\[|\'|\]|,]', '', str(i['_source']['SubjectHeadingEN'])))
            except Exception:
                enKeywords = ''
            try:
                collectionSum = i['_source']['CollectionNum']
            except Exception:
                collectionSum = 0
            try:
                viewSum = i['_source']['ReadNum']
            except Exception:
                viewSum = 0
            try:
                citation = i['_source']['PaperCitation']
            except Exception:
                citation = 0
            try:
                year = i['_source']['GrantYear']
            except Exception:
                year = 0

            res.append({
                'paperId': id,
                'title': title,
                'zhAbstract': zhAbstract,
                'enAbstract': enAbstract,
                'finalAbstract': finalAbstract,
                'author': author,
                'authorTitle': org,
                'zhKeywords': zhKeywords,
                'enKeywords':enKeywords,
                'collectionSum': collectionSum,
                'viewSum': viewSum,
                'citation': citation,
                'year': year
            })

        return JsonResponse({'num': num, 'result': res})
    elif type == 'patent':
        b = search_patent_index(Body(), search_key, radio)
        if start_year and end_year:
            b.add_range('PatentDate', start_year, end_year)
        b.set_from_page(page-1)
        b.set_page_size(per_page)
        if sort == 1:
            if howToSort%2 == 0:
                b.add_sort('PatentDate', False)
            else:
                b.add_sort('PatentDate', True)

        url = 'http://127.0.0.1:9200/patent_index/_search'
        body = b.get_body()
        data = json.loads(requests.get(url, data=json.dumps(body)).content)

        hits = data['hits']
        num = hits['total']
        l = hits['hits']
        res = []
        for i in l:
            id = i['_source']['django_id']
            title = i['_source']['PatentTitle']
            try:
                abstract = i['_source']['PatentAbstract']
            except Exception:
                abstract = ''
            try:
                author = i['_source']['PatentAuthor']
            except Exception:
                author = ''
            try:
                org = i['_source']['PatentCompany']
            except Exception:
                org = ''
            try:
                collectionSum = i['_source']['CollectionNum']
            except Exception:
                collectionSum = 0
            try:
                viewSum = i['_source']['ReadNum']
            except Exception:
                viewSum = 0
            try:
                citation = i['_source']['PaperCitation']
            except Exception:
                citation = 0
            try:
                year = i['_source']['PatentDate']
            except Exception:
                year = 0

            res.append({
                'paperId': id,
                'title': title,
                'abstract': abstract,
                'author': author,
                'authorOrg': org,
                'collectionSum': collectionSum,
                'viewSum': viewSum,
                'citation': citation,
                'year': year
            })
        return JsonResponse({'num': num, 'result': res})
    else:
        pass
