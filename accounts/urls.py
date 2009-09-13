from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^anki_site/', include('anki_site.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

	#sentences url's
	(r'^$', 'ankiResource.accounts.views.index'),
	(r'^profile/(?P<account_id>\d+)$', 'ankiResource.accounts.views.profile'),
	(r'^register/$', 'ankiResource.accounts.views.register'),
	(r'^login/$', 'ankiResource.accounts.views.loginUser'),
)
