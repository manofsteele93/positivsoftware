from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Response(models.Model):
    user = models.ForeignKey(User, related_name="User", on_delete=models.CASCADE, default=1)
    response_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    public = models.BooleanField(default=True)
    edited = models.BooleanField(default=False)

    #This will allow us to see the specific response_text
    def __str__(self):
        return self.response_text

    #This will display all questions published within the last 1 day.
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    #This will display all questions published within the last 7 days.
    def was_published_week(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=7)

    #This will display all questions published within the last 30 days.
    def was_published_month(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=30)

    #This will display all questions published within the last 90 days.
    def was_published_quarter(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=90)

    #This will display all questions published within the last 180 days.
    def was_published_half(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=180)

    #This will display all questions published within the last year.
    def was_published_year(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=365)

# class Choice(models.Model):
#     response = models.ForeignKey(Response, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)
