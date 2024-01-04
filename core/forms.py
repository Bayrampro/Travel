from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Booking, Feedback
from django.utils.translation import gettext_lazy as _


class BookingForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'date', 'type': 'date'}))

    class Meta:
        model = Booking
        fields = ['date']


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label=_('Username'), widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': _('Enter your full name')}))
    email = forms.EmailField(label=_('Email address'), widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': _('Enter your email')}))
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': _('Enter your password')}))
    password2 = forms.CharField(label=_('Confirm password'), widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': _('Confirm your password')}))
    privacy = forms.BooleanField(label=_('I accept all terms and rules'), widget=forms.CheckboxInput())

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label=_('Username'), widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': _('Enter your full name')}))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': _('Enter your password')}))


class FeedbackForm(forms.ModelForm):
    user = forms.CharField(label=_('User'), widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': _('Enter your full name')}))
    email = forms.EmailField(label=_('Email'), widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': _('Enter your email')}))
    subject = forms.CharField(label=_('Message'), widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': _('Enter your subject'), 'rows': 5}))
    captcha = CaptchaField(label=_("I'm human"))

    class Meta:
        model = Feedback
        fields = ['user', 'email', 'subject']
