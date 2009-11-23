from django.db import models
from django.contrib.auth.models import User
import ankiResource
import datetime
from tagging.fields import TagField
from tagging.models import Tag

def truncate(s, l):
	if len(s) < l:
		return s
	else:
		words = s[:l+1].split(' ')
		if len(words) == 1:
			return words[0][:l+1] + '...'
		return ' '.join(words[0:-1]) + '...'

# Create your models here.

class SentenceWords(models.Model):
	mecab_words = TagField()

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
	tags = TagField()
	words = models.ForeignKey(SentenceWords)
	
	# Custom Methods
	#Display something useful at interactive prompt...
	def __unicode__(self):
		return "<sentence> "+ self.sentence
		
	def short_form(self):
		return truncate(self.sentence, 50)

	def get_tags(self):
		return Tag.objects.get_for_object(self) 
		
	def has_tags(self):
		return len(self.get_tags()) != 0
		
	def get_words(self):
		return Tag.objects.get_for_object(self.words)
		
	def has_words(self):
		return len(self.get_words()) != 0
		

		

# LIST -----------------------------------------------------------------
# A list of sentences. A user can make a list of sentences for any purpose,
# a list for JLPT words, a list for a certain Drama series, etc
# A list can also be "open", which means that any user can edit / add to the list.
class ooList(models.Model):
	# Relationships
	user = models.ManyToManyField(User) 	  # (Optionally) attach this list to a user
									  # If this is set, only the user(s) can edit
									  # list.
	sentence = models.ManyToManyField(Sentence, blank=True, null=True) # Sentences associated with this List
	
	# Options
	open = models.BooleanField() # Whether or not the list is open.
								 # If a list is open, anyone can edit it.
								 
	name = models.CharField(max_length=200, blank=True) # Name of the list (optional)
	
	def number_of_sentences(self):
		return len(self.sentence.all())
		
	def __unicode__(self):
		return self.name
