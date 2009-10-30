from django.conf.urls.defaults import *
import settings

urlpatterns = patterns('',
	# Index Page
	url(r'^$', 'ankiResource.manager.views.index', name="url_manager_index"),
	
	# Start with a list
	url(r'^list/(?P<start_list_id>\d+)$', 'ankiResource.manager.views.start_list', name="url_manager_start_list"),

)
