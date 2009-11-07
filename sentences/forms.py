# -*- coding: utf-8 -*-
from django import forms
import tagging

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
	
	tags = tagging.forms.TagField(required=False)
	
	video = forms.FileField(required=False)
	sound = forms.FileField(required=False)
	image = forms.ImageField(required=False)
	
	list = forms.ChoiceField()
