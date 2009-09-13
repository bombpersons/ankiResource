from django.shortcuts import *
import ankiResource.sentences.models as m
from django.http import *
from django.core.urlresolvers import *
from django.contrib import auth

from ankiResource.accounts.forms import LoginForm
import datetime

# ----------------------------- INDEX ----------------------------------
# Shows the accounts index page (redirects to profile if you are logged in)
def index(request):
	
	return render_to_response("sentences/index.html", {'latest_sentences_list': latest_sentences_list})

# ----------------------------- LOGIN ----------------------------------
# Shows an individual sentence.
def loginUser(request):
	#If username and password POST values exist, try and login
	if 'username' in request.POST and 'password' in request.POST:
		#First validate the data, then authenticate
		form = LoginForm(request.POST)
		if form.is_valid():			
			user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
			
			#If that was succesful, log them in
			if user != None:
				auth.login(request, user)
				
				#Now redirect to success page
				return HttpResponseRedirect("success")
			
			#If it failed...	
			if user == None:
				#Fill in the post value telling the next view that we failed to login.
				request.POST['failed_login'] = True
				
				#Now redirect to the page
				return HttpResponseRedirect("")
	else:
		#make a blank form
		form = LoginForm()
	
	#If user isn't trying to login yet, draw the form
	dic = {'form': form}
	
	#If the user failed to login berfore, add that to dic, so that the template can display a message.
	#if 'failed_login' in request.POST:
	#	dic.append({'failed_login': request.POST['failed_login']})
	
	#render the page
	return render_to_response("accounts/login.html", dic)
