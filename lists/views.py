from django.shortcuts import *
from django.http import *
from django.core.urlresolvers import *
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User

from models import List
from ankiResource.sentences.models import Sentence
from ankiResource.sentences.forms import ListForm
from forms import QuicklistForm

from export import TextFileListExporter

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
	return render_to_response("lists/show_list.html", dic, context_instance=RequestContext(request))

# ---------------------------------- EXPORT LIST -----------------------
def export_list(request, list_id):
	# Make a dictionary
	dic = {
	}
	
	# Try and grab the list
	try:
		list = List.objects.get(pk=list_id)
	except:
		raise Http404
		
	# Put it into the dictionary, incase the template wants the info
	dic.update({
		'list': list,
	})
	
	# Check whether or not the user has specified which exporter to use.
	if 'export_type' not in request.GET:
		# Add a not in the dict telling the template
		dic.update({ 'no_export_type': True })
		
		# Render
		return render_to_response("lists/export_list.html", dic, context_instance=RequestContext(request))
	
	# Check what format the user wants to export to
	if request.GET['export_type'] == "Text":
			# User wants to export as a text file
			exporter = TextFileListExporter()
	
	# Not supported
	else:
		# Tell the template that, that format is not supported.
		dic.update({ 'not_supported': True })
		
		# Render the template
		return render_to_response("lists/export_list.html", dic, context_instance=RequestContext(request))
	
	# Let's continue exporting.
	# Load the list
	exporter.readList(list)
	
	# Export the to file and get the name
	file = exporter.export()
	
	# If that was succesful...
	if file:
		
		# Forward the user to download the file
		response = HttpResponse(file.read(), mimetype='application/octet-stream')
		response['Content-Disposition'] = 'attachment; filename=' + exporter.filename
		return response
	
	# We didn't get a filename...
	else:
		
		# For some reason we didn't get a filename, tell the template
		dic.update({ 'error': True })
		return render_to_response("lists/export_list.html", dic, context_instance=RequestContext(request))
			
	

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
		return render_to_response("lists/new_list.html", dic, context_instance=RequestContext(request))
	
	#If we aren't already adding, draw a blank form.
	else:
		form = ListForm()
		
		#make a dic to hold the form
		dic = {'form': form}
		
		#render the page
		return render_to_response("lists/new_list.html", dic, context_instance=RequestContext(request))
		
@login_required
def save_quick_list(request):
	if request.method == "POST":
		#validate the data
		form = QuicklistForm(request.POST)
		
		#continue if the form is valid
		if form.is_valid():
			# Add the sentence
			new_list = List(name=form.cleaned_data['name'],
							open=False,
							)
			new_list.save()			
			new_list.user.add(request.user)
			
			uql = request.user.get_profile().quick_list
			
			for sentence in uql.sentence.all():
				new_list.sentence.add(sentence)
			
			new_list.save()
			
			id=new_list.id
			
			#Redirect the user to the new list.
			return HttpResponseRedirect(reverse('ankiResource.lists.views.show_list', args=(id,)))
			
		#add the form to the dic
		dic = {'form': form}
	
		#render the page
		return render_to_response("lists/new_list.html", dic, context_instance=RequestContext(request))
	
	#If we aren't already adding, draw a blank form.
	else:
		form = QuicklistForm()
		
		#make a dic to hold the form
		dic = {'form': form}
		
		#render the page
		return render_to_response("lists/save_quick_list.html", dic, context_instance=RequestContext(request))		

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
	return render_to_response("lists/ajax/list_edit.html", dic, context_instance=RequestContext(request))
