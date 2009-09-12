from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^anki_site/', include('anki_site.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

	#sentences url's
	(r'^$', 'anki_site.sentences.views.index'),
	(r'^(?P<sentence_id>\d+)$', 'anki_site.sentences.views.sentence'),
	(r'^new/$', 'anki_site.sentences.views.new'),
)
