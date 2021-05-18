from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserInfo

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )
        widgets = {
            'username': forms.TextInput(
                attrs = {
                    'placeholder': 'Username'
                }
            ),
            'email': forms.EmailInput(
                attrs = {
                    'placeholder': 'Email'
                }
            ),
            'password1': forms.PasswordInput(
                attrs = {
                    'placeholder': 'Password'
                }
            )
        }
    
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'})
    

class CreateUserInfoForm(ModelForm):
    class Meta:
        model = UserInfo
        fields = (
            'user',
            'name',
            'phone',
            'profile_pic',
            'date_of_birth',
            'gender',
            'city',
            'interests',
            'bio'
        )
        widgets = {
            'user': forms.HiddenInput(),
            'name': forms.TextInput(
                attrs = {
                    'placeholder': 'Name'
                }
            ),
            'phone': forms.TextInput(
                attrs = {
                    'placeholder': 'Phone Number'
                }
            ),
            'date_of_birth': forms.DateInput(
                attrs = {
                    'placeholder': 'Date of Birth'
                }
            ),
            'city': forms.TextInput(
                attrs = {
                    'placeholder': 'City'
                }
            ),
            'interests': forms.SelectMultiple(
                attrs = {
                    'data-placeholder': 'Choose your interests',
                    'class': 'chosen-select'
                }
            ),
            'bio': forms.TextInput(
                attrs = {
                    'placeholder': 'Short bio about you'
                }
            ),
        }
