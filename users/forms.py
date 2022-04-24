from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm): # register form that inherits from creation form
    email= forms.EmailField()

    class Meta: #nested namespace for configurations
        model= User
        fields= ['username', 'email', 'password1', 'password2']
    
#user update form
class UserUpdateForm(forms.ModelForm):
    email= forms.EmailField()

    class Meta:
        model= User
        fields= ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model= Profile
        fields= ['image']