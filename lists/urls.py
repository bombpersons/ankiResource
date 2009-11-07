from django.conf.urls.defaults import *
from tagging.views import tagged_object_list
from ankiResource.sentences.models import Sentence

urlpatterns = patterns('',
	#shows a list
	url(r'^list/(?P<list_id>\d+)$', 'ankiResource.lists.views.show_list', name="url_sentences_show_list"),
	
	#shows all lists
	url(r'^all/$', 'ankiResource.lists.views.show_all', name="url_lists_show_all"),
	
	#exports a list
	url(r'^export/(?P<list_id>\d+)/$', 'ankiResource.lists.views.export_list', name="url_lists_export"),
	
	#adds a list
	url(r'^newlist/$', 'ankiResource.lists.views.new_list', name="url_sentences_new_list"),
	
	#saves quicklist
	url(r'^savequicklist/$', 'ankiResource.lists.views.save_quick_list', name="url_lists_savequicklist"),
			
	# ------------------------- AJAX -----------------------------------
	# Add / Removes / Confirms a sentence in a list
	url(r'^ajax/list/add/$', 'ankiResource.lists.views.ajax_list_edit', name="url_sentences_ajax_list_edit"),
	
	# Retrieves a list in JSON format
	url(r'^ajax/list/get/(?P<list_id>\d+)$', 'ankiResource.lists.views.ajax_list_get_json', name="url_sentences_ajax_list_get_json"),
)

