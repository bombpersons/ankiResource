from django.conf.urls.defaults import *
import settings

urlpatterns = patterns('',
	# Index Page
	url(r'^$', 'ankiResource.manager.views.index', name="url_manager_index"),
	
	# ** AJAX VIEWS **
	url(r'^ajax/modify/$', 'ankiResource.manager.views.modify', name="url_manager_ajax_modify"),

	# Start with a list
	url(r'^list/(?P<start_list_id>\d+)$', 'ankiResource.manager.views.start_list', name="url_manager_start_list"),
	
	# Edit all lists
	url(r'^list/all/$', 'ankiResource.manager.views.all_lists', name="url_manager_all_lists"),

)
