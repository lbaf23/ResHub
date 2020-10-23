from django.db import models

# Create your models here.

class Client(models.Model):
    CliEmail = models.CharField(max_length=50, primary_key=True)
    CliName = models.CharField(max_length=50, null=True)

class Search(models.Model):
    CliEmail = models.ForeignKey('Client', to_field='CliEmail', on_delete=models.CASCADE)
    SearchContent = models.CharField(max_length=200)
    SearchTime = models.DateTimeField(auto_now_add=True)

