from . import search_indexes

def search_keywords(request):
    w = request.GET.get('keyword')
    # 搜索
