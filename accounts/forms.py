from django import forms


class UserRegisForm(forms.Form):
    username = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                'placeholder': 'Max: 20 char'}))

