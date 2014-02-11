from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webSIte.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/$', include(admin.site.urls)),
    
    url(r'', include('social_auth.urls')),
    #url(r'^login/$', RedirectView.as_view('/login/facebook'),
    #User auth urls
    #url(r'^accounts/login/$',   'PhotoAlbum.auth_views.login'),
    #url(r'^accounts/auth/$',    'PhotoAlbum.auth_views.auth_view'),
    #url(r'^accounts/loggedin/$',  'PhotoAlbum.auth_views.loggedin'),
    #url(r'^accounts/invalid/$',    'PhotoAlbum.auth_views.invalid_login'),
    
    #User reg urls
    url(r'^accounts/register/$',  'PhotoAlbum.views.register_user'),
    #url(r'^accounts/register_success/$', 'PhotoAlbum.auth_views.register_success'),
    
    url(r'^login/$', 'PhotoAlbum.views.login', name='login'),
    url(r'^logout/$', 'PhotoAlbum.views.logout', name='logout'),
    url(r'^home/$', 'PhotoAlbum.views.home', name='home'),
    url(r'^explore/$', 'PhotoAlbum.views.explore', name='explore'),
    url(r'^home/edit/$', 'PhotoAlbum.views.edit', name='edit'),
    url(r'^home/edit/(?P<albumid>\d+)/$', 'PhotoAlbum.views.edit', name='edit'),
    url(r'^delete/(?P<albumid>\d+)/$', 'PhotoAlbum.views.delete', name='delete'),
    url(r'^save/$', 'PhotoAlbum.views.save', name='save'),
    url(r'^view/(?P<albumlink>[a-f0-9]+)/$', 'PhotoAlbum.views.view', name='view'),
    url(r'^$', 'PhotoAlbum.views.index', name='index'),
)
