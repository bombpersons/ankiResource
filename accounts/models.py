from django.db import models
from django.contrib.auth.models import User

from ankiResource.sentences.models import List

# User Profile
class Profile(models.Model):
	# Relationships
	user = models.ForeignKey(User)
	list = models.ForeignKey("sentences.List", blank=True, null=True) 
											   # A personal list just for the user.
											   # Used as a list for downloading sentences,
											   # if a list isn't specified.
	
	#Make something useful display at admin
	def __unicode__(self):
		return self.user.username
		
	#Custom save method to make sure a list object is made
	def save(self):
		# Make a list if it doesn't already exist.
		if not self.list:
			newList = List(open=False)
			newList.save()
			
			newList.user.add(self.user)
			
			self.list = newList
			
			newList.save()

		# Call the normal save
		super(Profile, self).save()

