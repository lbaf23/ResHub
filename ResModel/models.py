from django.db import models


# manage.py migrate    manage.py makemigrations
# Create your models here.

class HubUser(models.Model):
    UserEmail = models.CharField(max_length=50, primary_key=True)
    UserName = models.CharField(max_length=50, null=True)
    UserPassword = models.CharField(max_length=20)
    UserImage = models.CharField(max_length=50)
    UserIntroduction = models.CharField(max_length=2000, null=True)

class Researcher(models.Model):
    ResId = models.CharField(max_length=50, primary_key=True)
    IsClaim = models.BooleanField()  # 是否认领
    UserEmail = models.OneToOneField('HubUser', to_field='UserEmail', on_delete=models.CASCADE, null=True)
    ResName = models.CharField(max_length=50)  # 姓名
    NormalizedName = models.CharField(max_length=50, null=True)  # 规范化的姓名
    ResEmail = models.CharField(max_length=50, null=True, unique=True)
    ResField = models.CharField(max_length=50, null=True)  # 作者领域
    ResIntroduction = models.CharField(max_length=2000, null=True)
    LiteratureNum = models.IntegerField(default=0)  # 发表文章数量
    CitedNum = models.IntegerField(null=True)  # 文章被引用次数
    VisitNum = models.IntegerField(default=0)  # 浏览次数
    ConcernNum = models.IntegerField(default=0)  # 关注人数
    InstitutionName = models.CharField(max_length=100)#作者机构名


class Paper(models.Model):
    PaperId = models.CharField(max_length=50, primary_key=True)
    PaperTitle = models.CharField(max_length=1000)
    PaperAuthors = models.CharField(max_length=500, null=True)
    PaperOrg = models.TextField(max_length=5000, null=True)
    ReadNum = models.IntegerField(default=0)  # 阅读次数
    PaperUrl = models.TextField(max_length=8000, null=True)
    CollectionNum = models.IntegerField(default=0)  # 收藏次数
    IsUserUpload = models.BooleanField(default=False)
    PaperTime = models.IntegerField(null=True)  # 发表时间
    PaperAbstract = models.TextField(max_length=8000, null=True)  # 摘要
    PaperKeywords = models.TextField(max_length=8000, null=True)  # 关键字
    PaperCitation = models.IntegerField(null=True)  # 引用数量
    PaperStart = models.IntegerField(null=True)  # 论文开始页
    PaperEnd = models.IntegerField(null=True)  # 论文结束页
    PaperLang = models.CharField(max_length=20, null=True)  # 语言
    PaperVolume = models.IntegerField(null=True)  # 册
    PaperIssue = models.CharField(max_length=50, null=True)  # 期号
    PaperPublisher = models.CharField(max_length=1000, null=True)  # 出版商
    PaperType = models.CharField(max_length=50, null=True)  # 论文类型
    PaperFos = models.CharField(max_length=2000, null=True)  # 学科
    PaperDoi = models.CharField(max_length=100, null=True)
    PaperVenue = models.CharField(max_length=500, null=True)  # 会议


class PaperAuthor(models.Model):
    PaperId = models.ForeignKey('Paper', to_field='PaperId', on_delete=models.CASCADE)
    ResearcherId = models.ForeignKey('Researcher', to_field='ResId', on_delete=models.CASCADE)
    ResearcherRank = models.IntegerField(null=True)


class PaperReference(models.Model):
    PaperId = models.ForeignKey('Paper', to_field='PaperId', related_name='TPaperId', on_delete=models.CASCADE)
    RePaperId = models.ForeignKey('Paper', to_field='PaperId', related_name='RePaperId', on_delete=models.CASCADE)


class Patent(models.Model):
    PatentId = models.CharField(max_length=50, primary_key=True)
    PatentTitle = models.CharField(max_length=1000)
    ReadNum = models.IntegerField(default=0)
    PatentUrl = models.TextField(max_length=8000, default=0)
    CollectionNum = models.IntegerField(default=0)
    IsUserUpload = models.BooleanField(default=False)
    PatentAbstract = models.TextField(max_length=8000, null=True)  # 摘要
    PatentDate = models.DateField(null=True)
    PatentAuthor = models.CharField(max_length=500, null=True)
    PatentCompany = models.CharField(max_length=100, null=True)


class PatentAuthor(models.Model):
    PatentId = models.ForeignKey('Patent', to_field='PatentId', on_delete=models.CASCADE)
    ResearcherId = models.ForeignKey('Researcher', to_field='ResId', on_delete=models.CASCADE)
    ResearcherRank = models.IntegerField(null=True)


class Project(models.Model):
    ProjectId = models.CharField(max_length=50, primary_key=True)  # grant no
    ProjectTitle = models.CharField(max_length=1000)
    ReadNum = models.IntegerField(default=0)  # 阅读次数
    ProjectUrl = models.CharField(max_length=200, db_index=True, unique=True)
    CollectionNum = models.IntegerField(default=0)  # 收藏次数
    GrantYear = models.IntegerField(null=True)  # 发表年份
    Subject = models.CharField(max_length=100, null=True)  # 主题
    ProjectLeader = models.CharField(max_length=50, null=True)  # 项目组长
    ProjectLeaderTitle = models.CharField(max_length=50, null=True)  # 项目组长头衔
    SupportUnits = models.CharField(max_length=50, null=True)  # 赞助方
    Funding = models.CharField(max_length=20, null=True)  # 项目基金
    ProjectCategory = models.CharField(max_length=50, null=True)  # 项目类别
    StudyPeriod = models.CharField(max_length=100, null=True)  # 研究期
    SubjectHeadingCN = models.CharField(max_length=1000, null=True)  # 项目中文题目
    SubjectHeadingEN = models.CharField(max_length=1000, null=True)  # 项目英文题目
    ZhAbstract = models.TextField(max_length=8000, null=True)  # 中文摘要
    EnAbstract = models.TextField(max_length=8000, null=True)  # 英文摘要
    FinalAbstract = models.TextField(max_length=8000, null=True)  # 结题摘要


class ProjectAuthor(models.Model):
    ProjectId = models.ForeignKey('Project', to_field='ProjectId', on_delete=models.CASCADE)
    ResearcherId = models.ForeignKey('Researcher', to_field='ResId', on_delete=models.CASCADE)
    ResearcherRank = models.IntegerField(null=True)


class Concern(models.Model):
    UserEmail = models.ForeignKey('HubUser', to_field='UserEmail', on_delete=models.CASCADE)
    ResearchId = models.ForeignKey('Researcher', to_field='ResId', on_delete=models.CASCADE)
    ConcernTime = models.DateTimeField(auto_now_add=True)


class Collection(models.Model):
    UserEmail = models.ForeignKey('HubUser', to_field='UserEmail', on_delete=models.CASCADE)
    PaperId = models.ForeignKey('Paper', to_field='PaperId', on_delete=models.CASCADE, null=True)
    PatentId = models.ForeignKey('Patent', to_field='PatentId', on_delete=models.CASCADE, null=True)
    ProjectId = models.ForeignKey('Project', to_field='ProjectId', on_delete=models.CASCADE, null=True)
    CollectionTime = models.DateTimeField(auto_now_add=True)
    CollectionType = models.IntegerField()


class Mail(models.Model):
    SendEmail = models.ForeignKey('HubUser', related_name='send', to_field='UserEmail', on_delete=models.CASCADE)
    ReceiveEmail = models.ForeignKey('HubUser', related_name='receive', to_field='UserEmail', on_delete=models.CASCADE)
    MailContent = models.CharField(max_length=2000, null=False)
    SendTime = models.DateTimeField(auto_now_add=True)
    IsRead = models.BooleanField(default=False)
    WithDraw = models.BooleanField(default=False)


class Message(models.Model):
    ReceiveEmail = models.ForeignKey('HubUser', to_field='UserEmail', on_delete=models.CASCADE)
    MessageContent = models.CharField(max_length=2000)
    MessageType = models.SmallIntegerField()
    SendTime = models.DateTimeField(auto_now_add=True)
    IsRead = models.BooleanField(default=True)


class ChatFriends(models.Model):
    MyId = models.ForeignKey(HubUser, related_name='myId', to_field='UserEmail', on_delete=models.CASCADE)
    FriendId = models.ForeignKey(HubUser, related_name='friendId', to_field='UserEmail', on_delete=models.CASCADE)
    MeetDate = models.DateField(default=None)
    LastMail = models.ForeignKey(Mail, related_name='lastMail', on_delete=models.CASCADE, null=True)
    Unread = models.IntegerField(default=0)


class Administrators(models.Model):
    AdmEmail = models.CharField(max_length=50, primary_key=True)
    AdmPassword = models.CharField(max_length=20)


class Browse(models.Model):
    UserEmail = models.ForeignKey('HubUser', to_field='UserEmail', on_delete=models.CASCADE)
    PaperId = models.ForeignKey('Paper', to_field='PaperId', on_delete=models.CASCADE, null=True)
    PatentId = models.ForeignKey('Patent', to_field='PatentId', on_delete=models.CASCADE, null=True)
    ProjectId = models.ForeignKey('Project', to_field='ProjectId', on_delete=models.CASCADE, null=True)
    ResearchId = models.ForeignKey('Researcher', to_field='ResId', on_delete=models.CASCADE, null=True)
    BrowseType = models.IntegerField()
    BrowseTime = models.DateTimeField(auto_now_add=True)


class Search(models.Model):
    UserEmail = models.ForeignKey('HubUser', to_field='UserEmail', on_delete=models.CASCADE)
    SearchContent = models.CharField(max_length=200)
    SearchTime = models.DateTimeField(auto_now_add=True)


class Appeal(models.Model):
    ResearchId = models.ForeignKey('Researcher', to_field='ResId', on_delete=models.CASCADE)
    UserEmail = models.ForeignKey('HubUser', to_field='UserEmail', on_delete=models.CASCADE)
    AppealState = models.IntegerField()#0 未审核 1拒绝 2通过
    AppealTime = models.DateTimeField(auto_now_add=True,null=True)
    content = models.CharField(max_length=500)

class Review(models.Model):
    ReviewPath = models.CharField(max_length=100)
    UserEmail = models.ForeignKey('HubUser', to_field='UserEmail', on_delete=models.CASCADE)
    UploadTime = models.DateTimeField(auto_now_add=True)
    ReviewState = models.IntegerField()#0 未审核 1拒绝 2通过
    ReviewTime = models.DateTimeField(auto_now_add=False,null=True)
    content = models.CharField(max_length=500)

class Relationship(models.Model):
    ResearchId1 = models.ForeignKey('Researcher', related_name='first', to_field='ResId', on_delete=models.CASCADE)
    ResearchId2 = models.ForeignKey('Researcher', related_name='second', to_field='ResId', on_delete=models.CASCADE)
    LiteratureNum = models.IntegerField()
