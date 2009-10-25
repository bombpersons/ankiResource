from django.db import models
from django.contrib.auth.models import User
import ankiResource
import datetime
from tagging.fields import TagField
from tagging.models import Tag
from ankiResource.sentences.models import Sentence

class List(models.Model):
	# Relationships
	user = models.ManyToManyField(User) # (Optionally) attach this list to a user
									    # If this is set, only the user(s) can edit
									    # list.
	sentence = models.ManyToManyField(Sentence, blank=True, null=True) # Sentences associated with this List
	
	# Options
	open = models.BooleanField() # Whether or not the list is open.
								 # If a list is open, anyone can edit it.
								 
	name = models.CharField(max_length=200, blank=True) # Name of the list (optional)
	
	def contains_sentence(self, sentence):
		return sentence in self.sentence.all()
	
	def number_of_sentences(self):
		return len(self.sentence.all())
		
	def name_nos(self):
		return self.name + " (%s)" % self.number_of_sentences()
	
	def __unicode__(self):
		return self.name
