from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^anki_site/', include('anki_site.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

	#sentences url's
	url(r'^$', 'ankiResource.accounts.views.index', name="url_accounts_index"),
	#url(r'^profile/(?P<account_id>\d+)$', 'ankiResource.accounts.views.profile', name="url_accounts_profile"),
	#url(r'^register/$', 'ankiResource.accounts.views.register', name="url_accounts_register"),
	
	#LOGIN
	url(r'^login/$', 'ankiResource.accounts.views.loginUser', name="url_accounts_login"),
		
	#LOGOUT
	url(r'^logout/$', 'ankiResource.accounts.views.logoutUser', name="url_accounts_logout"),
	
	#Succes Message
	url(r'^success/$', 'ankiResource.accounts.views.success', name="url_accounts_success"),
)
