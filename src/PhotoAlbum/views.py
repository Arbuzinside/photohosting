from django.shortcuts import render_to_response
from models import Album, Page, Picture

def show_picture(request):
    return render_to_response("picture.html", {})  