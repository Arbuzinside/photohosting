from django.db import models
from django.forms import ModelForm

class Album(models.Model):
    title = models.CharField(max_length = 255)
    date = models.DateTimeField()
    link = models.URLField()
    'Preview picture - for slideshows'
    'Owner = models.ForeignKey()'

class AlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = ('title', )

class Page(models.Model):
    layout = models.IntegerField()
    containingAlbum = models.ForeignKey(Album, related_name="Pages")
    
class Picture(models.Model):
    title = models.CharField(max_length = 255)
    source = models.URLField()
    containingPage = models.ForeignKey(Page, related_name="Pictures")