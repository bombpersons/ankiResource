from django.conf.urls.defaults import *
from tagging.views import tagged_object_list
from ankiResource.sentences.models import Sentence, SentenceWords

urlpatterns = patterns('',
	#sentence index
	url(r'^$', 'ankiResource.sentences.views.index', name="url_sentences_index"),
	
	#show sentences as a list
	url(r'^all/$', 'ankiResource.sentences.views.list', name="url_sentences_list"),

	#show all sentences containing tag
	url(r'^tag/(?P<tag>[^/]+)/$', 'tagging.views.tagged_object_list', dict(queryset_or_model=Sentence), name="url_sentences_tags"),
	
	#show all sentences containing word
	url(r'^word/(?P<tag>[^/]+)/$', 'tagging.views.tagged_object_list', dict(queryset_or_model=SentenceWords), name="url_sentences_words"),
	
	#shows a specific sentence
	url(r'^(?P<sentence_id>\d+)$', 'ankiResource.sentences.views.sentence', name="url_sentences_sentence"),
	
	#makes a new sentence
	url(r'^new/$', 'ankiResource.sentences.views.new', name="url_sentences_new"),
		
	#deletes a sentence
	url(r'^delete/(?P<sentence_id>\d+)$', 'ankiResource.sentences.views.delete', name="url_sentences_delete"),
	
)

