from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class User:
    def newUser(self, username, name, surname, password, email):
        User.objects.create_user(username, name, surname, password, email)
        return True 