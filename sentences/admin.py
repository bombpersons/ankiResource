from ankiResource.sentences.models import *
from django.contrib import admin


# Display Media model in admin (linked with sentence)
class ChoiceInLine(admin.TabularInline):
	model = Media
	extra = 3


# Display Sentence model in admin
class SentenceAdmin(admin.ModelAdmin):
	#
	list_display = ('sentence', 'pub_date')
	list_filter = ['pub_date']
	search_fields = ['sentence']
	date_hierarchy = 'pub_date'
	
	#Change the way admin displays this model
	fieldsets = [
		(None,			{'fields': ['sentence']}),
		('Date', 		{'fields': ['pub_date']}),
	]
	
	inlines = [ChoiceInLine]

admin.site.register(Sentence, SentenceAdmin)
