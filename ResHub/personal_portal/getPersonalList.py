from django.http import JsonResponse
from ResModel.models import Patent, Researcher, PatentAuthor, PaperAuthor, Paper


def getPersonalList(request):
    try:
        if request.method == "GET":
            userId = request.GET.get('userId')
            if userId is not None:
                researcher = Researcher.objects.filter(
                    UserEmail=userId).first()
                researcher_id = researcher.ResId
                len = 0
                res = {}
                # 专利
                patent_author = PaperAuthor.objects.filter(
                    ResearcherId=researcher_id)
                patents = []
                for i in patent_author:
                    patentid = i.PatentId
                    patent = Patent.objects.filter(PatentId=patentid)
                    list = {}
                    list["type"] = 1
                    list["id"] = patent.PatentId
                    list["from"] = patent.PatentUrl
                    list["PatentTitle"] = patent.PatentTitle
                    patents.append(list)
                # 论文
                paper_author = PaperAuthor.objects.filter(
                    ResearcherId=researcher_id)
                papers = []
                for i in paper_author:
                    paper_author
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
