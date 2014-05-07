from django.db import models
from django.contrib.auth.models import User

class EvaluatingFormulas(models.Model):
	name = models.CharField(max_length=80)
	formula = models.CharField(max_length=200)


class WorkType(models.Model):
	name = models.CharField(max_length=80)
	mime = models.CharField(max_length=100)


class Evaluation(models.Model):
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=500)
    owner = models.ForeignKey(User)
    totals = models.ForeignKey(EvaluatingFormulas)
    created = models.DateField(auto_now_add=True)
    evaluationStartTime = models.DateTimeField()
    evaluationEndTime = models.DateTimeField()
    minEvaluators = models.IntegerField(default="1")
    maxEvaluators = models.IntegerField()
    deliberables = models.ManyToManyField(WorkType, related_name='deliberable',through='DeliberableAtributes')
    participants = models.ManyToManyField(User, related_name='participants')

    def __unicode__(self):
        return self.owner.name+'.'+self.name

    class Meta:
        ordering = ['owner','name']
        verbose_name_plural = 'Coevaluations'
        verbose_name = 'Coevaluation'


class GradingScale(models.Model):
	name = models.CharField(max_length=80)
	minimum = models.IntegerField()
	maximum = models.IntegerField()


class DeliberableAtributes(models.Model):
	name = models.CharField(max_length=80)
	conditions = models.TextField()
	workType = models.ForeignKey(WorkType)
	evaluation = models.ForeignKey(Evaluation)
	gradingScale = models.ForeignKey(GradingScale)


import os,time
def user_folder(instance, filename):
    return os.path.join('delivered',time.strftime('%Y%m%d%H%M%S'),instance.user.user.username, filename)

class DeliberedWork(models.Model):
	name = models.CharField(max_length=80)
	text = models.TextField()
	uploadedFile = models.FileField(upload_to=user_folder)
	url = models.URLField()


class UserDeliberableEvaluation(models.Model):
	student = models.ForeignKey(User)
	evaluation = models.ForeignKey(Evaluation)
	work = models.ForeignKey(DeliberedWork)
    

class ConcreteEvaluation(models.Model):
	evaluator = models.ForeignKey(User)
	work = models.ForeignKey(DeliberedWork)
	feedback = models.TextField()
	mark = models.IntegerField()