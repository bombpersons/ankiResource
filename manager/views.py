from django.utils import simplejson
from django.shortcuts import *
from django.http import *
from django.core.urlresolvers import *
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User

from ankiResource import settings

from ankiResource.lists.models import List
from ankiResource.sentences.models import Sentence

# --------------------------- INDEX ------------------------------------
def index(request):
	# Dictionary
	dic = {
	
	}
	
	
	
	# Render the page
	return render_to_response("manager/index.html", dic, context_instance=RequestContext(request))

# ------------------------- AJAX ---------------------------------------
# ----------------------------------------------------------------------
# Called when javascript wants to modify a list
def modify(request):
	# Make sure we have post data
	if request.POST:
		
		# Check if action is in the post data
		if 'action' in request.POST:
			
			# What are we doing?
			if request.POST['action'] == "delete":
				# Okay, javascript wants us to delete an item from a list.
				# Check if the user has permission to do it
				# 
				# If a parent list is in the post data, remove the sentence
				# from the list. If there is no parent list, delete the
				# sentence if possible.
				if 'source' in request.POST:
					if 'sentences' in request.POST:
						
						# Get the source list
						source = get_object_or_404(List, pk=request.POST['source'])
						
						# Check if we have permission to do this
						if request.user in source.user:
							
							# Remove the sentences from source
							for sentence in request.POST['sentences'].split():
								curr = get_object_or_404(Sentence, pk=sentence)
								source.remove(curr)
							
							# Return success
							return HttpResponse(simplejson.dump({'Success': True}, mimetype='application/javascript'))
				
				else:
					if 'sentences' in request.POST:
						
						# Get the sentences
						sentence_ids = request.POST['sentences'].split()
						
						# Delete them (Check each time if we have permission)
						for sentence_id in sentence_ids:
							sentence = Sentence.objects.get(pk=sentence_id)
							if request.user in sentence.user:
								sentence.delete()
						
						# Return success
						return HttpResponse(simplejson.dump({'Success': True}, mimetype='application/javascript'))
			
			elif request.POST['action'] == "move":
				# Okay, Javascript wants us to move some sentences from one list to another. 
				# Sentences are removed from the source and moved to the dest
				if 'dest' in request.POST and 'source' in request.POST:
					# Get a reference to the list
					dest = get_object_or_404(List, pk=request.POST['dest'])
					source = get_object_or_404(List, pk=request.POST['source'])
				
					# Check if we have permission
					if request.user in dest.user and request.user in source.user:
					
						if 'sentences' in request.POST:
							
							# Add these sentences to the list
							for sentence_id in request.POST['sentences'].split():
								sentence = Sentence.objects.get(pk=sentence_id)
								dest.sentences.add(sentence)
								source.sentences.remove(sentence)
							
							# Return success
							return HttpResponse(simplejson.dump({'Success': True}, mimetype='application/javascript'))
						
			elif request.POST['action'] == "copy":
				# Okay, Javascript wants us to copy some sentences from one
				# list to another. 
				#
				# A source list isn't really needed, since we aren't modify it.
				if 'dest' in request.POST:
					# Get the list
					dest = get_object_or_404(List, pk=request.POST['dest'])
					
					# Check if we have permission to write to the list
					if request.user in dest.user:
						
						if 'sentences' in request.POST:
							
								# Add these sentences to the list
								for sentence_id in request.POST['sentences'].split():
									sentence = Sentence.objects.get(pk=sentence_id)
									dest.sentence.add(sentence)
								
								# Return success
								return HttpResponse(simplejson.dump({'Success': True}, mimetype='application/javascript'))
								
	# If we get here an error has happened,
	raise Http500
														
	
def start_list(request, start_list_id):

	dic = {'start_list_id' : start_list_id
	}

	# dic = start_list_id.render_to_json not implemented yet!
	
	return render_to_response("manager/start_list.html", dic, context_instance=RequestContext(request))
