from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^anki_site/', include('anki_site.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
	
	(r'^sentences/', include('anki_site.sentences.urls')),
	
	#static files (don't use this in a production environment!!!1!)
	(r'^Media/(?P<path>.*)$', 'django.views.static.serve',
		{'document_root': '/home/bombpersons/site/anki_site/Media'}),

)
