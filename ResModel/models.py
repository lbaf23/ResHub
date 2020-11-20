from django.db import models
#manage.py migrate    manage.py makemigrations
# Create your models here.

class HubUser(models.Model):
    UserEmail = models.CharField(max_length=50, primary_key=True)
    UserName = models.CharField(max_length=50, null=True)
    UserPassword = models.CharField(max_length=20)
    UserImage = models.CharField(max_length=50)
    UserIntroduction = models.CharField(max_length=2000,null=True)

class Institution(models.Model):
    InsName = models.CharField(max_length=50)
    InsField = models.CharField(max_length=50,null=True)
    InsIntroduction = models.CharField(max_length=50)

class Researcher(models.Model):
    ResId = models.CharField(max_length=50,primary_key=True)
    IsClaim = models.BooleanField()
    UserEmail = models.OneToOneField('HubUser',to_field='UserEmail',on_delete=models.CASCADE,null=True)
    ResName = models.CharField(max_length=50)
    NormalizedName = models.CharField(max_length=50,null=True)
    ResEmail = models.CharField(max_length=50,null=True,unique=True)
    ResField = models.CharField(max_length=50,null=True)
    ResCompany = models.ForeignKey('Institution',to_field='id',on_delete=models.CASCADE,null=True)
    ResIntroduction = models.CharField(max_length=50,null=True)
    LiteratureNum = models.IntegerField(default=0)#发表文章数量
    CitedNum = models.IntegerField(null=True)#文章被引用次数
    VisitNum = models.IntegerField(default=0)#浏览次数
    ConcernNum = models.IntegerField(default=0)#关注人数
    ResHIndex = models.IntegerField(null=True)
    ResPubs = models.CharField(max_length=2000,null=True)#作者发表的文章

class Paper(models.Model):
    LitId = models.CharField(max_length=50,primary_key=True)
    LitTitle = models.CharField(max_length=200)
    ReadNum = models.IntegerField(default=0)
    LitUrl = models.CharField(max_length=200,default=0)
    CollectionNum = models.IntegerField(default=0)
    IsUserUpload = models.BooleanField(default=False)
    PaperTime = models.DateField(auto_now_add=False,null=True)#发表时间
    PaperAbstract = models.CharField(max_length=2000,null=True)#摘要
    PaperKeywords = models.CharField(max_length=200,null=True)#关键字
    PaperCitation = models.IntegerField(null=True)#引用数量
    PaperStart = models.CharField(max_length=20,null=True)#论文开始页
    PaperEnd = models.CharField(max_length=20,null=True)#论文结束页
    PaperVolume = models.CharField(max_length=50,null=True) #册
    PaperIssue = models.CharField(max_length=50,null=True)#期号
    PaperPublisher = models.CharField(max_length=50,null=True)#出版商
    PaperType = models.CharField(max_length=50,null=True)#论文类型
    LitType = models.IntegerField(default=1)#学术成果种类，默认为1，表示论文

class Paper_Author(models.Model):
    PaperId = models.ForeignKey('Paper',to_field='LitId',on_delete=models.CASCADE)
    ResearcherId = models.ForeignKey('Researcher',to_field='ResId',on_delete=models.CASCADE)

class Patent(models.Model):
    LitId = models.CharField(max_length=50,unique=True)
    LitTitle = models.CharField(max_length=200)
    ReadNum = models.IntegerField(default=0)
    LitUrl = models.CharField(max_length=200,default=0)
    CollectionNum = models.IntegerField(default=0)
    IsUserUpload = models.BooleanField(default=False)
    PatentAbstract = models.CharField(max_length=2000,null=True)#摘要
    LitType = models.IntegerField(default=2)#学术成果种类，默认为2，表示专利

class Patent_Author(models.Model):
    PatentId = models.ForeignKey('Patent',to_field='LitId',on_delete=models.CASCADE)
    ResearcherId = models.ForeignKey('Researcher',to_field='ResId',on_delete=models.CASCADE)

class Project(models.Model):
    LitId = models.CharField(max_length=50,unique=True)
    LitTitle = models.CharField(max_length=200)
    ReadNum = models.IntegerField(default=0)
    LitUrl = models.CharField(max_length=200,default=0)
    CollectionNum = models.IntegerField(default=0)
    IsUserUpload = models.BooleanField(default=False)
    GrantYear = models.DateField(auto_now_add=False,null=True)#发表年份
    Subject = models.CharField(max_length=100,null=True)#主题
    ProjectLeader = models.CharField(max_length=50,null=True)#项目组长
    ProjectLeaderTitle = models.CharField(max_length=50,null=True)#项目组长头衔
    SupportUnits = models.CharField(max_length=50,null=True)#赞助方
    Funding = models.CharField(max_length=20,null=True)#项目基金
    ProjectCategory = models.CharField(max_length=50,null=True)#项目类别
    StudyPeriod = models.CharField(max_length=100,null=True)#研究期
    SubjectHeadingCN = models.CharField(max_length=100,null=True)#项目中文题目
    SubjectHeadingEN = models.CharField(max_length=200,null=True)#项目英文题目
    LitType = models.IntegerField(default=3)#学术成果种类，默认为3，表示项目

class Project_Author(models.Model):
    ProjectId = models.ForeignKey('Project',to_field='LitId',on_delete=models.CASCADE)
    ResearcherId = models.ForeignKey('Researcher',to_field='ResId',on_delete=models.CASCADE)

class Concern(models.Model):
    UserEmail = models.ForeignKey('HubUser',to_field='UserEmail',on_delete=models.CASCADE)
    ResearchId = models.ForeignKey('Researcher',to_field='ResId',on_delete=models.CASCADE)
    ConcernTime = models.DateTimeField(auto_now_add=True)

class Collection(models.Model):
    UserEmail = models.ForeignKey('HubUser',to_field='UserEmail',on_delete=models.CASCADE)
    PaperId = models.ForeignKey('Paper',to_field='LitId',on_delete=models.CASCADE,null=True)
    PatentId = models.ForeignKey('Patent',to_field='LitId',on_delete=models.CASCADE,null=True)
    ProjectId = models.ForeignKey('Project',to_field='LitId',on_delete=models.CASCADE,null=True)
    CollectionTime = models.DateTimeField(auto_now_add=True)
    CollectionType = models.IntegerField()

class Mail(models.Model):
    SendEmail = models.ForeignKey('HubUser',related_name='send',to_field='UserEmail',on_delete=models.CASCADE)
    ReceiveEmail = models.ForeignKey('HubUser',related_name='receive',to_field='UserEmail',on_delete=models.CASCADE)
    MailContent = models.CharField(max_length=2000,null=False)
    SendTime = models.DateTimeField(auto_now_add=True)
    IsRead = models.BooleanField(default=False)
    WithDraw = models.BooleanField(default=False)

class Message(models.Model):
    ReceiveEmail = models.ForeignKey('HubUser',to_field='UserEmail',on_delete=models.CASCADE)
    MessageContent = models.CharField(max_length=2000)
    MessageType = models.SmallIntegerField()
    SendTime = models.DateTimeField(auto_now_add=True)
    IsRead = models.BooleanField(default=True)

class ChatFriends(models.Model):
    MyId = models.ForeignKey(HubUser,related_name='myId',to_field='UserEmail',on_delete=models.CASCADE)
    FriendId = models.ForeignKey(HubUser,related_name='friendId',to_field='UserEmail',on_delete=models.CASCADE)
    MeetDate = models.DateField(default=None)
    LastMail = models.ForeignKey(Mail,related_name='lastMail',on_delete=models.CASCADE,null=True)
    Unread = models.IntegerField(default=0)

class Administrators(models.Model):
    AdmEmail = models.CharField(max_length=50,primary_key=True)
    AdmPassword = models.CharField(max_length=20)

class Browse(models.Model):
    UserEmail = models.ForeignKey('HubUser',to_field='UserEmail',on_delete=models.CASCADE)
    PaperId = models.ForeignKey('Paper',to_field='LitId',on_delete=models.CASCADE,null=True)
    PatentId = models.ForeignKey('Patent',to_field='LitId',on_delete=models.CASCADE,null=True)
    ProjectId = models.ForeignKey('Project',to_field='LitId',on_delete=models.CASCADE,null=True)
    ResearchId = models.ForeignKey('Researcher',to_field='ResId',on_delete=models.CASCADE,null=True)
    BrowseType = models.IntegerField()
    BrowseTime = models.DateTimeField(auto_now_add=True)

class Search(models.Model):
    UserEmail = models.ForeignKey('HubUser', to_field='UserEmail', on_delete=models.CASCADE)
    SearchContent = models.CharField(max_length=200)
    SearchTime = models.DateTimeField(auto_now_add=True)

class Appeal(models.Model):
    ResearchId = models.ForeignKey('Researcher',to_field='ResId',on_delete=models.CASCADE)
    UserEmail = models.ForeignKey('HubUser',to_field='UserEmail',on_delete=models.CASCADE)
    AppealState = models.BooleanField()
    AppealTime = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    ReviewPath = models.CharField(max_length=100)
    UserEmail = models.ForeignKey('HubUser',to_field='UserEmail',on_delete=models.CASCADE)
    UploadTime = models.DateTimeField(auto_now_add=True)
    ReviewState = models.BooleanField()
    ReviewTime = models.DateTimeField(auto_now_add=False)

class Relationship(models.Model):
    ResearchId1 = models.ForeignKey('Researcher',related_name='first',to_field='ResId',on_delete=models.CASCADE)
    ResearchId2 = models.ForeignKey('Researcher',related_name='second',to_field='ResId',on_delete=models.CASCADE)
    LiteratureNum = models.IntegerField()



