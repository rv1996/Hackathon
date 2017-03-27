from django.db import models
from django.contrib.auth.models import AbstractUser,User
#from markdown_deux import markdown # for better question input from the user

# Create your models here.

# No models for MP is used we'll use the default USER models


class Department(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    department_name = models.CharField(max_length=1000)
    def __str__(self):
        return "{}".format(self.department_name)


class Question(models.Model):
    text = models.CharField(max_length=5000)
    subject = models.CharField(max_length=5000)
    type = models.CharField(max_length=50) # in the form section we'll use choice field.
    timestamp = models.DateTimeField(auto_now=True,null=True)
    deadline = models.DateField() # default is gonna be 3 days
    asked_by = models.ForeignKey(User)



    def deadline_check(self):
        pass

    def __str__(self):
        return  self.subject


class QuestionFor(models.Model):
    question = models.ForeignKey(Question)
    asked_to = models.ForeignKey(Department)
    answer = models.TextField(null=True)

    def __str__(self):
        return "{} | {} ".format(self.question.asked_by.username,self.asked_to.department_name)

class Recommendation(models.Model):

    class Meta:
        unique_together = (('to','by'))

    question = models.ForeignKey(Question)
    to = models.ForeignKey(Department,related_name='recommended_to_me') #related names are used for query back purpose
    by = models.ForeignKey(Department,related_name='recommended_by_me')

    recommended_answer = models.TextField()

    def __str__(self):
        return "{} | {}".format(self.to.department_name,self.by.department_name)

