from django.http import JsonResponse
from ResModel.models import HubUser, Researcher, Institution, Relationship, Concern


def getPersonalPortal(request):
    try:
        res = {}
        if request.method == "GET":
            userId = request.GET.get('userId')
            resId = request.GET.get('resId')
            if ((userId is not None) and (resId is not None)):
                # temp2记录从Researcher得到的结果
                temp2 = Researcher.objects.filter(ResEmail=resId).first()

                if(temp2 is not None):
                    res['realName'] = temp2.ResName
                    res['ResField'] = temp2.ResField
                    res['InsName'] = temp2.ResCompany.InsName
                    res['ResCompany'] = temp2.ResCompany.id
                    res['ResEmail'] = temp2.ResEmail
                    res['CitedNum'] = temp2.CitedNum
                    res['literatureNum'] = temp2.LiteratureNum
                    res['visitnum'] = temp2.VisitNum
                    coopList = []
                    temp = temp2.ResId
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

                    if(temp2.IsClaim == False):
                        res['IsClaim'] = False
                    else:
                        res['IsClaim'] = True
                    temp6 = Concern.objects.filter(
                        UserEmail=userId, ResearchId=temp2.ResId).first()
                    if(temp6 is not None):
                        res['isFollowing'] = True
                    else:
                        res['isFollowing'] = False
                    if(temp2.UserEmail == userId):
                        res['myPortal'] = True
                    else:
                        res['myPortal'] = False
                    res['visitNum'] = temp2.VisitNum
                    res['followNum'] = Concern.objects.filter(
                        ResearchId=temp2.ResId).all().__len__()
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
