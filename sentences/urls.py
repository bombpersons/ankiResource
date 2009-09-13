from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^anki_site/', include('anki_site.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

	#sentences url's
	url(r'^$', 'ankiResource.sentences.views.index', name="url_sentences_index"),
	url(r'^(?P<sentence_id>\d+)$', 'ankiResource.sentences.views.sentence', name="url_sentences_sentence"),
	url(r'^new/$', 'ankiResource.sentences.views.new', name="url_sentences_new"),
)
