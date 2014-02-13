from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class Album(models.Model):
    title = models.CharField(max_length = 255)
    date = models.DateTimeField()
    link = models.URLField()
    cover = models.URLField()
    owner = models.ForeignKey(User, related_name="albums")
    public = models.BooleanField()

class Page(models.Model):
    layout = models.IntegerField()
    containingAlbum = models.ForeignKey(Album, related_name="pages")
    
class Picture(models.Model):
    title = models.CharField(max_length = 255)
    source = models.URLField()
    containingPage = models.ForeignKey(Page, related_name="pictures")

    
class Payment(models.Model):
    pid = models.CharField(max_length = 40)
    date = models.DateTimeField()
    price = models.IntegerField()
    reference = models.IntegerField()
    item = models.ForeignKey(Album, related_name="payments")
    buyer = models.ForeignKey(User, related_name="payments")
