from django.http import JsonResponse
from ResModel.models import Institution, Researcher


def getDaGongRen(request):
    try:
        if request.method == "GET":
            instituteId = request.GET.get('instituteId')
            if instituteId is not None:
                institute = Institution.objects.filter(id=instituteId).first()
                if(institute is None):
                    return JsonResponse({
                        "status": 0,
                        "message": "Nothing"
                    })
                instituteid = institute.id
                researchers = Researcher.objects.filter(
                    ResCompany=instituteid)
                if(researchers.__len__() == 0):
                    return JsonResponse({
                        "status": 0,
                        "message": "Nothing"
                    })
                list = []
                for i in researchers:
                    temp = {}
                    temp["realName"] = i.ResName
                    temp["personCommunication"] = i.UserEmail.UserEmail
                    temp["personQuote"] = i.CitedNum
                    list.append(temp)

                res = {}
                res["len"] = researchers.__len__()
                res["list"] = list

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
                "message": "请求方法错误"
            })
    except Exception as e:
        return JsonResponse({
            "status": 4,
            "message": str(e)
        })
