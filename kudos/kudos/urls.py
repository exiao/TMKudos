from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#from haystack.views import SearchView

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'kudosapp.views.home', name='home'),
    url(r'^directory/$', 'kudosapp.views.dir', name='dir'),
    #url(r'^$', 'kudosapp.views.basic_search', name='search'),
    url(r'^search/$', 'kudosapp.views.basic_search', name='search'),

    # url(r'^$', SearchView(), name='haystack_search'),
    # url(r'^kudos/', include('kudos.foo.urls')),

    #Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    #Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
