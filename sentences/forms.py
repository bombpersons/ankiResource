# -*- coding: utf-8 -*-
from django import forms

#------------------------- SentenceForm --------------------------------
class SentenceForm(forms.Form):
	sentence = forms.CharField()
	language = forms.ChoiceField(choices=(
		('English', 'English'),
		('日本語', '日本語'),
		('Other', 'Other')
	)
	)
	
	other_language = forms.CharField(required=False)
	
	tags = forms.CharField(required=False)
	
	video = forms.FileField(required=False)
	sound = forms.FileField(required=False)
	image = forms.ImageField(required=False)
