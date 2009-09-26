from django.db import models
from django.contrib.auth.models import User
import ankiResource

# News post model. These are shown on the main index page.
class News(models.Model):
	title = models.CharField(max_length=200)
	text = models.TextField()
	pub_date = models.DateTimeField()
	
	#relationships
	user = models.ForeignKey(User)
	
	#Display something useful at a prompt
	def __unicode__(self):
		return self.text
