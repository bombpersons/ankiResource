from django.shortcuts import *
from django.http import *
from django.core.urlresolvers import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User

from haystack.query import SearchQuerySet

from ankiResource import settings
from ankiResource.uploading.functions import *
from ankiResource import accounts, media, lists
from ankiResource.lists.models import List
from ankiResource.sentences.forms import SentenceForm
from ankiResource.lists.forms import ListForm

from models import Sentence

# -----------------------------INDEX------------------------------------
# Shows the sentence index page
def index(request):
	#Get the latest 5 sentences to show on the main page
	latest_sentences_list = Sentence.objects.all().order_by('-pub_date')[:settings.ANKIRESOURCE_SENTENCES_INDEX_SENTENCE_NUM]
	
	dic = {
		'latest_sentences_list': latest_sentences_list,
	}
	
	return render_to_response("sentences/index.html", dic, context_instance=RequestContext(request))
	
# ----------------------------- LIST SENTENCES -------------------------
# Shows a list of sentences
def list(request):

	# Get page to render
	if 'page' in request.GET:
		page = request.GET['page']
	
	# If no page is specified, just display page 1
	else:
		page = 1
	
	#Get all sentences
	sentence_list = Sentence.objects.all().order_by('-pub_date')
	
	if request.user.is_authenticated():
		ql = request.user.get_profile().quick_list
	else:
		ql = None
	
	# Paginate
	sentence_paginator = Paginator(sentence_list, settings.ANKIRESOURCE_ITEMS_PER_PAGE)
	sentence_page = sentence_paginator.page(page)
	
	if request.user.is_authenticated():
		sentence_page_ql = [[sentence, ql.contains_sentence(sentence)] for sentence in sentence_page.object_list]
	else:
		sentence_page_ql = [[sentence, True] for sentence in sentence_page.object_list]
		
	#Send it all to template renderer
	dic = {
		'sentence_page_ql' : sentence_page_ql,
		'sentence_paginator': sentence_paginator,
		'quicklist': ql
	}
	
	#Render the page
	return render_to_response("sentences/list.html", dic, context_instance=RequestContext(request))

# ----------------------------- SENTENCE -------------------------------
# Shows an individual sentence.
def sentence(request, sentence_id):
	try:
		sentence = Sentence.objects.get(pk=sentence_id)
	except:
		raise Http404
	
	# Get more sentences like this.
	more = SearchQuerySet().all().more_like_this(sentence)
	
	print more.count()
	
	dic = {
		'sentence': sentence,
		'more': more,
		
	}
	
	return render_to_response("sentences/sentence.html", dic, context_instance=RequestContext(request))


def populate_choices(request, form):
	form.fields['list'].choices = []
	form.fields['list'].choices.append((0, "None"))

	for list in request.user.get_profile().editable_lists():
		form.fields['list'].choices.append((list.id, list.name))	
		
	return form

# ---------------------------- NEW SENTENCE ----------------------------
@login_required
# Makes a new Sentence
def new(request):
	if request.method == "POST":
		form = SentenceForm(request.POST)
		
		# If we don't add to this form as well, it will complain during validation
		form = populate_choices(request, form)
		
		if form.is_valid():

			id = addSentence(request, form)
			
			if u'stay' in form.data:
				empty_form = SentenceForm()
				empty_form = populate_choices(request, empty_form)
			
				dic = {'form': empty_form, 'previous_sentence': form.cleaned_data['sentence']}
				return render_to_response("sentences/new.html", dic, context_instance=RequestContext(request))
			elif u'view' in form.data:
				return HttpResponseRedirect(reverse('ankiResource.sentences.views.sentence', args=(id,)))
			else:
				return render_to_response("sentences/new.html", {'form': form})
			
		dic = {'form': form}
		return render_to_response("sentences/new.html", {'form': form})
		
	else:
		form = SentenceForm()
		
		form = populate_choices(request, form)
		
		dic = {'form': form}
		
		return render_to_response("sentences/new.html", dic, context_instance=RequestContext(request))


# --------------------------- DELETE SENTENCE --------------------------
@login_required
# Deletes a sentence
def delete(request, sentence_id):
	# First grab the sentence.
	sentence = Sentence.objects.get(pk=sentence_id)
	
	# Make a dic for the template to use.
	dic = {
	}
	
	# Only delete the sentence if the user is a superuser (admin
	# Or if the sentence is owned by them.
	if request.user == sentence.user or request.user.is_superuser == True:
		# Delete the sentence.
		sentence.delete()
		
		# Tell the template the sentence was deleted
		dic.update({'deleted': True})
		
	# Tell the template access was denied
	else:
		dic.update({'deleted': False})
	
	# Render the page
	return render_to_response("sentences/del.html", dic, context_instance=RequestContext(request))
	

