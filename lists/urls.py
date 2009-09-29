from django.conf.urls.defaults import *
from tagging.views import tagged_object_list
from ankiResource.sentences.models import Sentence

urlpatterns = patterns('',
    # Example:
    # (r'^anki_site/', include('anki_site.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
	
	#shows a list
	url(r'^list/(?P<list_id>\d+)$', 'ankiResource.lists.views.show_list', name="url_sentences_show_list"),
	
	#adds a list
	url(r'^newlist/$', 'ankiResource.lists.views.new_list', name="url_sentences_new_list"),
			
	# ------------------------- AJAX -----------------------------------
	# Add / Removes / Confirms a sentence in a list
	url(r'^ajax/list/add/$', 'ankiResource.lists.views.ajax_list_edit', name="url_sentences_ajax_list_edit"),
)

