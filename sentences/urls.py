from django.conf.urls.defaults import *
from tagging.views import tagged_object_list
from ankiResource.sentences.models import Sentence

urlpatterns = patterns('',
    # Example:
    # (r'^anki_site/', include('anki_site.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

	#sentences url's
	#
	#sentence index
	url(r'^$', 'ankiResource.sentences.views.index', name="url_sentences_index"),
	
	#show sentences as a list
	url(r'^all/$', 'ankiResource.sentences.views.list', name="url_sentences_list"),

	#show all sentences containing tag
	url(r'^tag/(?P<tag>[^/]+)/$', 'tagging.views.tagged_object_list', dict(queryset_or_model=Sentence), name="url_sentences_tags"),
	
	#shows a specific sentence
	url(r'^(?P<sentence_id>\d+)$', 'ankiResource.sentences.views.sentence', name="url_sentences_sentence"),
	
	#makes a new sentence
	url(r'^new/$', 'ankiResource.sentences.views.new', name="url_sentences_new"),
		
	#deletes a sentence
	url(r'^delete/(?P<sentence_id>\d+)$', 'ankiResource.sentences.views.delete', name="url_sentences_delete"),
	
	#shows a list
	url(r'^list/(?P<list_id>\d+)$', 'ankiResource.sentences.views.show_list', name="url_sentences_show_list"),
	
	#adds a list
	url(r'^newlist/$', 'ankiResource.sentences.views.new_list', name="url_sentences_new_list"),
			
	# ------------------------- AJAX -----------------------------------
	# Add / Removes / Confirms a sentence in a list
	url(r'^ajax/list/add/$', 'ankiResource.sentences.views.ajax_list_edit', name="url_sentences_ajax_list_edit"),
)

