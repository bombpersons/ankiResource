from django.shortcuts import *
import ankiResource.sentences.models as m
from django.http import *
from django.core.urlresolvers import *

import datetime

# Create your views here.

# -----------------------------INDEX------------------------------------
def index(request):
	latest_sentences_list = m.Sentence.objects.all().order_by('-pub_date')[:5]
	
	return render_to_response("sentences/index.html", {'latest_sentences_list': latest_sentences_list})

# ----------------------------- SENTENCE -------------------------------
def sentence(request, sentence_id):
	try:
		sentence = m.Sentence.objects.get(pk=sentence_id)
	except:
		raise Http404
	
	return render_to_response("sentences/sentence.html", {'sentence': sentence})

# ---------------------------- NEW SENTENCE ----------------------------
def new(request):
	#Try to make the new sentence
	newSentence = m.Sentence(sentence=request.POST['sentence'], pub_date=datetime.datetime.now())
	newSentence.save()
	
	return HttpResponseRedirect(reverse('ankiResource.sentences.views.sentence', args=(newSentence.id,)))
		
