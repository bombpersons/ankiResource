from django.conf.urls.defaults import *

urlpatterns = patterns('',
	#INDEX
	url(r'^$', 'ankiResource.accounts.views.index', name="url_accounts_index"),
	
	#PROFILE
	url(r'^profile/(?P<account_id>\d+)$', 'ankiResource.accounts.views.profile', name="url_accounts_profile"),
	
	#REGISTER
	url(r'^register/$', 'ankiResource.accounts.views.register', name="url_accounts_register"),
	
	#LOGIN
	url(r'^login/$', 'ankiResource.accounts.views.loginUser', name="url_accounts_login"),
		
	#LOGOUT
	url(r'^logout/$', 'ankiResource.accounts.views.logoutUser', name="url_accounts_logout"),
	
	#Succes Message
	url(r'^success/$', 'ankiResource.accounts.views.success', name="url_accounts_success"),
)
