from django import forms

class QuicklistForm(forms.Form):
	name = forms.CharField()
	clear = forms.BooleanField(required=False)
