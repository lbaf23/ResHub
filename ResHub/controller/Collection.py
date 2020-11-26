from django.http import  HttpResponse,JsonResponse
from ResModel.models import Collection
from ResModel.models import HubUser
from ResModel.models import Paper
from ResModel.models import Patent
from ResModel.models import Project
import json

def add_collection(request):
    user_id = request.POST.get('userId')
    paper_id = request.POST.get('paperId')
    paper_id
    succeed = True
    user = HubUser.objects.get(UserEmail=user_id)
    paper = Paper.objects.get(PaperId=paper_id)
    u = Collection(LiteratureId=paper,UserEmail=user)
    u.save()
    return JsonResponse({'succeed':succeed})

def del_collection(request):
    user_id = request.POST.get('userId')
    paper_id = request.POST.get('paperId')
    succeed = True
    user = HubUser.objects.get(UserEmail=user_id)
    paper = Paper.objects.get(PaperId=paper_id)
    Collection.objects.filter(PaperId=paper,UserEmail=user).delete()
    return JsonResponse({'succeed':succeed})

