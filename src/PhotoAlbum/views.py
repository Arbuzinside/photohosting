from django.shortcuts import render_to_response
from models import Album, Page, Picture

def show_picture(request):
    pictures = Picture.objects.get(Title = 'Bunny')
    return render_to_response("picture.html", {'pics' : pictures})

def index(request):
    return render_to_response("index.html", {})  

def home(request):
    return render_to_response("home.html", {})

def edit(request):
    return render_to_response("edit.html", {})