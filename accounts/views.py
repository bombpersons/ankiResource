from django.shortcuts import *
from django.http import *
from django.core.urlresolvers import *
from django.contrib import auth
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from ankiResource.accounts.forms import LoginForm, RegisterForm
from ankiResource.accounts import models

# ----------------------------- INDEX ----------------------------------
# Shows the accounts index page (redirects to profile if you are logged in)
@login_required
def index(request):
	#redirect to users profile page
	return HttpResponseRedirect("/accounts/profile/" + str(request.user.id))

# ------------------------------ PROFILE -------------------------------
# View profile information
def profile(request, account_id):
	#Grab information about profile
	try:
		profile = models.Profile.objects.get(pk=account_id)
	except models.Profile.DoesNotExist:
		# Make a profile if the user doesn't have one
		profile = models.Profile(user_id=account_id)
		profile.save()
	
	profile = models.Profile.objects.get(pk=account_id)
	
	#Send information to template
	dic = {
		'profile': profile,
	}
	
	return render_to_response("accounts/profile.html", dic, context_instance=RequestContext(request))

# ----------------------------- REGISTER -------------------------------
# Registers a user
def register(request):
	#If we get post data, assume user has already filled form.
	#We need to validate the data.
	if request.method == "POST":
		form = RegisterForm(request.POST)
		
		#Validate
		if form.is_valid():
			
			#Cool, make the user and profile
			newUser = auth.models.User.objects.create_user(form.cleaned_data['username'],
							form.cleaned_data['email'],
							form.cleaned_data['password'],
			)
			newUser.is_active = True
			newUser.save()
			
			
			newProfile = models.Profile(user_id=newUser.id)
			newProfile.save()
			
			#Now redirect to success page
			return HttpResponseRedirect("/accounts/success/?registered=True")
		
		#If the form isn't valid redirect to show the user the errors	
		else:
			return HttpResponseRedirect("/accounts/register")
	
	#If we aren't getting post data, just show a blank form
	else:
		form = RegisterForm()
	
	dic = {
		'form': form,
	}
	
	return render_to_response("accounts/register.html", dic, context_instance=RequestContext(request))


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
