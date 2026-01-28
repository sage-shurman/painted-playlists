# users/forms.py

from django import forms  # Import Django's forms module
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
    """
    A form for registering new users, extending the default UserCreationForm
    to include an email field.
    """
    email = forms.EmailField(  # Add an email field to the registration form
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )

    class Meta:
        """
        Meta class to specify the model and fields to include in the form.
        """
        model = User  # Use the Django built-in User model
        fields = ['username', 'email', 'password1', 'password2']  # Fields to include in the form
        widgets = {  # Custom widgets for form fields
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),  # Username input
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),  # Password input
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),  # Confirm password input
        }
