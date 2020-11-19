from django.http import JsonResponse
from ResModel.models import HubUser, Researcher, Institution


def getPersonalPortal(request):
    try:
        res = {}
        if request.method == "GET":
            userId = request.GET.get('userId')
            if userId is not None:
                # temp1记录从HubUser得到的结果
                temp1 = HubUser.objects.filter(UserEmail=userId).first()
                # temp2记录从Researcher得到的结果
                temp2 = Researcher.objects.filter(UserEmail=userId).first()
                # temp3记录从
                res['userName'] = temp1.UserName
                if(temp2 is not None):
                    res['realName'] = temp2.ResName
                    res['instituteId'] = temp2.ResCompany
                    res['researchInstitute'] = (
                        Institution.objects.filter(id=temp2.temp2.ResCompany).first).InsName
                res['perosonCommunication'] = temp1.UserEmail
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
