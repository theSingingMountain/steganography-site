from xml.dom import ValidationErr
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.core.validators import FileExtensionValidator

# Create your forms here.

class NewUserForm(UserCreationForm):
	username = forms.CharField(
		max_length = 100,
		required = True,
		help_text = 'Username',
		widget = forms.TextInput(
			attrs = {
				'class':'form-control',
				'placeholder':'Username'
			}
		),
	)

	password1 = forms.Field(
		required=True, 
		help_text = 'Password',
		widget = forms.PasswordInput(
			attrs={
				'class':'form-control', 
				'placeholder':'Password'
			}
		),
	)

	password2 = forms.CharField(
		required=True, 
		help_text = 'Password Confirmation',
		widget = forms.PasswordInput(
			attrs={
				'class':'form-control', 
				'placeholder':'Password Check'
			}
		),
	)
	class Meta:
		model = User
		fields = [
			'username','password1','password2'
		]


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(
		required = True, 
		help_text = 'Username', 
		widget=forms.TextInput(
			attrs={
				'class': 'form-control', 
				'placeholder': 'Username'
			}
		)
	)

    password = forms.CharField(		
		required = True, 
		help_text = 'Username', 
		widget=forms.PasswordInput(
			attrs={
            'class': 'form-control',
            'placeholder': 'Password',
    	    }
		)
	)

class UploadFileForm(forms.Form):
	file = forms.FileField(
		label='Select a file', 		
		required = True,
		widget=forms.FileInput(
			attrs={
            'class': 'form-control',
    	    }
		),
		validators=[FileExtensionValidator(allowed_extensions=['png', 'tif', 'tiff', 'bmp'])]
	)

	message = forms.CharField(
		label='Message to Embed Onto The File',
		required = True,
		max_length=150,
		widget = forms.TextInput(
			attrs={
				'class':'form-control',
				'placeholder': 'Message',
			}
		)
	)

