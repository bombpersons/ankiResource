from django.db import models
from django.contrib.auth.models import User

from ankiResource.sentences.models import List

# User Profile
class Profile(models.Model):
	# Relationships
	user = models.ForeignKey(User)
	quick_list = models.ForeignKey("sentences.List", blank=True, null=True) 
											   # A personal list just for the user.
											   # Used as a list for downloading sentences,
											   # if a list isn't specified.
	
	#Make something useful display at admin
	def __unicode__(self):
		return self.user.username
		
	#Custom save method to make sure a list object is made
	def save(self):
		# Make a list if it doesn't already exist.
		if not self.quick_list:
			newList = List(open=False, name= str(self.user.username) + "'s quicklist")
			newList.save()
			
			newList.user.add(self.user)
			
			self.quick_list = newList
			
			newList.save()

		# Call the normal save
		super(Profile, self).save()
	
	def editable_lists(self):
		#returns lists that the user can edit
		return List.objects.filter(user=self.user)
