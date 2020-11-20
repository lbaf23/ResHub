from django.http import JsonResponse


def temp(request):
    res = {}
    list1 = [1, 2, 3, 4]
    list2 = [5, 6, 7, 8]
    res['list1'] = list1
    res['list2'] = list2
    return JsonResponse(res)
