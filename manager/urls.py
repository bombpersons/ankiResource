from django.conf.urls.defaults import *
import settings

urlpatterns = patterns('',
	# Index Page
	url(r'^$', 'ankiResource.manager.views.index', name="url_manager_index"),
	
	# ** AJAX VIEWS **
	url(r'ajax/modify$', 'ankiResource.manager.views.modify', name="url_manager_ajax_modify"),

)
