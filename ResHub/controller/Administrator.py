import json

from django.http import  HttpResponse,JsonResponse
from ResModel.models import Administrators
from ResModel.models import Review
from ResModel.models import Appeal

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
    Appeal.objects.filter(id=appeal_id).update(AppealState=2)
    succeed=True
    return JsonResponse({'succeed':succeed})


def getList(request):
    if request.method == "GET":
        AppealList0 = Appeal.objects.filter(AppealState= 0 ).order_by("AppealTime")
        AppealList1 = Appeal.objects.filter(AppealState= 1 ).order_by("AppealTime")
        AppealList2 = Appeal.objects.filter(AppealState= 2 ).order_by("AppealTime")
        ReviewList0 = Review.objects.filter(ReviewState= 0 ).order_by("ReviewTime")
        ReviewList1 = Review.objects.filter(ReviewState= 2 ).order_by("ReviewTime")
        ReviewList2 = Review.objects.filter(ReviewState= 3 ).order_by("ReviewTime")
        AppealList0_out = []
        AppealList1_out = []
        AppealList2_out = []
        ReviewList0_out = []
        ReviewList1_out = []
        ReviewList2_out = []
        for i in AppealList0:
            r= {}
            r['AppealState']=i.AppealState
            r['AppealTime'] = i.AppealTime
            r['ResearchId'] = i.ResearchId
            r['UserEmail'] = i.UserEmail
            AppealList0_out.append(r)

        for i in AppealList1:
            r= { }
            r['AppealState']=i.AppealState
            r['AppealTime'] = i.AppealTime
            r['ResearchId'] = i.ResearchId
            r['UserEmail'] = i.UserEmail
            AppealList1_out.append(r)

        for i in AppealList2:
            r= { }
            r['AppealState']=i.AppealState
            r['AppealTime'] = i.AppealTime
            r['ResearchId'] = i.ResearchId
            r['UserEmail'] = i.UserEmail
            AppealList2_out.append(r)

        for i in ReviewList0:
            r= { }
            r['ReviewPath']=i.ReviewPath
            r['UserEmail'] = i.UserEmail
            r['UploadTime'] = i.UploadTime
            r['ReviewState'] = i.ReviewState
            r['ReviewTime'] = i.ReviewTime

            ReviewList0_out.append(r)
        for i in ReviewList1:
            r= { }
            r['ReviewPath']=i.ReviewPath
            r['UserEmail'] = i.UserEmail
            r['UploadTime'] = i.UploadTime
            r['ReviewState'] = i.ReviewState
            r['ReviewTime'] = i.ReviewTime

            ReviewList1_out.append(r)

        for i in ReviewList2:
            r= { }
            r['ReviewPath']=i.ReviewPath
            r['UserEmail'] = i.UserEmail
            r['UploadTime'] = i.UploadTime
            r['ReviewState'] = i.ReviewState
            r['ReviewTime'] = i.ReviewTime

            ReviewList2_out.append(r)

        return JsonResponse({
            "status": 1,
            "AppealList0": AppealList0_out,
            "AppealList1": AppealList1_out,
            "AppealList2": AppealList2_out,
            "ReviewList0": ReviewList0_out,
            "ReviewList1": ReviewList1_out,
            "ReviewList2": ReviewList2_out,
            "message": "返回审核申诉列表成功"
        })

    else:
        return JsonResponse({
          "status": 2,
          "message": "请求方法错误"
        })