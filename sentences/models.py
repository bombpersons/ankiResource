from django.db import models
from django.contrib.auth.models import User
import ankiResource
import datetime
from tagging.fields import TagField
from tagging.models import Tag
from haystack.query import SearchQuerySet

def truncate(s, l):
	if len(s) < l:
		return s
	else:
		return s[0:l] + '...'

# Create your models here.

class SentenceWords(models.Model):
	mecab_words = TagField()
	
class SentenceTags(models.Model):
	sentence_tags = TagField()

# SENTENCE -------------------------------------------------------------
# A sentence
class Sentence(models.Model):
	# Relationships
	user = models.ForeignKey(User)
	media = models.ManyToManyField('media.Media', blank=True, null=True) #Media attached to this sentence
	
	# Values
	sentence = models.TextField()
	translation = models.TextField()
	pub_date = models.DateTimeField("Date Submitted") #The date and time the sentence was submitted
	
	#tags
	tags = models.ForeignKey(SentenceTags)
	words = models.ForeignKey(SentenceWords)
	
	# Custom Methods
	#Display something useful at interactive prompt...
	def __unicode__(self):
		return "<sentence> "+ self.sentence
		
	def short_form(self):
		return truncate(self.sentence, 25)

	def get_tags(self):
		return Tag.objects.get_for_object(self.tags) 
		
	def has_tags(self):
		return len(self.get_tags()) != 0
		
	def get_words(self):
		return Tag.objects.get_for_object(self.words)
		
	def has_words(self):
		return len(self.get_words()) != 0
		
	def has_more(self):
		return self.more_like_this != []
	
	def more_like_this(self):
		print SearchQuerySet().all().more_like_this(self)
		return [s.object for s in SearchQuerySet().more_like_this(self) if s.object != None]
		
		
		
