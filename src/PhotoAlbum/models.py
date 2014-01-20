from django.db import models

class Album(models.Model):
    Title = models.CharField(max_length = 255)
    Date = models.DateTimeField()
    Link = models.URLField()
    'Owner = models.ForeignKey()'

class Page(models.Model):
    Layout = models.IntegerField()
    ContainingAlbum = models.ForeignKey(Album, related_name="Pages")
    
class Picture(models.Model):
    Title = models.CharField(max_length = 255)
    Source = models.URLField()
    Order = models.IntegerField()
    'ContainingPage = models.ForeignKey(Page, related_name="Pictures")'