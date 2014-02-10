from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from models import MyRegistrationForm


def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('home.html', c)

def auth_view(request):
    name = request.POST.get('loginname', '')
    passwd = request.POST.get('loginpasswd', '')
    
    print "username: " + name + " " + passwd
    
    user = auth.authenticate(username = name, password = passwd)
    
    print "user authenticate: " + user.username
    
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/home', {'username': name})
    else:
        return HttpResponseRedirect('/')
    
def loggedin(request):
    return render_to_response('loggedin.html',
                               { 'full_name': request.user.username})

def invalid_login(request):
    return render_to_response('invalid_login.html')

def logout(request):
    auth.logout(request)
    return render_to_response('logout.html')

def register_user(request):
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/home', { 'username': request.user.username})
     
    args = {}
    args.update(csrf(request))
    
    args['form'] = MyRegistrationForm()
    
    return render_to_response('register.html', args)

def register_success(request):
    render_to_response('register_success.html')
    
    

