import json

from django.http import  HttpResponse,JsonResponse
from ResModel.models import Administrators
from ResModel.models import Review
from ResModel.models import Appeal,HubUser,Researcher

def reject_review(request):
    review_id=request.GET.get('id')
    Review.objects.filter(id=review_id).update(ReviewState=1)
    succeed=True
    return JsonResponse({'succeed':succeed})
def pass_review(request):
    review_id=request.GET.get('id')
    Review.objects.filter(id=review_id).update(ReviewState=2)
    succeed=True
    return JsonResponse({'succeed':succeed})
def reject_appeal(request):
    appeal_id=request.GET.get('id')
    Appeal.objects.filter(id=appeal_id).update(AppealState=1)
    succeed=True
    return JsonResponse({'succeed':succeed})
def pass_appeal(request):
    appeal_id=request.GET.get('id')
    user=request.GET.get('email')
    resid =request.GET.get('ResId')
    print(resid)
    print(user)
    Appeal.objects.filter(id=appeal_id).update(AppealState=2)
    Researcher.objects.filter(ResId=resid).update(UserEmail=user,IsClaim=1)
    succeed=True
    return JsonResponse({'succeed':succeed})


def getList(request):
    if request.method == "GET":
        AppealList0 = Appeal.objects.filter(AppealState= 0 ).order_by("AppealTime")
        AppealList1 = Appeal.objects.filter(AppealState__in = [1,2]).order_by("AppealTime")
        ReviewList0 = Review.objects.filter(ReviewState= 0 ).order_by("ReviewTime")
        ReviewList1 = Review.objects.filter(ReviewState__in= [1,2]).order_by("ReviewTime")
        AppealList0_out = []
        AppealList1_out = []
        ReviewList0_out = []
        ReviewList1_out = []
        for i in AppealList0:

            r = {}

            user = HubUser.objects.filter(UserEmail=i.UserEmail_id).first()
            researcher = Researcher.objects.filter(ResId=i.ResearchId_id).first()

            r['id'] = str(i.id)
            r['AppealState'] = i.AppealState
            r['AppealTime'] = i.AppealTime
            r['ResearchId'] = str(researcher.ResId)
            r['UserEmail'] = user.UserEmail
            r['content'] = i.content

            AppealList0_out.append(r)

        for i in AppealList1:
            r= {}

            user = HubUser.objects.filter(UserEmail=i.UserEmail_id).first()
            researcher = Researcher.objects.filter(ResId=i.ResearchId_id).first()

            r['id']=str(i.id)
            r['AppealState']= i.AppealState
            r['AppealTime'] = i.AppealTime
            r['ResearchId'] = str(researcher.ResId)
            r['UserEmail'] = user.UserEmail
            r['content'] = i.content

            AppealList1_out.append(r)

        for i in ReviewList0:
            r= { }

            user = HubUser.objects.filter(UserEmail=i.UserEmail_id).first()

            r['id']=str(i.id)
            r['ReviewPath']=i.ReviewPath
            r['UserEmail'] = user.UserEmail
            r['UploadTime'] = i.UploadTime
            r['ReviewState'] = i.ReviewState
            r['ReviewTime'] = i.ReviewTime
            r['content'] = i.content

            ReviewList0_out.append(r)
        for i in ReviewList1:
            r= { }

            user = HubUser.objects.filter(UserEmail=i.UserEmail_id).first()

            r['id']=str(i.id)
            r['ReviewPath']=i.ReviewPath
            r['UserEmail'] = user.UserEmail
            r['UploadTime'] = i.UploadTime
            r['ReviewState'] = i.ReviewState
            r['ReviewTime'] = i.ReviewTime
            r['content'] = i.content

            ReviewList1_out.append(r)

        return JsonResponse({
            "status": 1,
            "AppealList0": AppealList0_out,
            "AppealList1": AppealList1_out,
            "ReviewList0": ReviewList0_out,
            "ReviewList1": ReviewList1_out,
            "message": "返回审核申诉列表成功"
        })

    else:
        return JsonResponse({
          "status": 2,
          "message": "请求方法错误"
        })
