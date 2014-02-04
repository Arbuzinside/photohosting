from django.shortcuts import render_to_response, get_object_or_404
from django.http import  HttpResponseRedirect
from django.template import RequestContext
from django.utils.timezone import utc
from datetime import datetime
from django.utils import simplejson
from models import Album, Page, Picture

def index(request):
    return render_to_response("index.html", {})  

def home(request):    
    albums = Album.objects.all()
    
    return render_to_response("home.html", {'album' : albums}, context_instance=RequestContext(request))

def edit(request): 
    return render_to_response("edit.html", {}, context_instance=RequestContext(request))

def delete(request, albumid = None):
    if albumid:
        album = get_object_or_404(Album, id=albumid)
        album.delete()
    return HttpResponseRedirect('/home/') 

def save(request):
    if request.method == 'POST':
        #validate???
        album = Album()
        album.title = request.POST.get('title','')
        #TODO:set time-zone in profile
        album.date = datetime.utcnow().replace(tzinfo=utc)
        album.link = 'http://i.pinger.pl/pgr151/04058fee002b47de511554b2/the_mane_six__group_hug___mlp_fim_vector_by_kirklands_girl39-d5mqlzq%5B1%5D.png'
        album.save()
        
        layouts = simplejson.loads(request.POST.get('layouts'))
        images = simplejson.loads(request.POST.get('images'))

        for i in range(0, len(layouts)):
            page = Page(layout=layouts[i], containingAlbum=album)
            page.save()
            for j in range(0, len(images[i])):
                image = Picture(title=images[i][j]["caption"], source=images[i][j]["src"], containingPage=page)
                image.save()
        
        return HttpResponseRedirect('/home/')