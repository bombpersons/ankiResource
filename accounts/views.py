from django.shortcuts import *
from django.http import *
from django.core.urlresolvers import *
from django.contrib import auth
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from ankiResource.accounts.forms import LoginForm
import ankiResource.sentences.models as m

# ----------------------------- INDEX ----------------------------------
# Shows the accounts index page (redirects to profile if you are logged in)
@login_required
def index(request):
	#redirect to users profile page
	return HttpResponseRedirect("/accounts/profile/" + str(request.user.id))


# ----------------------------- LOGIN ----------------------------------
# Logs a user in
def loginUser(request):
	#If username and password POST values exist, try and login
	if 'username' in request.POST and 'password' in request.POST:
		#First validate the data, then authenticate
		form = LoginForm(request.POST)
		if form.is_valid():			
			user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
			
			#If that was succesful, log them in
			if user != None:
				#check if the user isn't unactive (not activated or banned)
				if user.is_active:
					auth.login(request, user)
					
					#Now redirect to success page
					if 'next' not in request.GET:
						return HttpResponseRedirect("/accounts/success/?login=True")
					else:
						return HttpResponseRedirect(request.GET['next'])
			
			#User is banned or has not activated their account
			else:
				return HttpResponseRedirect("?not_active=True")
			
			#If it failed...	
			if user == None:
				#Send a GET var saying we failed to login last time.
				
				#Now redirect to the page
				return HttpResponseRedirect("?failed_login=True")
	else:
		#make a blank form
		form = LoginForm()
	
	#If user isn't trying to login yet, draw the form
	dic = {'form': form}
	
	#add get vars to dic so the template can use those values
	dic.update(request.GET)
	
	#render the page
	return render_to_response("accounts/login.html", dic, context_instance=RequestContext(request))

#------------------------- LOGOUT --------------------------------------
# Logs a user out.
@login_required
def logoutUser(request):
	#logout
	auth.logout(request)
	
	#redirect to success
	return HttpResponseRedirect("/accounts/success/?logout=True")
	
#----------------------- SUCCESS ---------------------------------------
# Displays success messages. 
def success(request):
	return render_to_response("accounts/success.html", request.GET, context_instance=RequestContext(request))
