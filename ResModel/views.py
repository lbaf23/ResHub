from django.shortcuts import render

from drf_haystack.viewsets import HaystackViewSet
from .serializers import PaperIndexSerializer
from .models import Paper

from rest_framework.pagination import PageNumberPagination
from drf_haystack.filters import HaystackFilter, BaseHaystackFilterBackend

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 20


class PaperSearchViewSet(HaystackViewSet):
    # paper 搜索
    index_models = [Paper]
    serializer_class = PaperIndexSerializer
    pagination_class = StandardResultsSetPagination

