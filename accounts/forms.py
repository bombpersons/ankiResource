from django import forms

#------------------------- LOGIN FORM ----------------------------------
class LoginForm(forms.Form):
	username = forms.CharField(max_length=100, label="Username", error_messages={'required': 'Please enter a username!'})
	password = forms.CharField(max_length=100, label="Password", error_messages={'required': 'Please enter a password!'}, widget=forms.PasswordInput)
