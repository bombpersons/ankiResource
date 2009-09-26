from django.db import models
from django.contrib.auth.models import User
import ankiResource
import datetime
from tagging.fields import TagField
from tagging.models import Tag


# Create your models here.

class List(models.Model):
	# Relationships
	profile = models.ForeignKey(ankiResource.accounts.models.Profile) # (Optionally) attach this list to a user
																	  # If this is set, only the user(s) can edit
																	  # list.
	
	# Options
	open = models.BooleanField() # Whether or not the list is open.
								 # If a list is open, anyone can edit it.

# Sentence
class Sentence(models.Model):
	# Relationships
	profile = models.ForeignKey(ankiResource.accounts.models.Profile) #Attach sentences to users.
	list = models.ForeignKey(List, blank=True, null=True) #Attach sentence to a list (optional)
	
	sentence = models.TextField() #the sentence
	
	#other info
	pub_date = models.DateTimeField("Date Submitted")
	
	#language
	language = models.CharField(max_length=30) #what language the sentence is in
	
	#tags
	tags = TagField()
	
	#Display something useful at interactive prompt...
	def __unicode__(self):
		return self.sentence

	def get_tags(self):
		return Tag.objects.get_for_object(self) 


# Media
class Media(models.Model):
	file = models.FileField(upload_to="Sentences", blank=True) #the location of the file
	image = models.ImageField(upload_to="Sentences", blank=True) #the location of the image (if it is an image)
	
	TYPE_CHOICES = (
		('Sound', 'Sound'),
		('Image', 'Image'),
		('Video', 'Video'),
	)
	
	#type of Media
	type = models.CharField(max_length=10, choices=TYPE_CHOICES)
			
	#Relationships
	sentence = models.ForeignKey(Sentence)
