from django.http import JsonResponse
from ResModel.models import HubUser, Researcher, Institution, Relationship, Concern


def getPersonalPortal(request):
    try:
        if request.method == "GET":
            userId = request.GET.get('userId')
            resId = request.GET.get('resId')
            if ((userId is not None) and (resId is not None)):

                researcher = Researcher.objects.filter(ResEmail=resId).first()
                hubuser = HubUser.objects.filter(UserEmail=userId).first()
                if((researcher is not None) and (hubuser is not None)):
                    res = {}
                    res['realName'] = researcher.ResName
                    res['isClaimed'] = researcher.IsClaim
                    res['InsName'] = researcher.ResCompany.InsName
                    res['ResCompany'] = researcher.ResCompany.id
                    res['ResEmail'] = researcher.ResEmail
                    res['CitedNum'] = researcher.CitedNum
                    res['literatureNum'] = researcher.LiteratureNum
                    res['visitnum'] = researcher.VisitNum
                    coopList = []
                    temp = researcher.ResId
                    temp3 = Relationship.objects.filter(ResearchId1=temp).all()
                    temp4 = Relationship.objects.filter(ResearchId2=temp).all()
                    len = 0
                    for i in temp3:
                        temp5 = i.ResearchId2
                        coopList.append(temp5.ResName)
                        len = len+1
                        if(len == 5):
                            break
                    for i in temp4:
                        if(len == 5):
                            break
                        temp5 = i.ResearchId1
                        coopList.append(temp5.ResName)
                        len = len+1
                    res['coopList'] = coopList

                    if(researcher.IsClaim == False):
                        res['IsClaim'] = False
                    else:
                        res['IsClaim'] = True
                    temp6 = Concern.objects.filter(
                        UserEmail=userId, ResearchId=temp2.ResId).first()
                    if(temp6 is not None):
                        res['isFollowing'] = True
                    else:
                        res['isFollowing'] = False
                    if(researcher.UserEmail == userId):
                        res['myPortal'] = True
                    else:
                        res['myPortal'] = False
                    res['visitNum'] = researcher.VisitNum
                    res['followNum'] = Concern.objects.filter(
                        ResearchId=researcher.ResId).all().__len__()
                    return JsonResponse({
                        "status": 1,
                        "message": res
                    })
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
        return JsonResponse({
            "status": 5,
            "message": str(e)
        })
