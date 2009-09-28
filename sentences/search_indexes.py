# Contains indexes for haystack
from haystack import indexes
from haystack import site
from ankiResource.sentences import models

class SentenceIndex(indexes.SearchIndex):
	text = indexes.CharField(document=True, use_template=True)
	sentence = indexes.CharField(model_attr='sentence')


site.register(models.Sentence, SentenceIndex)
