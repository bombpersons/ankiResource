from django.db import models
from django.contrib.auth.models import User

# User Profile
class Profile(models.Model):
	#Link this to a username
	user = models.ForeignKey(User)
	
	#Make something useful display at admin
	def __unicode__(self):
		return self.user.username
