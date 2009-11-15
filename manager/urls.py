from django.conf.urls.defaults import *
import settings

urlpatterns = patterns('',
	# Index Page
	url(r'^$', 'ankiResource.manager.views.index', name="url_manager_index"),
	
	# Start with a list
	url(r'^list-id=(?P<start_list_id>\d+)$', 'ankiResource.manager.views.start_list', name="url_manager_start_list"),
	
	# Edit all lists
	url(r'^all-lists/$', 'ankiResource.manager.views.all_lists', name="url_manager_all_lists"),
	
	# ----------------------- AJAX --------------------------------------------
	# Modify list (rearrange sentences etc)
	url(r'^ajax/modify/$', 'ankiResource.manager.views.modify', name="url_manager_ajax_modify"),

	# Retrieves a list in JSON format
	url(r'^ajax/list/get/(?P<list_id>\d+)$', 'ankiResource.manager.views.ajax_list_get_json', 		name="url_sentences_ajax_list_get_json"),

)
