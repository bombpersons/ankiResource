from ankiResource import settings

import os

#Stores the file in the media dir. Returns the location (relative to media dir) if succesfull.
def storeFile(file, dir):
	#open the destination file
	dest = open(os.path.join(settings.MEDIA_ROOT, dir, file.name), "wb+")
	
	#if we couldn't open the file return a blank string
	if not dest:
		return ""
	
	#now write to the file
	for chunk in file.chunks():
		dest.write(chunk)
		
	#close the file
	dest.close()
	
	#return the location of the file
	return os.path.join(dir, file.name)
