from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import login, logout
from django.views.generic.simple import redirect_to
from django.conf import settings

import dtestapp.views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dtestproj.views.home', name='home'),
    # url(r'^dtestproj/', include('dtestproj.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    #(r'^$', dtestapp.views.showRoom)    
    url(r'^accounts/login/$',  login),
    url(r'^accounts/logout/$', logout),
    url(r'^accounts/register/$', dtestapp.views.registerUser),
    url(r'^game/$', dtestapp.views.showRoom),
    url(r'^restart/$', dtestapp.views.restart),
    url(r'^$', redirect_to, {'url': '/game/'})
    
)
