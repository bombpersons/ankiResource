from ankiResource.sentences.models import *
from ankiResource.accounts.models import Profile
from django.contrib import admin


# Display Media model in admin (linked with sentence)
class ChoiceInLineMedia(admin.TabularInline):
	model = Media
	extra = 3
	
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
		('Profile',		{'fields': ['profile']}),
	]
	
	inlines = [ChoiceInLineMedia]

admin.site.register(Sentence, SentenceAdmin)
admin.site.register(Media)
