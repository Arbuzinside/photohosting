from django.shortcuts import render_to_response
from django.http import  HttpResponseRedirect
from django.template import RequestContext
from django.utils.timezone import utc
from datetime import datetime
from models import Album, Page, Picture, AlbumForm

def show_picture(request):
    pictures = Picture.objects.get(title = 'Bunny')
    return render_to_response("picture.html", {'pics' : pictures})

def index(request):
    return render_to_response("index.html", {})  

def home(request):
    if request.method == 'POST':
        #validate???
        album = Album()
        album.title = request.POST.get('title','')
        #TODO:set time-zone in profile
        album.date = datetime.utcnow().replace(tzinfo=utc)
        album.link = 'http://image-uniservice.copainsdavant.com/image/450/2/2080911558/10696081.png'
        album.save()
        return HttpResponseRedirect('/home/')
    
    albums = Album.objects.all()
    return render_to_response("home.html", {'album' : albums}, context_instance=RequestContext(request))

def edit(request): 
    return render_to_response("edit.html", {}, context_instance=RequestContext(request))