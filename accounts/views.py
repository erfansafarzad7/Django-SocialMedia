from django.shortcuts import render
from django.views import View
from .forms import UserRegisForm


class RegisterView(View):
    def get(self, request):
        form = UserRegisForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        return render(request, 'accounts/register.html')


