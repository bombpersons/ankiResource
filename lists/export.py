# This file contains classes that can export lists into various formats.

import settings

import tempfile, re, codecs, random, os, shutil, zipfile, copy
import anki

# LIST FILES -----------------------------------------------------------
# This function lists all the files in a directory (ignoring folders)
def listFiles(dir):
	files = []
	
	for file in os.listdir(dir):
		if os.path.isfile(os.path.join(dir,file)):
			files.append(file)
	
	return files

# LIST DIRS ------------------------------------------------------------
# This function lists all the folders in a folder (ignoring files)
def listDirs(dir):
	files = []
	
	for file in os.listdir(dir):
		if os.path.isdir(os.path.join(dir,file)):
			files.append(file)
	
	return files


# A class to store information about sentences
# E.g The sentence itself, media information etc

class Sentence:
	def __init__(self, sentence="", media=[], language=""):
		# Initiate variables
		self.sentence = sentence # Blank sentence to begin with.
		self.media = media # A list of media associated with this sentence.
		self.language = language # The language this sentence is in.


# BASE EXPORTER CLASS --------------------------------------------------
class ListExporter:
	# INIT -------------------------------------------------------------
	def __init__(self):
		# VARS
		self.sentences = [] # A list of the sentences to export.
		self.letters = [
			'a', 'b', 'c', 'd', 'e',
		]
		
	# GET RANDOM NAME
	def getRandomName(self, length):
		# Get random characters and make a string length long
		name = ""
		running = True
		while running:
			for pizza in range(length):
				name += random.choice(self.letters)
			
			# K, now check whether or not this file already exists
			if name not in listFiles(os.path.join(settings.SITE_ROOT, "tmp")) or name not in listDirs(os.path.join(settings.SITE_ROOT, "tmp")):
				running = False
		
		return os.path.join(settings.SITE_ROOT, "tmp", name)
	
	# OPEN TEMP FILE
	def openTempFile(self):
		# Get a name
		self.tempname = self.getRandomName(10)
		
		# Now open the proper file with utf-8
		file = codecs.open(self.tempname, "w+b", "utf-8")
		
		# Now return this.
		return file
	
	# READ LIST --------------------------------------------------------
	# This function takes a django List object and extracts the
	# Sentences from it.
	def readList(self, list):
		# Loop through the sentences in the list
		for sentence in list.sentence.all():
			newSentence = Sentence(sentence=sentence.sentence, language=sentence.language, media=[])
			
			for media in sentence.media.all():
				if media.type == "Image":
					newSentence.media.append(media.image.path.split("/")[-1])
				else:
					newSentence.media.append(media.file.path.split("/")[-1])
			
			# Now add the sentence to our list
			self.sentences.append(newSentence)
		
		# Let's read the name of the list for convenience later on.
		self.name = list.name
		
		# Done for now.
			
	# EXPORT -----------------------------------------------------------
	# Export the sentences to a file and return the path, so that we can
	# redirect the user to the file. (The file can be outside of the
	# the websites path, as long as the webserver has permission to read
	# the files. We can send a special header in the http request to
	# make the webserver send the file.
	def export(self):
		pass
		
	
# AS TEXT FILE
# This class exports setences into a text file, line seperated.
class TextFileListExporter(ListExporter):
	def export(self):
		# Check if we have any sentences before doing anything.
		if self.sentences:
			
			# Right now open a temporary file and write our sentences to
			# it.
			file = self.openTempFile()
			
			for sentence in self.sentences:
				file.write(sentence.sentence + "\n")
			
			# Close the file
			file.close()
			
			# Open the file again
			file = codecs.open(self.tempname, "rb+", "utf-8")
			
			# Before we exit, it would be convenient for use to make a
			# name to use for this file. (even though we can't choose
			# the name of the temporary file)
			self.filename = self.name + ".txt"
			
			# Make sure we strip any spaces
			self.filename = re.sub('\s', '', self.filename)
			
			# We should have a file now, return the file
			return file
		
		# No sentences, fail.
		else:
			return False

# AS ANKI DECK
# This class exports sentences as an anki deck (zip file with media)
class AnkiListExporter(ListExporter):
	def export(self):
		if self.sentences:
			# Make a name for the deck from the list name
			deck_name = self.name
			deck_name = re.sub('\s', '', deck_name)
			
			# First make a directory that we can work in
			tempDir = self.getRandomName(10)
			os.mkdir(tempDir)
			
			# And a directory to put media
			os.mkdir(os.path.join(tempDir, deck_name + ".media"))
			
			# Get the path to make the anki deck in.
			anki_name = os.path.join(tempDir, deck_name + ".anki")
			
			# Now make a zip file with the media and anki deck
			zip_name = os.path.join(tempDir, deck_name + ".zip")
			z = zipfile.ZipFile(zip_name, "a")
			
			# Open an anki deck with anki
			deck = anki.DeckStorage.Deck(anki_name)
			
			# Now make an ankiResource model
			model = anki.models.Model(name=u"AnkiResource")
			model.addFieldModel(anki.models.FieldModel(name=u"Expression", required=False, unique=False))
			model.addFieldModel(anki.models.FieldModel(name=u"Image", required=False, unique=False))
			model.addFieldModel(anki.models.FieldModel(name=u"Sound", required=False, unique=False))
			model.addFieldModel(anki.models.FieldModel(name=u"Video", required=False, unique=False))
			model.addFieldModel(anki.models.FieldModel(name=u"Readings", required=False, unique=False))
			
			# Now add a card model to this model
			model.addCardModel(
				anki.models.CardModel(name=u"Recognition", 
					qformat=u"%(Expression)s<br>%(Image)s",
					aformat=u"%(Video)s<br>%(Sound)s<br>%(Readings)s"))
			
			deck.addModel(model)
			
			# Now add cards
			for sentence in self.sentences:
				fact = anki.facts.Fact(model=model)
				fact['Expression'] = sentence.sentence
				
				# Find media
				for media in sentence.media:
					if media.endswith(".jpg") or media.endswith(".png") or media.endswith(".gif"):
						fact['Image'] += "<img src=\"" + media + "\" /><br>"
						shutil.copyfile(os.path.join(settings.MEDIA_ROOT, "media", "images", media), os.path.join(tempDir, deck_name + ".media", media))
						z.write(os.path.join(tempDir, deck_name + ".media", media), arcname=os.path.join(deck_name + ".media", media))
						
					elif media.endswith(".mpg") or media.endswith(".mpeg") or media.endswith(".avi") or media.endswith(".mp4") or media.endswith(".ogv") or media.endswith(".flv"):
						fact['Video'] += "[sound:" + media + "]"
						shutil.copyfile(os.path.join(settings.MEDIA_ROOT, "media", "video", media), os.path.join(tempDir, deck_name + ".media", media))
						z.write(os.path.join(tempDir, deck_name + ".media", media), arcname=os.path.join(deck_name + ".media", media))
						
					elif media.endswith(".mp3") or media.endswith(".ogg"):
						fact['Sound'] += "[sound:" + media + "]"
						shutil.copyfile(os.path.join(settings.MEDIA_ROOT, "media", "sound", media), os.path.join(tempDir, deck_name + ".media", media))
						z.write(os.path.join(tempDir, deck_name + ".media", media), arcname=os.path.join(deck_name + ".media", media))
				
				fact.setModified(textChanged=True)
				
				# Add the fact.
				deck.addFact(fact)
			
			# Save the anki deck
			deck.setModified()
			deck.save()
			deck.close()
			
			# Add the files
			z.write(anki_name, arcname=deck_name + ".anki")
			z.close()
			
			self.filename = deck_name + ".zip"
			
			return open(zip_name, "rb")
			
		else:
			
			return False
			
			
