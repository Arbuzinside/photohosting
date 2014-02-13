from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

#Represents the albums
class Album(models.Model):
    title = models.CharField(max_length = 255)
    date = models.DateTimeField()
    link = models.URLField()
    cover = models.URLField()
    public = models.BooleanField()
    owner = models.ForeignKey(User, related_name="albums")

#Pages of the albums
#layout contains the selected layout (value 1..4)
class Page(models.Model):
    layout = models.IntegerField()
    containingAlbum = models.ForeignKey(Album, related_name="pages")
    
#Pictures on the page
#title contains the caption
#source contains the url of the image
class Picture(models.Model):
    title = models.CharField(max_length = 255)
    source = models.URLField()
    containingPage = models.ForeignKey(Page, related_name="pictures")

#Registration
#TODO: check that the passwords are equal
class MyRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    username = forms.CharField(min_length=5, max_length=50)
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    def save(self, commit = True):
        user = super(MyRegistrationForm, self).save(commit=False)
        #cleaned_data = super(MyRegistrationForm, self).clean()
        if commit:
            user.save()
            
        return user

#Payments
#Contains the buyer and the album

#TODO: ref number?
class Payment(models.Model):
    pid = models.CharField(max_length = 40)
    date = models.DateTimeField()
    item = models.ForeignKey(Album, related_name="payments")
    buyer = models.ForeignKey(User, related_name="payments")