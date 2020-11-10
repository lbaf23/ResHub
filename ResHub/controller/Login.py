from ResModel.models import HubUser

def identity_check(request):
    uid = request.POST.get('userId')
    pwd = request.POST.get('password')
    u = HubUser.objects.filter(UserEmail=uid).filter(UserPassword=pwd)
    return u.__len__() > 0