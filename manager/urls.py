from django.conf.urls.defaults import *
import settings

urlpatterns = patterns('',
	# Index Page
	url(r'^$', 'ankiResource.manager.views.index', name="url_manager_index"),

)
