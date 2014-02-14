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
    item = models.ForeignKey(Album, related_name="payments")
    buyer = models.ForeignKey(User, related_name="payments")
    
    
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
        super(MyRegistrationForm, self).clean()
        
        if commit:
            user.save()
            
        return user

class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        forms.CharField(label='Username').initial = self.instance.username
        forms.EmailField(label='Email').initial = self.instance.email
        print(self.instance.username)
        
    def save(self, *args, **kw):
        super(UserProfileForm, self).save(commit=False)
        self.instance.user.username = self.cleaned_data.get('username')
        self.instance.user.email = self.cleaned_data.get('email')
        self.instance.user.save()


    class Meta:
        model = User
        fields = ('username', 'email')       