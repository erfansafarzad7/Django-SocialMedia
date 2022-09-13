from django.shortcuts import render, redirect
from django.views import View
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class HomeView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'home/index.html', {'posts': posts})


class PostDetailView(View):
    def get(self,request, post_id, post_slug):
        try:
            post = Post.objects.get(pk=post_id, slug=post_slug)
            return render(request, 'home/detail.html', {'post': post})
        except ObjectDoesNotExist:
            messages.warning(request, 'Page Not Found', 'warning')
            return redirect('home:home')


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id, user_id):
        try:
            post = Post.objects.get(pk=post_id)
            if request.user.id == post.user.id:
                post.delete()
                messages.success(request, 'Post Successfully Deleted', 'success')
            else:
                messages.error(request, 'You Can Not Delete This Message')
            user = User.objects.get(pk=user_id)
            posts = Post.objects.filter(user=user)
            return render(request, 'accounts/profile.html', {'user': user, 'posts': posts})
        except ObjectDoesNotExist:
            messages.warning(request, 'Page Not Found', 'warning')
            return redirect('home:home')
