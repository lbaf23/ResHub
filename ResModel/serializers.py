from rest_framework import serializers
from .models import Paper
from drf_haystack.serializers import HaystackSerializer
from .search_indexes import PaperIndex

class PaperSerializer(serializers.ModelSerializer):
    # paper序列化
    class Meta:
        model = Paper
        fields = (
            'LitTitle',
            'PaperTime',
            'PaperCitation',
            'PaperLang',
            'PaperIssue',
            'PaperPublisher',
            'PaperType',
            'LitType'
        )

class PaperIndexSerializer(HaystackSerializer):
    # 索引结果数据序列化器
    object = PaperSerializer(read_only=True)

    class Meta:
        index_classes = [PaperIndex]

        fields = (
            'text',
            'object',
        )