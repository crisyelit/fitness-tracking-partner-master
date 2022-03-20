from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.validators import RegexValidator
from django.forms import widgets
from django.forms.widgets import PasswordInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit





class SignUpForm(UserCreationForm):
	class Meta:
		model = get_user_model()
		fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')

		widgets = {

			'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Nombre de usuario'}),
			'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':' Nombre'}),
			'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Apellido'}),
			'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'Correo electrónico'}),
			'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Contraseña'}),
			'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Confirmar contraseña'}),
			
			}
		
 
class UserUpdateForm(UserChangeForm):
	password = None
	phone = forms.CharField(label='Número de teléfono',validators=[RegexValidator(regex='^\+\d{1,4}\d{10}$')], widget=forms.TextInput(attrs={'placeholder': '+00000000000'}))
	image = forms.ImageField(label='Imagen', widget=forms.FileInput(attrs={'class': 'image-upload'}))
	

	class Meta:
		model = get_user_model()
		fields = ['first_name', 'last_name', 'image', 'birth_day',  'phone','weight', 'height', 'short_description' ]
		labels = {
			"last_name": "Apellido",
			'image': 'Imagen', 
			'birth_day': 'Fecha de nacimiento', 
			"short_description": 'Descripción',
			'weight' : 'Peso',
			'height': 'Altura', 
		}

		widgets = {
        	'birth_day': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
    	}
		
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()

		self.helper.add_input(Submit('submit', 'Guardar'))
