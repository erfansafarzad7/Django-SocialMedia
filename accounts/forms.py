from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import render


class UserRegisForm(forms.Form):
    username = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                'placeholder': 'Max: 20 char'}))
    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('This Email Already Exist')
        return email

    # def clean_username(self):
    #     username = self.cleaned_data['username']
        # user = User.objects.filter(username=username).exists()
        # if user:
        #     raise IntegrityError('Exist')
        # return username
        # from django.db import IntegrityError
        # from django.shortcuts import render_to_response

        # try:
        #     User.objects.create_user(username=username)
        # except IntegrityError as e:
        #     return render("message.html", {"message": e.__cause__})