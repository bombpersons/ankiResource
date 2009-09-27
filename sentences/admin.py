from ankiResource.sentences.models import Sentence, List
from ankiResource.media.models import Media
from django.contrib import admin

# Display Sentence model in admin
class SentenceAdmin(admin.ModelAdmin):
	#
	list_display = ('sentence', 'pub_date', 'language')
	list_filter = ['pub_date']
	search_fields = ['sentence', 'user']
	date_hierarchy = 'pub_date'
	
	#Change the way admin displays this model
	fieldsets = [
		(None,			{'fields': ['sentence']}),
		('Date', 		{'fields': ['pub_date']}),
		(None,			{'fields': ['language']}),
		('Tags',		{'fields': ['tags']}),
		('user',		{'fields': ['user']}),
		('media',		{'fields': ['media']}),
	]
	
admin.site.register(Sentence, SentenceAdmin)
admin.site.register(List)
