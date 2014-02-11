from django.shortcuts import render_to_response, get_object_or_404
from django.http import  HttpResponseRedirect
from django.template import RequestContext
from django.utils.timezone import utc
from django.utils import simplejson

from django.contrib.auth import authenticate
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required

from datetime import datetime

from hashlib import sha1, md5
from models import Album, Page, Picture, MyRegistrationForm

# Session handling

def register_user(request):
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Congratulations! You have registered successfully! Now you can log in.')
            return HttpResponseRedirect('/')
        else:
            return render_to_response("index.html", {'form': form}, context_instance=RequestContext(request))

def login(request):
    name = request.POST.get('loginname', '')
    passwd = request.POST.get('loginpasswd', '')
    user = authenticate(username = name, password = passwd)

    if user is not None:
        if user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect('/home/')
    else:
        return HttpResponseRedirect('/')
            
    
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

# Main Methods

def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home/')
    else:
        form = MyRegistrationForm()
        return render_to_response("index.html", {'form': form}, context_instance=RequestContext(request))  

@login_required(login_url='/')
def home(request):
    albums = Album.objects.filter(owner = request.user)
    return render_to_response("home.html", {'username' : request.user, 'album' : albums}, context_instance=RequestContext(request))

@login_required(login_url='/')
def edit(request, albumid = None): 
    if albumid:
        album = Album.objects.get(id = albumid)
        
        lays = {}
        imgs = {}
        
        for l in album.pages.all():
            lays[l.id] = l.layout
            for i in l.pictures.all():
                imgs[i.id] = {"title" : i.title, "source" : i.source}
            
        layouts = simplejson.dumps(lays, indent = 4)
        images = simplejson.dumps(imgs, indent = 4)
        
        return render_to_response("edit.html", {'album' : album, 'layouts' : layouts, 'images' : images, 'username': request.user}, context_instance=RequestContext(request))
    else:
        return render_to_response("edit.html", {'username': request.user}, context_instance=RequestContext(request))

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
            
            for l in album.pages.all():
                l.pictures.all().delete()
            
            album.pages.all().delete()            
        else:
            album = Album()
            album.title = request.POST.get('title','')
            #TODO:set time-zone in profile
            album.date = datetime.utcnow().replace(tzinfo=utc)
            album.link = sha1(album.title + album.date.isoformat()).hexdigest()
            album.owner = request.user

        i = 0
        j = 0
        found = False
        while i < len(images) and not found:
            while j < len(images[i]) and not found:
                if images[i][j]["src"] != '':
                    found = True
                j += 1
            i += 1
        
        if found:
            album.cover = images[i - 1][j - 1]["src"]
        else:
            album.cover = "/Static/images/album.png"
        
        if (request.POST.get('public') == 'public'):
            album.public = True
        else:
            album.public = False
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
    if (request.user == album.owner or album.public): #TODO: do it on the client side
        lays = {}
        imgs = {}
        
        for l in album.pages.all():
            lays[l.id] = l.layout
            for i in l.pictures.all():
                imgs[i.id] = {"title" : i.title, "source" : i.source}
            
        layouts = simplejson.dumps(lays, indent = 4)
        images = simplejson.dumps(imgs, indent = 4)
    
        return render_to_response("view.html", {'album' : album, 'layouts' : layouts, 'images' : images, 'username': request.user}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')

def explore(request):
    album = Album.objects.filter(public = True)
    return render_to_response("explore.html", {'album': album, 'username': request.user})

def pay(request):
    #generate pid
    if request.method == 'POST':
        request.session["albumlink"] = request.POST.get('albumlink')
        return render_to_response("details.html", {}, context_instance=RequestContext(request))
        
def confirm(request):
    if request.method == 'POST':
        #order details
        request.session["name"] = request.POST.get("name")
        request.session["country"] = request.POST.get("country")
        request.session["postcode"] = request.POST.get("postcode")
        request.session["address"] = request.POST.get("address")
        request.session["quantity"] = request.POST.get("quantity")
        request.session["mail"] = request.POST.get("mail")
        request.session["sum"] = int('0' + request.session["quantity"]) * 10 #TODO: price of the album?
        
        #generate checksum
        pid = "pid" #md5(request.session["albumlink"] + datetime.utcnow().replace(tzinfo=utc).isoformat()).hexdigest()
        sid = "Moments"
        secret_key = "61d78fc36457dfe32acd8a3731ba71a6"
        checksumstr = "pid=%s&sid=%s&amount=%s&token=%s"%(pid, sid, request.session["sum"], secret_key)
        m = md5(checksumstr)
        checksum = m.hexdigest()
        
        print checksum  + " check"
        
        return render_to_response("confirm.html", { "session" : request.session, 'pid' : pid, 'sid' : sid, 'checksum' : checksum })        