from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.db.models.deletion import DO_NOTHING
from django.db.models.fields import CharField
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey
# Create your models here.

class Expense(models.Model):
    userid = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    exp_date = models.DateField(default=date.today)
    exp_name = models.CharField(max_length=150)
    exp_desc = models.CharField(max_length=300)
    exp_amount = models.IntegerField()
    exp_month = models.CharField(max_length=12)
    exp_year = models.CharField(max_length=4)

class Income(models.Model):
    userid = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    inc_date = models.DateField(default=date.today)
    inc_name = models.CharField(max_length=150)
    inc_desc = models.CharField(max_length=300)
    inc_amount = models.IntegerField()
    inc_month = models.CharField(max_length=12)
    inc_year = models.CharField(max_length=4)

class UserImage(models.Model):
    userid = ForeignKey(User, on_delete=DO_NOTHING)
    imgcaption = CharField(max_length=230, default="Profile Picture")
    userimage = ImageField(upload_to ="profile_pics/")

    def __str__(self) -> str:
        return self.imgcaption