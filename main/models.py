from django.db import models
import ankiResource

# News post model. These are shown on the main index page.
class News(models.Model):
	title = models.CharField(max_length=200)
	text = models.TextField()
	pub_date = models.DateTimeField()
	
	#relationships
	profile = models.ForeignKey(ankiResource.accounts.models.Profile)
	
	#Display something useful at a prompt
	def __unicode__(self):
		return self.text
