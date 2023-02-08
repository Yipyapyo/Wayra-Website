from datetime import datetime
from django import forms
from django.core.validators import RegexValidator

from portfolio.models import User

class LogInForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())