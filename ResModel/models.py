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
    ResId = models.CharField(max_length=50)
    IsClaim = models.BooleanField()
    UserEmail = models.OneToOneField('HubUser',to_field='UserEmail',on_delete=models.CASCADE,null=True)
    ResName = models.CharField(max_length=50)
    NormalizedName = models.CharField(max_length=50,null=True)
    ResEmail = models.CharField(max_length=50,null=True,unique=True)
    ResField = models.CharField(max_length=50,null=True)
    ResCompany = models.ForeignKey('Institution',to_field='id',on_delete=models.CASCADE,null=True)
    ResIntroduction = models.CharField(max_length=50,null=True)
    LiteratureNum = models.IntegerField(default=0)
    CitedNum = models.IntegerField(null=True)
    VisitNum = models.IntegerField(default=0)
    ConcernNum = models.IntegerField(default=0)
    ResHIndex = models.IntegerField(null=True)

class Literature(models.Model):
    LitId = models.CharField(max_length=50,primary_key=True)
    LitTitle = models.CharField(max_length=200)
    ReadNum = models.IntegerField(default=0)
    LinkNum = models.CharField(max_length=200,default=0)
    CollectionNum = models.IntegerField(default=0)
    IsUserUpload = models.BooleanField(default=False)
    PaperAuthor = models.ManyToManyField(to="Researcher",null=True)
    class Meta:
        abstract = True

class Paper(Literature):
    PaperVenue =  models.CharField(max_length=200,null=False)
    PaperTime = models.DateField(auto_now_add=False,null=True)
    PaperCitation = models.IntegerField(null=False)
    PaperStart = models.CharField(max_length=20,null=True)
    PaperEnd = models.CharField(max_length=20,null=True)
    PaperLang = models.CharField(max_length=20,null=True)#语言
    PaperVolume = models.CharField(max_length=50,null=True) #册
    PaperIssue = models.CharField(max_length=50,null=True)
    PaperPublisher = models.CharField(max_length=50,null=True)
    PaperType = models.CharField(max_length=50,null=True)
    LitType = models.IntegerField(default=1)

class Patent(Literature):
    PatentAbstract = models.CharField(max_length=2000,null=True)
    LitType = models.IntegerField(default=2)

class Project(Literature):
    GrantYear = models.DateField(auto_now_add=False,null=True)
    Subject = models.CharField(max_length=100,null=True)
    ProjectLeader = models.CharField(max_length=50,null=True)
    ProjectLeaderTitle = models.CharField(max_length=50,null=True)
    SupportUnits = models.CharField(max_length=50,null=True)
    Funding = models.CharField(max_length=20,null=True)
    ProjectCategory = models.CharField(max_length=50,null=True)
    StudyPeriod = models.CharField(max_length=100,null=True)
    SubjectHeadingCN = models.CharField(max_length=100,null=True)
    SubjectHeadingEN = models.CharField(max_length=200,null=True)
    LitType = models.IntegerField(default=3)

class Concern(models.Model):
    UserEmail = models.ForeignKey('HubUser',to_field='UserEmail',on_delete=models.CASCADE)
    ResearchId = models.ForeignKey('Researcher',to_field='id',on_delete=models.CASCADE)
    ConcernTime = models.DateTimeField(auto_now_add=True)

class Collection(models.Model):
    UserEmail = models.ForeignKey('HubUser',to_field='UserEmail',on_delete=models.CASCADE)
    PaperId = models.ForeignKey('Paper',to_field='LitId',on_delete=models.CASCADE,null=True)
    PatentId = models.ForeignKey('Patent',to_field='LitId',on_delete=models.CASCADE,null=True)
    ProjectId = models.ForeignKey('Project',to_field='LitId',on_delete=models.CASCADE,null=True)
    CollectionTime = models.DateTimeField(auto_now_add=True)

class Mail(models.Model):
    SendEmail = models.ForeignKey('HubUser',related_name='send',to_field='UserEmail',on_delete=models.CASCADE)
    ReceiveEmail = models.ForeignKey('HubUser',related_name='receive',to_field='UserEmail',on_delete=models.CASCADE)
    MailContent = models.CharField(max_length=2000,null=False)
    SendTime = models.DateTimeField(auto_now_add=True)
    IsRead = models.BooleanField(null=False)
    withDraw = models.BooleanField(default=False)

class Message(models.Model):
    ReceiveEmail = models.ForeignKey('HubUser',to_field='UserEmail',on_delete=models.CASCADE)
    MessageContent = models.CharField(max_length=2000)
    MessageType = models.SmallIntegerField()
    SendTime = models.DateTimeField(auto_now_add=True)
    IsRead = models.BooleanField(default=True)

class ChatFriends(models.Model):
    myId = models.ForeignKey(HubUser,related_name='myId',to_field='UserEmail',on_delete=models.CASCADE)
    friendId = models.ForeignKey(HubUser,related_name='friendId',to_field='UserEmail',on_delete=models.CASCADE)
    meetDate = models.DateField(default=None)
    lastMail = models.ForeignKey(Mail,related_name='lastMail',on_delete=models.CASCADE,default=None)
    unread = models.IntegerField(default=0)

class Administrators(models.Model):
    AdmEmail = models.CharField(max_length=50)
    AdmPassword = models.CharField(max_length=20)

class Browse(models.Model):
    UserEmail = models.ForeignKey('HubUser',to_field='UserEmail',on_delete=models.CASCADE)
    PaperId = models.ForeignKey('Paper',to_field='LitId',on_delete=models.CASCADE,null=True)
    PatentId = models.ForeignKey('Patent',to_field='LitId',on_delete=models.CASCADE,null=True)
    ProjectId = models.ForeignKey('Project',to_field='LitId',on_delete=models.CASCADE,null=True)
    ResearchId = models.ForeignKey('Researcher',to_field='id',on_delete=models.CASCADE,null=True)
    BrowseType = models.SmallIntegerField()
    BrowseTime = models.DateTimeField(auto_now_add=True)

class Search(models.Model):
    UserEmail = models.ForeignKey('HubUser', to_field='UserEmail', on_delete=models.CASCADE)
    SearchContent = models.CharField(max_length=200)
    SearchTime = models.DateTimeField(auto_now_add=True)

class Appeal(models.Model):
    ResearchId = models.ForeignKey('Researcher',to_field='id',on_delete=models.CASCADE)
    UserEmail = models.ForeignKey('HubUser',to_field='UserEmail',on_delete=models.CASCADE)
    AppealState = models.BooleanField()
    AppealTime = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    UserEmail = models.ForeignKey('HubUser',to_field='UserEmail',on_delete=models.CASCADE)
    UploadTime = models.DateTimeField(auto_now_add=True)
    ReviewState = models.BooleanField()
    ReviewTime = models.DateTimeField(auto_now_add=False)

class Relationship(models.Model):
    ResearchId1 = models.ForeignKey('Researcher',related_name='first',to_field='id',on_delete=models.CASCADE)
    ResearchId2 = models.ForeignKey('Researcher',related_name='second',to_field='id',on_delete=models.CASCADE)
    LiteratureNum = models.IntegerField()



