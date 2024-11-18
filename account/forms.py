from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import (AuthenticationForm, SetPasswordForm, PasswordResetForm, UserCreationForm)

from .models import User


class LoginForm(AuthenticationForm):

	username = forms.EmailField(widget=forms.EmailInput(
		attrs={
			'class': 'form-control',
			'placeholder': 'Email',
			'autofocus': 'autofocus'
		}
	))
	password = forms.CharField(widget=forms.PasswordInput(
		attrs={
			'class': 'form-control',
			'placeholder': 'Password',
		}
	))


class RegistrationForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('email', 'first_name', 'last_name')


	def cleaned_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError(
				'Please use another email, this is already taken or used.'
			)
		return email

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['email'].widget.attrs.update({
			'class': 'form-control',
			'placeholder': 'Email',
			'name': 'email'
		})
		self.fields['first_name'].widget.attrs.update({
			'class': 'w-100',
			'placeholder': 'First Name'
		})
		self.fields['last_name'].widget.attrs.update({
			'class': 'w-100',
			'placeholder': 'Last Name'
		})
		self.fields['password1'].widget.attrs.update({
			'class': 'form-control mb-2',
			'placeholder': 'Password'
		})
		self.fields['password2'].widget.attrs.update({
			'class': 'form-control mb-2',
			'placeholder': 'Confirm Password'
		})


class PwdResetForm(PasswordResetForm):
	email = forms.EmailField(max_length=254, widget=forms.EmailInput(
		attrs={
			'class': 'form-control',
			'placeholder': 'Email',
			'autofocus': 'autofocus'
		}
	))

	def clean_email(self):
		email = self.cleaned_data['email']
		try:
			user = User.objects.get(email=email)
		except ObjectDoesNotExist:
			raise forms.ValidationError(
				'Unfortunately we can not find that email address.'
			)
		return email


class PwdResetConfirmForm(SetPasswordForm):
	new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(
		attrs={
			'class': 'form-control',
			'placeholder': 'New Password',
			'autofocus': 'autofocus'
		}
	))
	new_password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
		attrs={
			'class': 'form-control',
			'placeholder': 'Repeat Password',
		}
	))


class ProfileEditForm(forms.ModelForm):

	email = forms.EmailField(
		label='Email', max_length=200, widget=forms.EmailInput(
			attrs={
				'class': 'form-control mb-3',
				'placeholder': 'email',
				'id': 'form-email',
				'disabled': 'true'
			}
		)
	)
	first_name = forms.CharField(
		label='First Name', min_length=4, max_length=50, widget=forms.TextInput(
			attrs={
				'class': 'form-control',
				'placeholder': 'First Name',
				'id': 'form-first-name'
			}
		)
	)
	last_name = forms.CharField(
		label='Last Name', min_length=4, max_length=50, widget=forms.TextInput(
			attrs={
				'class': 'form-control',
				'placeholder': 'Last Name',
				'id': 'form-last-name'
			}
		)
	)

	class Meta:
		model = User
		fields = ('email', 'first_name', 'last_name')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['email'].required = True
