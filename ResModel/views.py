from django.shortcuts import render

from drf_haystack.viewsets import HaystackViewSet
from .serializers import PaperIndexSerializer
from .models import Paper

class PaperSearchViewSet(HaystackViewSet):
    # paper 搜索
    index_models = [Paper]
    serializer_class = PaperIndexSerializer

