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