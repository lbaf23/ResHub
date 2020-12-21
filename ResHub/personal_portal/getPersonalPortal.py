from django.http import JsonResponse
from ResModel.models import HubUser, Researcher, Relationship, Collection, Institution
from ResModel.models import ProjectAuthor, Concern, ResInstitution, PaperAuthor, Paper
import re


def getPersonalPortal(request):
    try:
        if request.method == "GET":
            userId = request.GET.get('userId')
            resId = request.GET.get('resId')
            if ((userId is not None) and (resId is not None)):

                researcher = Researcher.objects.get(ResId=resId)
                try:
                    institution_id = researcher.ResCompany_id
                except Exception as e:
                    print(str(e))
                    institution_id = None

                if(researcher is not None):

                    res = {}
                    res['authorid'] = resId
                    # is_have
                    try:
                        is_have = Researcher.objects.get(UserEmail_id=userId)
                        if(is_have is not None):
                            res['ishave'] = True
                        else:
                            res['ishave'] = False
                    except Exception as e:
                        print(str(e))
                        res['ishave'] = False

                    # visitNum
                    res['visitnum'] = researcher.VisitNum

                    # 浏览量加一
                    visitnumber = researcher.VisitNum
                    Researcher.objects.filter(ResId=resId).update(
                        VisitNum=visitnumber+1)

                    # avatar
                    try:
                        keyword_email = researcher.UserEmail_id
                        if(keyword_email is not None):
                            keyword_hubuser = HubUser.objects.get(
                                UserEmail=keyword_email)
                            res['avatar'] = keyword_hubuser.UserImage
                        else:
                            res['avatar'] = 'head00.jpg'
                    except Exception as e:
                        print(str(e))
                        res['avatar'] = 'head00.jpg'

                    # isClaimed
                    res['isclaimed'] = researcher.IsClaim

                    # isFollowing
                    try:
                        concern = Concern.objects.get(
                            UserEmail_id=userId, ResearchId_id=researcher.ResId)
                        if(concern is not None):
                            res['isfollowing'] = True
                        else:
                            res['isfollowing'] = False
                    except Exception as e:
                        print(str(e))
                        res['isfollowing'] = False

                    # isMyPortal
                    try:
                        if(researcher.UserEmail_id == userId):
                            res['ismyportal'] = True
                        else:
                            res['ismyportal'] = False
                    except Exception as e:
                        print(str(e))
                        res['ismyportal'] = False

                    # followNum
                    try:
                        follow = researcher.ConcernNum
                        if(follow is None):
                            res['follownum'] = 0
                        else:
                            res['follownum'] = follow
                    except Exception as e:
                        print(str(e))
                        res['follownum'] = 0

                    # realName
                    res['realname'] = researcher.ResName

                    # insName
                    try:
                        institutionid = institution_id
                        if(institution_id is not None):
                            res['insname'] = institutionid
                        else:
                            res['insname'] = ""
                    except Exception as e:
                        print(str(e))
                        res['insname'] = ""

                    # insId
                    try:
                        if(institution_id is not None):
                            res['insid'] = institution_id
                        else:
                            res['insid'] = ""
                    except Exception as e:
                        print(str(e))
                        res['insid'] = ""

                    # mail
                    if(researcher.ResEmail is not None):
                        res['mail'] = researcher.ResEmail
                    elif(researcher.UserEmail_id is not None):
                        res['mail'] = researcher.UserEmail_id
                    else:
                        res['mail'] = ""

                    # resField
                    if(researcher.ResField is not None):
                        res['resfield'] = researcher.ResField
                    else:
                        res['resfield'] = ""

                    # 一堆东西
                    try:
                        papersid = PaperAuthor.objects.filter(
                            ResearcherId_id=resId).all()
                        datas = [0, 0, 0, 0, 0, 0, 0, 0]
                        quotes = [0, 0, 0, 0, 0, 0, 0, 0]
                        tabledata = []
                        quoteNum = 0
                        for i in papersid:
                            res_temp = {}
                            try:
                                paper = Paper.objects.get(PaperId=i.PaperId_id)
                            except Exception as e:
                                print(str(e))
                                continue
                            res_temp['paperId'] = i.PaperId_id
                            if(paper.PaperTitle.__len__() > 30):
                                res_temp['title'] = paper.PaperTitle[:30]+'...'
                            else:
                                res_temp['title'] = paper.PaperTitle
                            if(paper.PaperAbstract.__len__() > 60):
                                res_temp['msg'] = paper.PaperAbstract[:60]+'...'
                            else:
                                res_temp['msg'] = paper.PaperAbstract
                            res_temp['collectionSum'] = paper.CollectionNum
                            res_temp['link'] = re.sub(
                                r'[\[|\]|\'| ]', '', paper.PaperUrl).split(',')[0]
                            res_temp['type'] = '文章'
                            try:
                                pp = paper.CollectionNum
                                if(pp == 0):
                                    res_temp['collectStatus'] = True
                                else:
                                    res_temp['collectStatus'] = False
                            except Exception as e:
                                print(e)
                                res_temp['collectStatus'] = False
                            tabledata.append(res_temp)
                            year = paper.PaperTime
                            index = (8 - (2020-year)) % 5
                            # if(index < 0):
                            #     continue
                            datas[index] = datas[index] + 1
                            quotes[index] = quotes[index] + paper.PaperCitation
                            quoteNum = quoteNum + paper.PaperCitation
                        resCount = []
                        quoCount = []
                        for i in datas:
                            resCount.append(str(i))
                        for i in quotes:
                            quoCount.append(str(i))
                        res['rescount'] = resCount
                        res['quocount'] = quoCount
                        res['quotenum'] = str(quoteNum)
                        res['tabledata'] = tabledata
                    except Exception as e:
                        print(str(e))
                        res['rescount'] = [
                            '0', '0', '0', '0', '0', '0', '0', '0']
                        res['quocount'] = [
                            '0', '0', '0', '0', '0', '0', '0', '0']
                        res['quotenum'] = '0'
                        res['tabledata'] = []

                    # magCount ....
                    try:
                        projectauthor = ProjectAuthor.objects.filter(
                            ResearcherId=resId).all()
                        confCount = projectauthor.__len__()
                        magCount = researcher.LiteratureNum
                        all_have = projectauthor.__len__() + researcher.LiteratureNum
                        magpar = str(
                            int(float(magCount)/float(all_have)*100))+'%'
                        confpar = str(
                            int(float(confCount)/float(all_have)*100))+'%'
                        res['magcount'] = magCount
                        res['magpar'] = magpar
                        res['confcount'] = confCount
                        res['confpar'] = confpar
                        res['papernum'] = magCount+confCount
                    except Exception as e:
                        print(str(e))
                        res['magcount'] = 0
                        res['magpar'] = '0%'
                        res['confcount'] = 0
                        res['confpar'] = '0%'
                        res['papernum'] = 0

                    # coopData
                    try:
                        count = 0
                        coopData = []
                        relationship = Relationship.objects.filter(
                            ResearchId1=resId).all()
                        for i in relationship:
                            if(coopData.__len__() == 5):
                                break
                            res_temp = {}
                            reseacher_relation_temp = i.ResearchId2_id
                            reseacher_relation = Researcher.objects.get(
                                ResId=reseacher_relation_temp)
                            email = reseacher_relation.UserEmail_id
                            try:
                                if(email is not None):
                                    user_temp = HubUser.objects.get(
                                        UserEmail=email)
                                    res_temp['avatar'] = user_temp.UserImage
                                else:
                                    res_temp['avatar'] = user_temp.UserImage
                            except Exception as e:
                                print(str(e))
                                res_temp['avatar'] = 'head00.jpg'
                            resinstitution_temp = ResInstitution.objects.get(
                                ResId=reseacher_relation.ResId)
                            institution_this = Institution.objects.get(
                                id=resinstitution_temp.InstitutionId)
                            res_temp['name'] = reseacher_relation.ResName
                            res_temp['institute'] = institution_this.InsName

                            res_temp['link'] = reseacher_relation.ResId
                            coopData.append(res_temp)
                        if(coopData.__len__() == 5):
                            donothing = 1
                        else:
                            relationship = Relationship.objects.filter(
                                ResearchId2=resId).all()
                            for i in relationship:
                                if(coopData.__len__() == 5):
                                    break
                                res_temp = {}
                                reseacher_relation_temp = i.ResearchId1_id
                                reseacher_relation = Researcher.objects.get(
                                    ResId=reseacher_relation_temp)
                                email = reseacher_relation.UserEmail_id
                                try:
                                    if(email is not None):
                                        user_temp = HubUser.objects.get(
                                            UserEmail=email)
                                        res_temp['avatar'] = user_temp.UserImage
                                    else:
                                        res_temp['avatar'] = 'head00.jpg'
                                except Exception as e:
                                    print(str(e))
                                    res_temp['avatar'] = 'head00.jpg'
                                institution_this = Institution.objects.get(
                                    id=reseacher_relation.ResCompany_id)
                                if(institution_this is not None):
                                    res_temp['name'] = reseacher_relation.ResName
                                    res_temp['institute'] = institution_this.InsName
                                else:
                                    res_temp['name'] = ""
                                    res_temp['institute'] = ""
                                res_temp['link'] = reseacher_relation.ResId
                                coopData.append(res_temp)

                        res['coopdata'] = coopData
                    except Exception as e:
                        print(str(e))
                        res['coopdata'] = []

                    return JsonResponse(res)
                else:
                    return JsonResponse({
                        "status": 2,
                        "message": "请求参数错误"
                    })
            else:
                return JsonResponse({
                    "status": 3,
                    "message": "请求参数错误"
                })
        else:
            return JsonResponse({
                "status": 4,
                "message": "请求方法错误"
            })
    except Exception as e:
        print(str(e))
        return JsonResponse({
            "status": 5,
            "message": str(e)
        })
