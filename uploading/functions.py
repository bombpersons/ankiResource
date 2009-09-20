from ankiResource import settings

import os, shutil, hashlib, re

#Stores the file in the media dir. Returns the location (relative to media dir) if succesfull.
def storeFile(file, dir):
	#open the destination file
	temp = open(os.path.join(settings.MEDIA_ROOT, 'temp', file.name), "wb+")
	
	#if we couldn't open the file return a blank string
	if not temp:
		return ""
	
	#now write to the file
	for chunk in file.chunks():
		temp.write(chunk)
	
	#get the checksum for the file
	hash =  hashlib.md5(temp.read()).hexdigest()
	
	#close the file
	temp.close()
	
	#get the file extension
	ext = file.name.split(".")
	proper_filename = hash + "." + ext[len(ext) - 1]
	
	#now mv temp to proper location
	shutil.move(os.path.join(settings.MEDIA_ROOT, 'temp', file.name), 
					os.path.join(settings.MEDIA_ROOT, dir, proper_filename))
	
	#return the location of the file
	return os.path.join(dir, proper_filename)
