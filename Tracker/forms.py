from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class ProfileForm(forms.ModelForm):
    class Meta:
        model= Profile
        fields = '__all__'
        exclude=['user']

class CreateUserform(UserCreationForm):
    first_name=forms.CharField(required=True)
    last_name=forms.CharField(required=True)
    email=forms.EmailField(required=True)
    class Meta:
        model= User
        fields=['username','first_name','last_name','email','password1','password2']