from django.http import JsonResponse
from ResModel.models import Institution, Researcher


def getDaGongRen(request):
    try:
        res = {}
        if request.method == "Get":
            instituteId = request.GET.get('instituteId')
            if instituteId is not None:
                temp = Researcher.objects.filter(ResCompany=instituteId).all()
                str_temp_1 = 1
                str_temp_2 = 'list'
                for i in temp:
                    i = i+1
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
