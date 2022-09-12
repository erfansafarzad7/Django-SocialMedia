from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError



class RegisterView(View):
    form_class = UserRegisForm
    temp_name = 'accounts/register.html'

    def get(self, request):
        form = UserRegisForm()
        return render(request, self.temp_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            try:
                User.objects.create_user(cd['username'], cd['email'], cd['password1'])
                messages.success(request, 'Registered Successfully', 'success')
                return redirect('home:home')
            except IntegrityError as e:
                messages.warning(request, 'username already exist', 'warning')
                return render(request, self.temp_name, {'form': form})

        return render(request, self.temp_name, {'form': form})
