from haystack import indexes
from .models import Paper

class PaperIndex(indexes.SearchIndex, indexes.Indexable):
    # 必须写的字段
    text = indexes.CharField(document=True, use_template=True)

    PaperAbstract = indexes.CharField(model_attr='PaperAbstract', null=True)
    PaperFos = indexes.CharField(model_attr='PaperFos', null=True)
    PaperKeywords = indexes.CharField(model_attr='PaperKeywords', null=True)

    def get_model(self):
        # 返回建立索引的模型 数据库表
        return Paper

    def index_queryset(self, using=None):
        return self.get_model().objects.filter()
