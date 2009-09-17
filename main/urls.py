from django.conf.urls.defaults import *
import settings

urlpatterns = patterns('',
	url(r'^$', 'ankiResource.main.views.index', name="url_main_index"),
	
)
