# Contains indexes for haystack
from haystack import indexes
from haystack import site
from ankiResource.sentences import models

class SentenceIndex(indexes.SearchIndex):
	text = indexes.CharField(document=True, use_template=True)
	sentence = indexes.CharField(model_attr='sentence')
	tags = indexes.CharField(model_attr='tags')
	language = indexes.CharField(model_attr='language')
	author = indexes.CharField(model_attr='user')
	pub_date = indexes.DateTimeField(model_attr='pub_date')


site.register(models.Sentence, SentenceIndex)
