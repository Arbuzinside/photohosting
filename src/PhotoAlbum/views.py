from django.shortcuts import render_to_response, get_object_or_404
from django.http import  HttpResponseRedirect
from django.template import RequestContext
from django.utils.timezone import utc
from datetime import datetime
from django.utils import simplejson
from hashlib import sha1
from models import Album, Page, Picture, MyRegistrationForm

def index(request):
    form = MyRegistrationForm()
    return render_to_response("index.html", {'form': form}, context_instance=RequestContext(request))  

def home(request):    
    albums = Album.objects.all()
    
    return render_to_response("home.html", {'album' : albums}, context_instance=RequestContext(request))

def edit(request, albumid = None): 
    if albumid:
        album = Album.objects.get(id = albumid)
        
        lays = {}
        imgs = {}
        
        for l in album.Pages.all():
            lays[l.id] = l.layout
            for i in l.Pictures.all():
                imgs[i.id] = {"title" : i.title, "source" : i.source}
            
        layouts = simplejson.dumps(lays, indent = 4)
        images = simplejson.dumps(imgs, indent = 4)
        
        return render_to_response("edit.html", {'album' : album, 'layouts' : layouts, 'images' : images}, context_instance=RequestContext(request))
    else:
        return render_to_response("edit.html", {}, context_instance=RequestContext(request))

def delete(request, albumid = None):
    if albumid:
        album = get_object_or_404(Album, id=albumid)
        album.delete()
    return HttpResponseRedirect('/home/') 

def save(request):
    if request.method == 'POST':
        #validate???
        layouts = simplejson.loads(request.POST.get('layouts'))
        images = simplejson.loads(request.POST.get('images'))
        
        albumid = request.POST.get('albumid', '')
        
        if albumid != '':
            album = Album.objects.get(id = albumid)
            album.title = request.POST.get('title','')
            
            for l in album.Pages.all():
                l.Pictures.all().delete()
            
            album.Pages.all().delete()            
        else:
            album = Album()
            album.title = request.POST.get('title','')
            #TODO:set time-zone in profile
            album.date = datetime.utcnow().replace(tzinfo=utc)
            album.link = sha1(album.title + album.date.isoformat()).hexdigest()

        i = 0
        j = 0
        found = False
        while i < len(images) and not found:
            while j < len(images[i]) and not found:
                if images[i][j]["src"] != '':
                    found = True
                j += 1
            i += 1
        
        album.cover = images[i - 1][j - 1]["src"]
            
        album.save()
        
        for i in range(0, len(layouts)):
            page = Page(layout=layouts[i], containingAlbum=album)
            page.save()
            for j in range(0, len(images[i])):
                image = Picture(title=images[i][j]["caption"], source=images[i][j]["src"], containingPage=page)
                image.save()
        
        return HttpResponseRedirect('/home/')

def view(request, albumlink):
    album = Album.objects.get(link = albumlink)
        
    lays = {}
    imgs = {}
    
    for l in album.Pages.all():
        lays[l.id] = l.layout
        for i in l.Pictures.all():
            imgs[i.id] = {"title" : i.title, "source" : i.source}
        
    layouts = simplejson.dumps(lays, indent = 4)
    images = simplejson.dumps(imgs, indent = 4)
    
    return render_to_response("view.html", {'album' : album, 'layouts' : layouts, 'images' : images}, context_instance=RequestContext(request))