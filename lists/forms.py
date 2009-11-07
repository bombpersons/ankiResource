from django import forms

class QuicklistForm(forms.Form):
	name = forms.CharField()
	clear = forms.BooleanField(required=False)

#--------------------------ListForm -----------------------------------
class ListForm(forms.Form):
	name = forms.CharField()
	open = forms.BooleanField(required=False) # Whether or not the list is open.
