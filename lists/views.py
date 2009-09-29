from django.shortcuts import *
from django.http import *
from django.core.urlresolvers import *
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User

from models import List
from ankiResource.sentences.models import Sentence
from ankiResource.sentences.forms import ListForm

# ------------------------------- SHOW LIST ----------------------------
def show_list(request, list_id):
	# Make a dic
	dic = {
	}
	
	# Grab the list
	try:
		list = List.objects.get(pk=list_id)
	except:
		raise Http404
		
	# Put it into the dict
	dic.update({ 'list': list })
	
	# Render the template
	return render_to_response("sentences/show_list.html", dic, context_instance=RequestContext(request))

#---------------------Create a new list------------------#
@login_required
def new_list(request):
	if request.method == "POST":
		#validate the data
		form = ListForm(request.POST)
		
		#continue if the form is valid
		if form.is_valid():
			# Add the sentence
			new_list = List(name=form.cleaned_data['name'],
							open=form.cleaned_data['open'],
							)
			new_list.save()			
			new_list.user.add(request.user)
			new_list.save()
			
			id=new_list.id
			
			#Redirect the user to the new list.
			return HttpResponseRedirect(reverse('ankiResource.lists.views.show_list', args=(id,)))
			
		#add the form to the dic
		dic = {'form': form}
	
		#render the page
		return render_to_response("sentences/new_list.html", dic, context_instance=RequestContext(request))
	
	#If we aren't already adding, draw a blank form.
	else:
		form = ListForm()
		
		#make a dic to hold the form
		dic = {'form': form}
		
		#render the page
		return render_to_response("sentences/new_list.html", dic, context_instance=RequestContext(request))
		
		

# //////////////////////////////////////////////////////////////////////
# ------------------------------- AJAX ---------------------------------
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# ---------------------------- ADD / REMOVE TO LIST --------------------
@login_required
def ajax_list_edit(request):	
	# Make sure the list and sentence exist
	list = List.objects.get(pk=request.POST['list'])
	sentence = Sentence.objects.get(pk=request.POST['sentence'])
	
	# Make a dic
	dic = {
	}
	
	# K, now check if the user has permissions to do this.
	if request.user in list.user.all() or list.open:
		# Add / Remove the sentence to the list
		if 'add' in request.POST:
			if request.POST['add'] == "1":
				list.sentence.add(sentence)
				
				# Tell the template we succeeded
				dic.update({'success': True})
		
		if 'remove' in request.POST:
			if request.POST['remove'] == "1":
				list.sentence.remove(sentence)
				
				# Tell the template we succeeded
				dic.update({'success': True})
		
		# Check whether or not the sentence is in the list.
		if 'exists' in request.POST:
			if request.POST['exists'] == "1":
				if sentence in list.sentence.all():
					dic.update({'success': True})
				else:
					# Tell the template we failed
					dic.update({'success': False})
				
			
		# Save the list
		list.save()
		
	else:
		
		# Tell the template we failed =(
		dic.update({'success': False})
	
	#Render to template
	return render_to_response("sentences/ajax/list_edit.html", dic, context_instance=RequestContext(request))
