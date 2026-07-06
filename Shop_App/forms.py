from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *

class CustomUserCreationForm(UserCreationForm):
    # Field definitions with precise clean CSS classes
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@domain.com'}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. +123456789'}))
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'role')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter unique username'}),
            'role': forms.Select(attrs={'class': 'form-select'}), # Corrected to Bootstrap 5 form-select
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Explicitly style the internal security fields inherited from UserCreationForm
        if 'password1' in self.fields:
            self.fields['password1'].widget = forms.PasswordInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter secure password'
            })
            self.fields['password1'].help_text = "" # Clears long Django text blocks safely
            self.fields['password1'].label = "Password"
            
        if 'password2' in self.fields:
            self.fields['password2'].widget = forms.PasswordInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Repeat password'
            })
            self.fields['password2'].help_text = ""
            self.fields['password2'].label = "Confirm Password"

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Password'
    }))