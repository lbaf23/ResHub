import json

from django.http import JsonResponse

from ResModel.models import Browse
from ResModel.models import HubUser
from ResModel.models import Paper
from ResModel.models import Patent
from ResModel.models import Project

def browse_history(request):
    if request.method == "GET":
        userEmailId = request.GET.get("UserEmail")
        if userEmailId is not None:
            History = Browse.objects.filter(UserEmail_id=userEmailId).order_by("BrowseTime")
            HistoryList = list(History)
            retPaperUrlList = []
            retPaperTitleList = []
            retTimeList = []
            if len(HistoryList)==0:
                return JsonResponse({
                    "status": 4,
                    "Timelist": retTimeList,
                    "PaperUrlList" : retPaperUrlList,
                    "PaperTitleList" : retPaperTitleList,
                    "message": "列表为空"
                })

            for i in HistoryList:
                paper = Paper.objects.filter(PaperId= i.PaperId_id).first()
                retPaperUrlList.append(paper.PaperUrl)
                retPaperTitleList.append(paper.PaperTitle)
                retTimeList.append(i.BrowseTime)
            return JsonResponse({
                "status": 1,
                "Timelist": retTimeList,
                "PaperUrlList" : retPaperUrlList,
                "PaperTitleList" : retPaperTitleList,
                "message": "已经返回浏览记录列表",
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

def add_browse_history(request):
    user_id = request.POST.get('userId')
    bro_id = request.POST.get('paperId')
    bro_type = int(request.POST.get('type'))
    succeed = True
    user = HubUser.objects.get(UserEmail=user_id)
    if bro_type == 1:
        paper = Paper.objects.get(PaperId=bro_id)
        u = Browse(PaperId=paper,UserEmail=user,BrowseType=1)
        u.save()
        read_num = Paper.objects.get(PaperId=bro_id).ReadNum
        Paper.objects.filter(PaperId=bro_id).update(ReadNum=read_num+1)
    elif bro_type == 3:
        print(bro_id)
        print(bro_type)
        patent = Patent.objects.get(PatentId=bro_id)
        u = Browse(PatentId=patent,UserEmail=user,BrowseType=2)
        u.save()
        read_num = Patent.objects.get(PatentId=bro_id).ReadNum
        Patent.objects.filter(PatentId=bro_id).update(ReadNum = read_num+1)
    elif bro_type == 2:
        project = Project.objects.get(ProjectId=bro_id)
        u = Browse(ProjectId=project,UserEmail=user,BrowseType=3)
        u.save()
        read_num = Project.objects.get(ProjectId=bro_id).ReadNum
        Project.objects.filter(ProjectId=bro_id).update(ReadNum = read_num+1)
    return JsonResponse({'succeed':succeed})

def add_view_num(request):
    paper_id = request.GET.get('paperId')
    bro_type = int(request.GET.get('type'))
    succeed = True
    if bro_type == 1:
        read_num = Paper.objects.get(PaperId=paper_id).ReadNum
        Paper.objects.filter(PaperId=paper_id).update(ReadNum=read_num+1)
    elif bro_type == 2:
        read_num = Patent.objects.get(PatentId=paper_id).ReadNum
        Patent.objects.filter(PatentId=paper_id).update(ReadNum = read_num+1)
    elif bro_type == 3:
        read_num = Project.objects.get(ProjectId=paper_id).ReadNum
        Project.objects.filter(ProjectId=paper_id).update(ReadNum = read_num+1)
    return JsonResponse({'succeed':succeed})