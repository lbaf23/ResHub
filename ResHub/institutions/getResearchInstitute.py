from django.http import JsonResponse
from ResModel.models import Institution, Researcher, ResInstitution, HubUser
from ResModel.models import Concern, Collection, PaperAuthor, Paper, ProjectAuthor


def author_array(authors):
    temp = []
    len = authors.__len__()
    index1 = 0
    index2 = authors.find(',', index1+1)
    if(index2 == -1):
        temp.append(authors[index1:len])
    index1 = index2
    index2 = authors.find(',', index1+1)
    while((index2 < len-1) and (index1 != -1)) and (index2 != -1):
        temp.append(authors[index1:index2])
        index1 = index2
        index2 = authors.find(',', index1+1)
        if(index2 == -1):
            break
    return temp


def getResearchInstitute(request):
    try:
        if request.method == "GET":
            instituteId = request.GET.get('instituteId')
            if (instituteId is not None):
                res = {}
                institute = Institution.objects.get(id=instituteId)
                if(institute is None):
                    return JsonResponse({
                        "status": 0,
                        "message": "Nothing"
                    })
                # insname
                insname = institute.InsName
                res['insname'] = insname

                # domain
                res['domain'] = institute.InsField

                # reseachers
                reseachers = ResInstitution.objects.filter(
                    InstitutionId=instituteId).all()
                res['researchers'] = str(reseachers.__len__())

                resdata = []
                hotData = []
                datas = [0, 0, 0, 0, 0, 0, 0, 0]
                quotes = [0, 0, 0, 0, 0, 0, 0, 0]
                magcount = 0
                confcount = 0
                index = 0
                hotData_temp = []
                for i in reseachers:
                    res_temp = {}
                    this_reseacher = Researcher.objects.get(i.ResId)
                    resid = i.ResId.ResId
                    res_temp['resid'] = i.ResId.ResId
                    hotData_temp.append(i.ResId.ResId)
                    res_temp['name'] = i.ResId.ResName
                    res_temp['mail'] = i.ResId.UserEmail.UserEmail
                    res_temp['domain'] = i.ResId.ResField
                    res_temp['viewsum'] = i.ResId.VisitNum
                    try:
                        collection = Collection.objects.filter(
                            UserEmail=i.ResId.UserEmail.UserEmail).all()
                        if(collection.__len__() == 0):
                            res_temp['collectstatus'] = True
                            res_temp['collectionsum'] = collection.__len__()
                        else:
                            res_temp['collectstatus'] = False
                            res_temp['collectionsum'] = 0
                    except Exception as e:
                        print(e)
                        res_temp['collectstatus'] = False
                        res_temp['collectionsum'] = 0
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
                    papernum = papernum + PaperAuthor.objects.filter(
                        ResearcherId=i).all().__len__()

                    projectauthor = ProjectAuthor.objects.filter(
                        ResearcherId=i).all()
                    confCount = confCount+projectauthor.__len__()

                    data_temp = PaperAuthor.objects.get(ResearcherId=i)
                    if(data_temp is not None):
                        res_temp = {}
                        res_temp['paperid'] = data_temp.PaperId.PaperId
                        res_temp['title'] = data_temp.PaperId.PaperTitle
                        res_temp['msg'] = data_temp.PaperId.PaperAbstract
                        quoted = quoted+data_temp.PaperId.PaperCitation
                        authors = data_temp.PaperId.PaperAuthors
                        res_temp['author'] = author_array(authors)
                        authorid = []
                        authorid.append(i)
                        res_temp['authorid'] = authorid
                        res_temp['link'] = data_temp.PaperId.PaperUrl
                        hotData.append(res_temp)

                        papersid = PaperAuthor.objects.filter(
                            ResearcherId=1).all()
                        for j in papersid:
                            year = j.PaperId.PaperTime
                            index = 8 - (2020-year)
                            if(index < 0):
                                continue
                            datas[index] = datas[index] + 1
                            quotes[index] = quotes[index] + \
                                j.PaperId.PaperCitation
                        magCount = magCount + papersid.__len__()
                        projectauthor = ProjectAuthor.objects.filter(
                            ResearcherId=i).all()
                        magCount = magCount + projectauthor.__len__()
                    ind = ind + 1
                    if (ind == 5):
                        break
                res['hotdata'] = hotData
                all_have = magCount+confCount
                magpar = str(int(float(magCount)/float(all_have)*100))+'%'
                confpar = str(
                    int(float(confCount)/float(all_have)*100))+'%'
                res['magcount'] = magCount
                res['magpar'] = magpar
                res['confcount'] = confCount
                res['confpar'] = confpar
                res['quoted'] = str(quoted)
                res['papernum'] = str(papernum)

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
