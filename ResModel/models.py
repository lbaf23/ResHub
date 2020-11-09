from django.db import models
#manage.py migrate    manage.py makemigrations
# Create your models here.

class HubUser(models.Model):
    UserEmail = models.CharField(max_length=50, primary_key=False,unique=True)
    UserName = models.CharField(max_length=50, null=True)
    UserPassword = models.CharField(max_length=20,null=False)
    UserImage = models.CharField(max_length=50,null=False)
    UserIntroduction = models.CharField(max_length=2000,null=True)

class Institution(models.Model):
    InsName = models.CharField(max_length=50,null=False)
    InsField = models.CharField(max_length=50,null=True)
    InsIntroduction = models.CharField(max_length=50,null=False)

class Researcher(models.Model):
    IsClaim = models.BooleanField(null=False)
    UserEmail = models.OneToOneField('HubUser',to_field='UserEmail',on_delete=models.CASCADE,null=True)
    ResName = models.CharField(max_length=50,null=False)
    ResEmail = models.CharField(max_length=50,null=False)
    ResField = models.CharField(max_length=50,null=True)
    ResCompany = models.ForeignKey('Institution',to_field='id',on_delete=models.CASCADE)
    ResIntroduction = models.CharField(max_length=50,null=True)
    LiteratureNum = models.IntegerField(null=False)
    CitedNum = models.IntegerField(null=False)
    VisitNum = models.IntegerField(null=False)
    ConcernNum = models.IntegerField(null=False)

class Literature(models.Model):
    '''
    LitName = models.CharField(max_length=200,null=False)
    LitDate = models.DateField(auto_now_add=False)
    LitType = models.SmallIntegerField(null=False)
    LitAuthor = models.CharField(max_length=200,null=False)
    LitQuote = models.CharField(max_length=200,null=True)
    '''
    LitRead = models.IntegerField(null=False)
    LitLink = models.CharField(max_length=200,null=True)
    CollectionNum = models.IntegerField(null=False)
    IsUserUpload = models.BooleanField(null=False)

class Paper(Literature):
    PaperId = models.CharField(max_length=50, primary_key=True)
    PaperTitle = models.CharField(max_length=200,null=False)
    PaperAuthor = models.CharField(max_length=200,null=False)
    PaperVenue =  models.CharField(max_length=200,null=False)
    PaperTime = models.DateField(auto_now_add=False,null=True)
    PaperCitation = models.IntegerField(null=False)
    PaperStart = models.CharField(max_length=20,null=True)
    PaperEnd = models.CharField(max_length=20,null=True)
    PaperLang = models.CharField(max_length=20,null=True)#语言
    PaperVolume = models.CharField(max_length=50) #册
    PaperIssue = models.CharField(max_length=50)
    PaperPublisher = models.CharField(max_length=50)
    PaperType = models.CharField(max_length=50)

class Concern(models.Model):
    UserEmail = models.ForeignKey('HubUser',to_field='UserEmail',on_delete=models.CASCADE)
    ResearchId = models.ForeignKey('Researcher',to_field='id',on_delete=models.CASCADE)
    ConcernTime = models.DateTimeField(auto_now_add=True)

class Collection(models.Model):
    UserEmail = models.ForeignKey('HubUser',to_field='UserEmail',on_delete=models.CASCADE)
    LiteratureId = models.ForeignKey('Literature',to_field='id',on_delete=models.CASCADE)
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
    MessageContent = models.CharField(max_length=2000,null=False)
    MessageType = models.SmallIntegerField(null=False)
    SendTime = models.DateTimeField(auto_now_add=True)
    IsRead = models.BooleanField(default=True)

class ChatFriends(models.Model):
    myId = models.ForeignKey(HubUser,related_name='myId',on_delete=models.CASCADE)
    friendId = models.ForeignKey(HubUser,related_name='friendId',on_delete=models.CASCADE)
    meetDate = models.DateField(default=None)
    lastMail = models.ForeignKey(Mail,related_name='lastMail',on_delete=models.CASCADE,default=None)
    unread = models.IntegerField(default=0)

class Administrators(models.Model):
    AdmEmail = models.CharField(max_length=50,null=False)
    AdmPassword = models.CharField(max_length=20,null=False)

class Browse(models.Model):
    UserEmail = models.ForeignKey('HubUser',to_field='UserEmail',on_delete=models.CASCADE)
    LiteratureId = models.ForeignKey('Literature',to_field='id',on_delete=models.CASCADE,null=True)
    ResearchId = models.ForeignKey('Researcher',to_field='id',on_delete=models.CASCADE,null=True)
    BrowseType = models.SmallIntegerField(null=False)
    BrowseTime = models.DateTimeField(auto_now_add=True)

class Search(models.Model):
    UserEmail = models.ForeignKey('HubUser', to_field='UserEmail', on_delete=models.CASCADE)
    SearchContent = models.CharField(max_length=200,null=False)
    SearchTime = models.DateTimeField(auto_now_add=True)

class Appeal(models.Model):
    ResearchId = models.ForeignKey('Researcher',to_field='id',on_delete=models.CASCADE)
    UserEmail = models.ForeignKey('HubUser',to_field='UserEmail',on_delete=models.CASCADE)
    AppealState = models.BooleanField(null=False)
    AppealTime = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    UserEmail = models.ForeignKey('HubUser',to_field='UserEmail',on_delete=models.CASCADE)
    UploadTime = models.DateTimeField(auto_now_add=True)
    ReviewState = models.BooleanField(null=False)
    ReviewTime = models.DateTimeField(auto_now_add=False)

class Relationship(models.Model):
    ResearchId1 = models.ForeignKey('Researcher',related_name='first',to_field='id',on_delete=models.CASCADE)
    ResearchId2 = models.ForeignKey('Researcher',related_name='second',to_field='id',on_delete=models.CASCADE)
    LiteratureNum = models.IntegerField(null=False)



