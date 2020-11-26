from django.http import JsonResponse
from ResModel.models import Institution, Researcher


def getResearchInstitute(request):
    try:
        if request.method == "GET":
            instituteId = request.GET.get('instituteId')
            if instituteId is not None:
                institute = Institution.objects.filter(id=instituteId)
                instituteid = institute.id
                researchers = Researcher.objects.filter(ResCompany=instituteid)
                res = {}
                res["instituteName"] = institute.InsName
                res["InsField"] = institute.InsField
                res["InsIntroduction"] = institute.InsIntroduction
                res["hold"] = researchers.len()
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
