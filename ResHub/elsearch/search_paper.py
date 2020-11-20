from drf_haystack.viewsets import HaystackViewSet
from ResModel.serializers import PaperIndexSerializer
from ResModel.models import Paper

def search_keywords(request):
    # 搜索

    index_models = [Paper]
    serializer_class = PaperIndexSerializer
