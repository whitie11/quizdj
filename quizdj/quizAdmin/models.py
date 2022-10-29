from operator import mod
from django.db import models

# Create your models here.


class Question(models.Model):
    ID = models.AutoField(primary_key=True)
    group = models.CharField(max_length=20)
    question_num = models.IntegerField()
    text = models.CharField(max_length=250)
    answerA = models.CharField(max_length=150)
    answerB = models.CharField(max_length=150)
    answerC = models.CharField(max_length=150)
    answerD = models.CharField(max_length=150)
    duration = models.IntegerField()
    correctAns = models.CharField(max_length=1)

class QuestionGroupList(models.Model):
    group = models.CharField(max_length=20)
    count = models.IntegerField()
    
