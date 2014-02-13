from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm



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


    class Meta:
        model = User
        fields = ('username', 'email')
            
