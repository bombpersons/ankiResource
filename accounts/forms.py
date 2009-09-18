from django import forms

#------------------------- LOGIN FORM ----------------------------------
class LoginForm(forms.Form):
	username = forms.CharField(max_length=100, label="Username", error_messages={'required': 'Please enter a username!'})
	password = forms.CharField(max_length=100, label="Password", error_messages={'required': 'Please enter a password!'}, widget=forms.PasswordInput)

#------------------------- REGISTER FORM -------------------------------
class RegisterForm(forms.Form):
	username = forms.CharField(max_length=100, label="Desired username", error_messages={
						'required': 'Please enter a username',
	} )
	
	password = forms.CharField(max_length=100, label="Password",
						widget=forms.PasswordInput,
						error_messages={
							'required': 'Please enter a password',
						}
	)

	password_confirm = forms.CharField(max_length=100, label="Confirm Password",
						widget=forms.PasswordInput,
						error_messages={
							'required': 'Please confirm your password',
						}
	)
	
	email = forms.EmailField(label="E-mail address", error_messages={
						'required': 'Please enter an E-mail address',
	} )
	
