from ankiResource import settings
from ankiResource import media, sentences, accounts
from ankiResource.lists.models import List
from mecab_parse import parse, print_in

import os, shutil, hashlib, re, datetime
import string

#Stores the file in the media dir. Returns the location (relative to media dir) if succesfull.
def storeFile(file, dir):
	#open the destination file
	temp = open(os.path.join(settings.MEDIA_ROOT, 'temp', file.name), "wb")
	
	#if we couldn't open the file return a blank string
	if not temp:
		return ""
	
	#now write to the file
	for chunk in file.chunks():
		temp.write(chunk)
	
	#close the file
	temp.close()
		
	#get the checksum for the file
	hash = hashlib.md5(open(os.path.join(settings.MEDIA_ROOT, 'temp', file.name), "rb").read()).hexdigest()
	
	print os.path.join(settings.MEDIA_ROOT, 'temp', file.name)
		
	#get the file extension
	ext = file.name.split(".")
	proper_filename = hash + "." + ext[len(ext) - 1]
	
	#now mv temp to proper location
	shutil.move(os.path.join(settings.MEDIA_ROOT, 'temp', file.name), 
					os.path.join(settings.MEDIA_ROOT, dir, proper_filename))
	
	#return the location of the file
	return os.path.join(dir, proper_filename)

#Adds a sentence, returns the new sentence's id
def addSentence(request, form):
	#Try to make the new sentence
	newSentence = sentences.models.Sentence(
											sentence=form.cleaned_data['sentence'], 
											pub_date=datetime.datetime.now(), 
											user=request.user,
											)
	
	newSentence.save()
	

	#Reading
	#print_in(parse(form.cleaned_data['sentence']))
	
	#If there is media, save it
	ms = []
	if 'video' in request.FILES:
		ms.append(media.models.Media(file=storeFile(request.FILES['video'], "media/video"), type="Video"))
		
	if 'sound' in request.FILES:
		ms.append(media.models.Media(file=storeFile(request.FILES['sound'], "media/sound"), type="Sound"))
		
	if 'image' in request.FILES:
		ms.append(media.models.Media(image=storeFile(request.FILES['image'], "media/images"), type="Image"))
		
	# Add the media to the sentence
	for m in ms:
		m.save()
		newSentence.media.add(m)
	
	newSentence.tags = form.cleaned_data['tags'] + string.join(parse(form.cleaned_data['sentence']))
	newSentence.translation = form.cleaned_data['translation']
		
	#Now save again
	newSentence.save()
	
	#Add to the selected list, if exists
	if form.cleaned_data['list'] != u"0":
		
		list = List.objects.get(pk=form.cleaned_data['list'])
		
		#Check if the user has permission to do this
		if request.user in list.users.all():
			
			#Add the sentence to the list
			list.sentences.add(newSentence)
			
			#Save the list
			list.save()
	
	#Return ID
	return newSentence.id
