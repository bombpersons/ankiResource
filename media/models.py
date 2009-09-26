from django.db import models

# MEDIA ----------------------------------------------------------------
# Contains information about a media. File location, type, etc
class Media(models.Model):
	file = models.FileField(upload_to="media", blank=True) #the location of the file
	image = models.ImageField(upload_to="media", blank=True) #the location of the image (if it is an image)
	
	TYPE_CHOICES = (
		('Sound', 'Sound'),
		('Image', 'Image'),
		('Video', 'Video'),
	)
	
	#type of Media
	type = models.CharField(max_length=10, choices=TYPE_CHOICES)
	
	# Display something useful at a shell:
	def __unicode__(self):
		if self.type == "Sound" or self.type == "Video":
			return self.file.name
		else:
			return self.image.name
