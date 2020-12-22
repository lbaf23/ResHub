from haystack import indexes
from .models import Paper, Project, Patent, Researcher


class PaperIndex(indexes.SearchIndex, indexes.Indexable):
    # 必须写的字段
    text = indexes.CharField(document=True, use_template=True)

    PaperCitation = indexes.IntegerField(model_attr='PaperCitation', null=True)
    CollectionNum = indexes.IntegerField(model_attr='CollectionNum', null=True)
    ReadNum = indexes.IntegerField(model_attr='ReadNum', null=True)
    PaperTime = indexes.IntegerField(model_attr='PaperTime', null=True)
    PaperAbstract = indexes.CharField(model_attr='PaperAbstract', null=True)
    PaperKeywords = indexes.CharField(model_attr='PaperKeywords', null=True)
    PaperAuthors = indexes.CharField(model_attr='PaperAuthors', null=True)
    PaperTitle = indexes.CharField(model_attr='PaperTitle', null=True)
    PaperOrg = indexes.CharField(model_attr='PaperOrg', null=True)

    def get_model(self):
        # 返回建立索引的模型 数据库表
        return Paper

    def index_queryset(self, using='paper_index'):
        return self.get_model().objects.filter()


class ProjectIndex(indexes.SearchIndex, indexes.Indexable):
    # 必须写的字段
    text = indexes.CharField(document=True, use_template=True)

    CollectionNum = indexes.IntegerField(model_attr='CollectionNum', null=True)
    ReadNum = indexes.IntegerField(model_attr='ReadNum', null=True)
    GrantYear = indexes.IntegerField(model_attr='GrantYear', null=True)
    ProjectTitle = indexes.CharField(model_attr='ProjectTitle', null=True)
    Subject = indexes.CharField(model_attr='Subject', null=True)
    ProjectLeader = indexes.CharField(model_attr='ProjectLeader', null=True)
    SubjectHeadingCN = indexes.CharField(model_attr='SubjectHeadingCN', null=True)
    SubjectHeadingEN = indexes.CharField(model_attr='SubjectHeadingEN', null=True)
    ZhAbstract = indexes.CharField(model_attr='ZhAbstract', null=True)
    EnAbstract = indexes.CharField(model_attr='EnAbstract', null=True)
    FinalAbstract = indexes.CharField(model_attr='FinalAbstract', null=True)
    SupportUnits = indexes.CharField(model_attr='SupportUnits', null=True)

    def get_model(self):
        # 返回建立索引的模型 数据库表
        return Project

    def index_queryset(self, using='project_index'):
        return self.get_model().objects.filter()


class PatentIndex(indexes.SearchIndex, indexes.Indexable):
    # 必须写的字段
    text = indexes.CharField(document=True, use_template=True)

    CollectionNum = indexes.IntegerField(model_attr='CollectionNum', null=True)
    ReadNum = indexes.IntegerField(model_attr='ReadNum', null=True)
    PatentDate = indexes.DateField(model_attr='PatentDate', null=True)
    PatentTitle = indexes.CharField(model_attr='PatentTitle', null=True)
    PatentAbstract = indexes.CharField(model_attr='PatentAbstract', null=True)
    PatentAuthor = indexes.CharField(model_attr='PatentAuthor', null=True)
    PatentCompany = indexes.CharField(model_attr='PatentCompany', null=True)

    def get_model(self):
        # 返回建立索引的模型 数据库表
        return Patent

    def index_queryset(self, using='patent_index'):
        return self.get_model().objects.filter()


class ResearcherIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    LiteratureNum = indexes.IntegerField(model_attr='LiteratureNum', null=True)
    CitedNum = indexes.IntegerField(model_attr='CitedNum', null=True)

    def get_model(self):
        # 返回建立索引的模型 数据库表
        return Researcher

    def index_queryset(self, using='researcher_index'):
        return self.get_model().objects.filter()
