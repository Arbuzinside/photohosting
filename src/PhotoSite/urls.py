from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webSIte.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/$', include(admin.site.urls)),
    url(r'^home/$', 'PhotoAlbum.views.home', name='home'),
    url(r'^home/edit/$', 'PhotoAlbum.views.edit', name='edit'),
    url(r'^delete/(?P<albumid>\d+)/$', 'PhotoAlbum.views.delete', name='delete'),
    url(r'^save/$', 'PhotoAlbum.views.save', name='save'),
    url(r'^$', 'PhotoAlbum.views.index', name='index'),
)
