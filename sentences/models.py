from django.db import models
from django.contrib.auth.models import User
import ankiResource
import datetime

# Create your models here.

# SENTENCE -------------------------------------------------------------
# A sentence
class Sentence(models.Model):
	# Relationships
<<<<<<< HEAD:sentences/models.py
	user = models.ForeignKey(User) #Attach sentences to users.
	media = models.ManyToManyField('media.Media', blank=True, null=True) #Media attached to this sentence
=======
	profile = models.ForeignKey(ankiResource.accounts.models.Profile) #Attach sentences to users.
	list = models.ForeignKey(List, blank=True, null=True) #Attach sentence to a list (optional)
	
	sentence = models.TextField() #the sentence
	
	#other info
	pub_date = models.DateTimeField("Date Submitted")
>>>>>>> df2473d928c9135469ff7248a554eec234b2e998:sentences/models.py
	
	# Values
	sentence = models.TextField() #The actual sentence
	pub_date = models.DateTimeField("Date Submitted") #The date and time the sentence was submitted
	language = models.CharField(max_length=30) #what language the sentence is in
	tags = models.TextField(blank=True) #tags with spaces inbetween
	
	# Custom Methods
	#Display something useful at interactive prompt...
	def __unicode__(self):
		return self.sentence


# LIST -----------------------------------------------------------------
# A list of sentences. A user can make a list of sentences for any purpose,
# a list for JLPT words, a list for a certain Drama series, etc
# A list can also be "open", which means that any user can edit / add to the list.
class List(models.Model):
	# Relationships
	user = models.ManyToManyField(User) 	  # (Optionally) attach this list to a user
									  # If this is set, only the user(s) can edit
									  # list.
	sentence = models.ManyToManyField(Sentence, blank=True, null=True) # Sentences associated with this List
	
	# Options
	open = models.BooleanField() # Whether or not the list is open.
								 # If a list is open, anyone can edit it.
