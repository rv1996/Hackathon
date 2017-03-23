from django.db import models
from django.contrib.auth.models import User
#from markdown_deux import markdown # for better question input from the user

# Create your models here.

# No models for MP is used we'll use the default USER models

class Department(models.Model):
    department_id = models.CharField(max_length=1000)
    department_name = models.CharField(max_length=1000)
    password = models.CharField(max_length=1000) # add this in an encrypted way

    def __str__(self):
        return "{} | {}".format(self.department_name,self.department_id)


class Question(models.Model):
    text = models.CharField(max_length=5000)
    subject = models.CharField(max_length=5000)
    type = models.CharField(max_length=50) # in the form section we'll use choice field.
    timestamp = models.DateTimeField(auto_now=True,null=True)
    deadline = models.DateTimeField() # default is gonna be 3 days



    def __str__(self):
        return  self.subject

class QuestionFor(models.Model):
    question = models.ForeignKey(Question)
    asked_by = models.ForeignKey(User)
    asked_to = models.ForeignKey(Department)
    answer = models.TextField()

    def __str__(self):
        return "{} | {} ".format(self.asked_by.username,self.asked_to.department_name)

class Recommendation(models.Model):

    class Meta:
        unique_together = (('to','by'))

    to = models.ForeignKey(Department,related_name='to') #related names are used for query back purpose
    by = models.ForeignKey(Department,related_name='by')
    recommended_answer = models.TextField()

    def __str__(self):
        return "{} | {}".format(self.to.department_name,self.by.department_name)

