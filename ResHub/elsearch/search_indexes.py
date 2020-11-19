from haystack import indexes

from ResModel.models import Paper
class ELLiterature(indexes.SearchIndex, indexes.Indexable):
    # 必须写的字段
    text = indexes.CharField(document=True, use_template=True)

    LitId = indexes.CharField(model_attr='LitId')
    LitTitle = indexes.CharField(model_attr='LitTitle')
    LitAuthor = indexes.CharField(model_attr='LitAuthor')
    PaperTime = indexes.DateField(model_attr='PaperTime')
    PaperCitation = indexes.IntegerField(model_attr='PaperCitation')
    PaperLang = indexes.CharField(model_attr='PaperLang')#语言
    PaperPublisher = indexes.CharField(model_attr='PaperPublisher')
    PaperType = indexes.CharField(model_attr='PaperType')

    def get_model(self):
        # 返回建立索引的模型 数据库表
        return Paper

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(is_delete=False)