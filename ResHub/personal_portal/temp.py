from django.http import JsonResponse


def temp(request):
    res = {}
    list1 = [1, 2, 3, 4]
    list2 = [5, 6, 7, 8]
    res['1'] = list1
    res['2'] = list2
    list = {}
    node = {}
    node.append(list1)
    node.append(list2)
    res.append(node)
    return JsonResponse(res)
