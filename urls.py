from django.conf.urls.defaults import *
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
	(r'^admin/(.*)', admin.site.root),

	# Haystack
	(r'^search/', include('haystack.urls')),

	#main (root) app
	(r'^', include('ankiResource.main.urls')),

	#accounts app
	(r'^accounts/', include('ankiResource.accounts.urls')),

	#sentences app
	(r'^sentences/', include('ankiResource.sentences.urls')),
	
	#list app
	(r'^lists/', include('ankiResource.lists.urls')),
	
	#manager apP
	(r'^manager/', include('ankiResource.manager.urls')),

	#-------------------------------------------------------------------
	#-------------------------------------------------------------------
	#static files (don't use this in a production environment!!!1!)
	(r'^static/(?P<path>.*)$', 'django.views.static.serve',
		{'document_root': settings.MEDIA_ROOT}),

)
