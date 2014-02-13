from django.shortcuts import render_to_response, get_object_or_404
from django.http import  HttpResponseRedirect
from django.template import RequestContext
from django.utils.timezone import utc
from django.utils import simplejson

from django.contrib.auth import authenticate
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
    
from datetime import datetime

from hashlib import sha1, md5
from models import Album, Page, Picture, Payment, MyRegistrationForm, UserProfileForm

# Session handling
def register_user(request):
    #if the form has been POSTed
    if request.method == 'POST':
        #get the form
        form = MyRegistrationForm(request.POST)
        #check if it's valid
        if form.is_valid():
            #save the form
            form.save()
            #show message to the user
            messages.success(request,'Congratulations! You have registered successfully! Now you can log in.')
            return HttpResponseRedirect('/')
        else:
            #show errors to the user
            return render_to_response("index.html", {'form': form}, context_instance=RequestContext(request))

def login(request):
    #get the name and password
    name = request.POST.get('loginname', '')
    passwd = request.POST.get('loginpasswd', '')
    #get the user
    user = authenticate(username = name, password = passwd)
    #if the user is valid log in
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect('/home/')
    else:
        return HttpResponseRedirect('/')
            
def logout(request):
    #log out the user
    auth.logout(request)
    return HttpResponseRedirect('/')

# Main Methods


def index(request):
    #if the user is already logged in redirect him to the home page
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home/')
    else:
        form = MyRegistrationForm()
        return render_to_response("index.html", {'form': form}, context_instance=RequestContext(request))  

@login_required(login_url='/')
def home(request):
    #get the user's albums from the database
    albums = Album.objects.filter(owner = request.user)
    return render_to_response("home.html", {'username' : request.user, 'album' : albums}, context_instance=RequestContext(request))

@login_required(login_url='/')
#the albumid is none when the user creates a new album
def edit(request, albumid = None):
    #if the album already exists (modify)
    if albumid:
        #find the album
        album = Album.objects.get(id = albumid)
        
        lays = {}
        imgs = {}
        #get the album informations
        for l in album.pages.all():
            lays[l.id] = l.layout
            for i in l.pictures.all():
                imgs[i.id] = {"title" : i.title, "source" : i.source}
        
        #convert to json form
        layouts = simplejson.dumps(lays, indent = 4)
        images = simplejson.dumps(imgs, indent = 4)
        
        return render_to_response("edit.html", {'album' : album, 'layouts' : layouts, 'images' : images, 'username': request.user}, context_instance=RequestContext(request))
    else:
        return render_to_response("edit.html", {'username': request.user}, context_instance=RequestContext(request))

def change_user_data(request):
    if request.method == 'POST':
        form = UserProfileForm()
        if form.is_valid():
            form.save()
            messages.success(request,'Your data has been changed!')
            return HttpResponseRedirect('/')
        else:
            return render_to_response("index.html", {}, context_instance=RequestContext(request))


#delete album
@login_required(login_url='/')
def delete(request, albumid):
    if albumid:
        album = get_object_or_404(Album, id=albumid)
        album.delete()
    return HttpResponseRedirect('/home/') 

#save album changes
@login_required(login_url='/')
def save(request):
    if request.method == 'POST':
        #validate???
        #get the information from the form
        layouts = simplejson.loads(request.POST.get('layouts'))
        images = simplejson.loads(request.POST.get('images'))
        #check if the album already existed
        albumid = request.POST.get('albumid', '')
        #if yes
        if albumid != '':
            #get the old album
            album = Album.objects.get(id = albumid)
            #delete the old information
            for l in album.pages.all():
                l.pictures.all().delete()
            album.pages.all().delete()
        #if not         
        else:
            #create new album
            album = Album()
            #TODO:set time-zone in profile
            #set creation date
            album.date = datetime.utcnow().replace(tzinfo=utc)
            #create unique link
            album.link = sha1(album.title + album.date.isoformat()).hexdigest()
            #set owner
            album.owner = request.user

        #change the title
        album.title = request.POST.get('title','')
        
        #find the first avalaible picture in the album
        i = 0
        j = 0
        found = False
        while i < len(images) and not found:
            while j < len(images[i]) and not found:
                if images[i][j]["src"] != '':
                    found = True
                j += 1
            i += 1
        
        #set as a cover on the home page
        if found:
            album.cover = images[i - 1][j - 1]["src"]
        #else use a general image
        else:
            album.cover = "/Static/images/album.png"
        
        #check if the album is public
        if (request.POST.get('public') == 'public'):
            album.public = True
        else:
            album.public = False
            
        #save the album
        album.save()
        
        #save the pages and the images
        for i in range(0, len(layouts)):
            page = Page(layout=layouts[i], containingAlbum = album)
            page.save()
            for j in range(0, len(images[i])):
                image = Picture(title=images[i][j]["caption"], source=images[i][j]["src"], containingPage = page)
                image.save()
        
        return HttpResponseRedirect('/home/')

#View album
def view(request, albumlink):
    #get the album
    album = Album.objects.get(link = albumlink)
    #check if the album is avalaible for the user
    if (request.user == album.owner or album.public): #TODO: do it on the client side
        lays = {}
        imgs = {}
        #send the album data to the client
        for l in album.pages.all():
            lays[l.id] = l.layout
            for i in l.pictures.all(): 
                imgs[i.id] = {"title" : i.title, "source" : i.source}
            
        layouts = simplejson.dumps(lays, indent = 4)
        images = simplejson.dumps(imgs, indent = 4)
    
        return render_to_response("view.html", {'album' : album, 'layouts' : layouts, 'images' : images, 'username': request.user}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')

#list public avalaible albums
def explore(request):
    album = Album.objects.filter(public = True)
    return render_to_response("explore.html", {'album': album, 'username': request.user})

#Payment

#order details
@login_required(login_url='/')
def pay(request):
    #generate pid for the transaction
    if request.method == 'POST':
        #save the album link as id
        request.session["albumlink"] = request.POST.get('albumlink')
        album = Album.objects.get(link = request.session["albumlink"])
        pagenum = album.pages.all().count()
        return render_to_response("details.html", {'album' : album, 'pagenum': pagenum, 'username': request.user}, context_instance=RequestContext(request))

#confirm the details
def confirm(request):
    if request.method == 'POST':
        #save the order details
        request.session["name"] = request.POST.get("name")
        request.session["country"] = request.POST.get("country")
        request.session["postcode"] = request.POST.get("postcode")
        request.session["address"] = request.POST.get("address")
        request.session["quantity"] = request.POST.get("quantity")
        request.session["mail"] = request.POST.get("mail")
        request.session["sum"] = request.POST.get("sum")
        
        #generate checksum
        pid = md5(request.session["albumlink"] + datetime.utcnow().replace(tzinfo=utc).isoformat()).hexdigest()
        SID = "Moments"
        SECRET_KEY = "61d78fc36457dfe32acd8a3731ba71a6"
        checksumstr = "pid=%s&sid=%s&amount=%s&token=%s"%(pid, SID, request.session["sum"], SECRET_KEY)
        m = md5(checksumstr)
        checksum = m.hexdigest()
        
        album = Album.objects.get(link = request.session["albumlink"])
        
        return render_to_response("confirm.html", { "session" : request.session, 'pid' : pid, 'sid' : SID, 'checksum' : checksum, 'username': request.user, 'album': album })   

#if the payment was successful
@login_required(login_url='/')
def success(request):
    #send an email to the customer
    subject = 'order details'
    message = 'Thanks for buying the album you can access the online form at'
    sender = 'Moments'
    recipients = request.session["mail"]
    send_mail(subject, message, sender, recipients)
    
    if request.method == 'GET':
        print "pid: " + request.GET.get('pid')
        print "ref: " + request.GET.get('ref')
        print "checksum: " + request.GET.get('checksum')
        
        payment = Payment()
        payment.pid = request.GET.get('pid')
        payment.date = datetime.utcnow().replace(tzinfo=utc)
        payment.price = request.session['sum']
        payment.reference = request.GET.get('ref')
        album = Album.objects.get(link = request.session['albumlink'])
        payment.item = album
        payment.buyer = request.user
        
        payment.save()
        
    return render_to_response("success.html", {'username': request.user})

#if the payment was canceled
def cancel(request):
    return HttpResponseRedirect('/home/')

#settings page
@login_required(login_url='/')
def settings(request):
    payments = Payment.objects.filter(buyer = request.user)
    
    return render_to_response("settings.html", {'username' : request.user, 'payments': payments}, context_instance=RequestContext(request))
