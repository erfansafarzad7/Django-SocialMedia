from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisForm, UserLoginForm, EditProfileForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_view
from .models import Relation


class UserRegisterView(View):
    form_class = UserRegisForm
    temp_name = 'accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = UserRegisForm()
        return render(request, self.temp_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            try:
                User.objects.create_user(cd['username'], cd['email'], cd['password1'])
                messages.success(request, 'Registered Successfully !', 'success')
                return redirect('accounts:user_login')
            except IntegrityError as e:
                messages.warning(request, 'Username Already Exist !', 'warning')
                return render(request, self.temp_name, {'form': form})

        return render(request, self.temp_name, {'form': form})


class UserLoginView(View):
    form_class = UserLoginForm
    temp_name = 'accounts/login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        super().setup(self, request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.temp_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user:
                login(request, user)
                messages.success(request, 'Logged in Successfully !', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            messages.warning(request, 'Username OR Password IS Wrong', 'warning')
        return render(request, self.temp_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Logged out Successfully', 'success')
        return redirect('home:home')


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        is_following = False
        user = User.objects.get(pk=user_id)
        posts = user.posts.all()
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            is_following = True
        return render(request, 'accounts/profile.html', {'user': user, 'posts': posts, 'is_following': is_following})


class UserPasswordResetView(auth_view.PasswordResetView):
    template_name = 'accounts/email/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_send')
    email_template_name = 'accounts/email/password_reset_email.html'


class UserPasswordResetSendView(auth_view.PasswordResetDoneView):
    template_name = 'accounts/email/password_reset_send.html'


class UserPasswordResetConfirmView(auth_view.PasswordResetConfirmView):
    template_name = 'accounts/email/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class UserPasswordResetCompeleteView(auth_view.PasswordResetCompleteView):
    template_name = 'accounts/email/password_reset_complete.html'


class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            messages.warning(request, 'You Already Following This User', 'warning')
        else:
            Relation(from_user=request.user, to_user=user).save()
            messages.success(request, 'You Followed This User', 'success')
        return redirect('accounts:user_profile', user.id)


class UserUnFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            relation.delete()
            messages.warning(request, 'You UnFollowed This User', 'warning')
        else:
            messages.warning(request, "You are Not Following This User", 'warning')
        return redirect('accounts:user_profile', user.id)


class EditUserProfileView(LoginRequiredMixin, View):
    form_class = EditProfileForm

    def get(self, request):
        form = self.form_class(instance=request.user.profile, initial={'email': request.user.email})
        return render(request, 'accounts/edit_profile.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request, 'Profile Successfully Edited', 'success')
        return redirect('accounts:user_profile', request.user.id)




