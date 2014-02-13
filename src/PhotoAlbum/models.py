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

class MyRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    username = forms.CharField(min_length=5, max_length=50)
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()
    password2.help_text = None
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    def save(self, commit = True):
        user = super(MyRegistrationForm, self).save(commit=False)
        cleaned_data = super(MyRegistrationForm, self).clean()
        
        if commit:
            user.save()
            
        return user
    
class Payment(models.Model):
    pid = models.CharField(max_length = 40)
    date = models.DateTimeField()
    price = models.IntegerField()
    reference = models.IntegerField()
    item = models.ForeignKey(Album, related_name="payments")
    buyer = models.ForeignKey(User, related_name="payments")