from django.http import JsonResponse
from ResModel.models import Researcher, HubUser
from ResModel.models import PaperAuthor, Paper, ProjectAuthor
import re


def getResearchInstitute(request):
    try:
        if request.method == "GET":
            instituteId = request.GET.get('instituteId')
            if (instituteId is not None):
                res = {}
                institute = Researcher.objects.filter(
                    InstitutionName=instituteId).order_by("ResId")
                if(institute is None):
                    return JsonResponse({
                        "status": 0,
                        "message": "Nothing"
                    })
                # insname
                res['insname'] = instituteId

                res['researchers'] = institute.__len__()

                # domain
                for i in institute:
                    if(i is not None):
                        if(i.ResField is not None):
                            res['domain'] = i.ResField
                            break
                        else:
                            res['domain'] = '暂无'
                        break
                    else:
                        return JsonResponse({"error": 'error'})

                resdata = []
                hotData = []
                datas = [0, 0, 0, 0, 0, 0, 0, 0]
                quotes = [0, 0, 0, 0, 0, 0, 0, 0]
                magcount = 0
                confcount = 0
                index = 0

                # 存放学者id
                hotData_temp = []
                for i in institute:
                    res_temp = {}
                    this_reseacher = i
                    resid = i.ResId
                    res_temp['resId'] = this_reseacher.ResId
                    hotData_temp.append(this_reseacher.ResId)
                    if(this_reseacher.ResName.__len__() > 20):
                        res_temp['name'] = this_reseacher.ResName[:20]+'...'
                    else:
                        res_temp['name'] = this_reseacher.ResName
                    # try:
                    #     UserEmail_id = this_reseacher.UserEmail_id
                    #     this_user = HubUser.objects.get(UserEmail=UserEmail_id)
                    #     res_temp['avatar'] = this_user.UserImage
                    #     if(UserEmail_id is None):
                    #         res['mail'] = ''
                    #     else:
                    #         res_temp['mail'] = this_reseacher.UserEmail_id
                    # except Exception as e:
                    res_temp['avatar'] = 'head00.jpg'
                    if(this_reseacher.UserEmail_id is None):
                        res['mail'] = '暂无'
                    else:
                        res_temp['mail'] = this_reseacher.UserEmail_id

                    ResField = this_reseacher.ResField
                    if(ResField is not None):
                        res_temp['domain'] = this_reseacher.ResField
                    else:
                        res_temp['domain'] = '暂无'

                    VisitNum = this_reseacher.VisitNum
                    if(VisitNum is not None):
                        res_temp['viewSum'] = this_reseacher.VisitNum
                    else:
                        res_temp['viewSum'] = 0
                    try:
                        if(this_reseacher.ConcernNum is None):
                            res_temp['collectionSum'] = 0
                        else:
                            res_temp['collectionSum'] = this_reseacher.ConcernNum
                    except Exception as e:
                        print(e)
                        res_temp['collectionSum'] = 0
                    resdata.append(res_temp)
                    index = index + 1
                    if(index == 10):
                        break
                res["resdata"] = resdata

                hot_temp = []
                ind = 0
                confCount = 0
                magCount = 0
                quoted = 0
                papernum = 0
                for i in hotData_temp:
                    paper_temp = PaperAuthor.objects.filter(
                        ResearcherId_id=i)
                    papernum = papernum + paper_temp.__len__()

                for i in hotData_temp:

                    projectauthor = ProjectAuthor.objects.filter(
                        ResearcherId=i).all()
                    confCount = confCount+projectauthor.__len__()

                    try:
                        data_temp = PaperAuthor.objects.get(
                            ResearcherId_id=i)
                    except Exception as e:
                        data_temp = None
                    if(data_temp is not None):
                        res_temp = {}
                        try:
                            paper = Paper.objects.get(
                                PaperId=data_temp.PaperId_id)
                            res_temp['paperId'] = paper.PaperId
                            if(paper.PaperTitle.__len__() > 20):
                                res_temp['title'] = paper.PaperTitle[:20]+'...'
                            else:
                                res_temp['title'] = paper.PaperTitle

                            try:
                                if(paper.PaperAbstract.__len__() > 60):
                                    res_temp['msg'] = paper.PaperAbstract[:60]+'...'
                                else:
                                    res_temp['msg'] = paper.PaperAbstract
                            except Exception as e:
                                res_temp['msg'] = ''

                            if(paper.PaperCitation is None):
                                quoted = quoted
                            else:
                                quoted = quoted + paper.PaperCitation
                            authors = paper.PaperAuthors
                            res_temp['author'] = re.sub(
                                r'[\[|\]|\'| ]', '', authors).split(',')[:-1]
                            authorid = []
                            paper_authors = PaperAuthor.objects.filter(
                                PaperId_id=paper.PaperId)
                            for k in paper_authors:
                                authorid.append(k.ResearcherId_id)
                            res_temp['authorId'] = authorid
                            res_temp['link'] = re.sub(
                                r'[\[|\]|\'| ]', '', paper.PaperUrl).split(',')[0]
                            hotData.append(res_temp)
                        except Exception as e:
                            donothing = 1

                        magCount = papernum
                        projectauthor = ProjectAuthor.objects.filter(
                            ResearcherId_id=i).all()
                        magCount = magCount + projectauthor.__len__()
                    ind = ind + 1
                    if (hotData.__len__() == 5):
                        break

                res['hotdata'] = hotData
                all_have = magCount+confCount
                if(all_have != 0):
                    magpar = str(int(float(magCount)/float(all_have)*100))+'%'
                    confpar = str(
                        int(float(confCount)/float(all_have)*100))+'%'
                else:
                    magpar = '0%'
                    confpar = '0%'
                res['magcount'] = magCount
                res['magpar'] = magpar
                res['confcount'] = confCount
                res['confpar'] = confpar
                res['quoted'] = str(int(quoted*(papernum/5)))
                res['papernum'] = papernum + confCount

                resCount = []
                quoCount = []
                for i in datas:
                    resCount.append(str(i))
                for i in quotes:
                    quoCount.append(str(i))
                res['rescount'] = resCount
                res['quocount'] = quoCount

                return JsonResponse(res)
            else:
                return JsonResponse({
                    "status": 2,
                    "message": "请求参数错误"
                })
        else:
            return JsonResponse({
                "status": 3,
                "message": "请求方法错误"
            })
    except Exception as e:
        return JsonResponse({
            "status": 4,
            "message": str(e)
        })
