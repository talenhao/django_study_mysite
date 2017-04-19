from django.db import models
from django.utils import timezone
from django.http import HttpResponse
import datetime

# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        # 现在的时间 - 时间差1天 = 昨天
        # 如果大于昨天的现在时间，返回True，否则False
        # return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
        now = timezone.now()
        # 只有处理昨天当前时刻与当前时刻之间才return True
        return now - datetime.timedelta(days=1) < self.pub_date < now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
