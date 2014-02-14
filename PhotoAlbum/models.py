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
    #if th user is not registered, the buyer field will be empty
    buyer = models.ForeignKey(User, related_name="payments", blank = True, null = True)
    
    
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
        cleaned_data = super(MyRegistrationForm, self).clean()
        
        if commit:
            user.save()
            
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')
        
    def __init__(self, *args, **kwargs):
        forms.CharField(label='Username').initial = self.instance.username
        email = forms.EmailField(label='Email')
        name = forms.CharField(label='First name')
        surname = forms.CharField(label='Last name')
        super(UserProfileForm, self).__init__(*args, **kwargs)
        name = self.instance.username
        self.fields['email'].initial = self.instance.email
        
    def save(self, *args, **kw):
        super(UserProfileForm, self).save(commit=False)
        self.instance.user.username = self.cleaned_data.get('username')
        self.instance.user.email = self.cleaned_data.get('email')
        self.instance.user.save()
