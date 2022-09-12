from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserRegisForm(forms.Form):
    username = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='password', max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                'placeholder': 'Max: 20 char'}))
    password2 = forms.CharField(label='Confirm Password', max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                'placeholder': 'Max: 20 char'}))
    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('This Email Already Exist')
        return email

    def clean(self):
        cd = super().clean()
        p1 = cd.get('password1')
        p2 = cd.get('password2')

        if p1 and p2 and p1 != p2:
            raise ValidationError('Passwords Most Match')


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                'placeholder': 'Max: 20 char'}))

