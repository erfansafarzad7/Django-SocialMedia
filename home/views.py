from django.shortcuts import render, redirect
from django.views import View
from .models import Post, Comments, Vote
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .forms import PostCreateUpdateForm, CommentCreateForm, CommentReplyForm, PostSearchForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class HomeView(View):
    form_class = PostSearchForm

    def get(self, request):
        posts = Post.objects.all()
        if request.GET.get('search'):
            posts = posts.filter(body__icontains=request.GET['search'])
        return render(request, 'home/index.html', {'posts': posts, 'form': self.form_class})


class PostDetailView(View):
    form_class = CommentCreateForm
    form_class_reply = CommentReplyForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(pk=kwargs['post_id'], slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)

    def get(self,request, *args, **kwargs):
        try:
            comments = self.post_instance.pcomments.filter(is_reply=False)
            # can_like = False
            # if request.user.is_authenticated and self.post_instance.user_can_like(request.user):
            #     can_like = True
            return render(request, 'home/detail.html', {'post': self.post_instance,
                                                        'comments': comments,
                                                        'form': self.form_class,
                                                        'reply_form': self.form_class_reply, })
                                                        # 'can_like': can_like
        except ObjectDoesNotExist:
            messages.warning(request, 'Page Not Found', 'warning')
            return redirect('home:home')

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request, 'Your Comment Submited Successfully!', 'success')
            return redirect('home:post_detail', self.post_instance.id, self.post_instance.slug)


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id, user_id):
        try:
            post = Post.objects.get(pk=post_id)
            if request.user.id == post.user.id:
                post.delete()
                messages.success(request, 'Post Successfully Deleted', 'success')
            else:
                messages.error(request, 'You Can Not Delete This Message', 'danger')
            # user = User.objects.get(pk=user_id)
            # posts = Post.objects.filter(user=user)
            # return render(request, 'accounts/profile.html', {'user': user, 'posts': posts})
            return redirect('accounts:user_profile', post.user.id)
        except ObjectDoesNotExist:
            messages.warning(request, 'Page Not Found', 'warning')
            return redirect('home:home')


class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm

    def setup(self, request, *args, **kwargs):
        try:
            self.post_instance = Post.objects.get(pk=kwargs['post_id'])
        except ObjectDoesNotExist:
            messages.error(request, 'You Can Not Delete This Message', 'danger')
            return redirect('accounts:user_profile', request.user.id)
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if post.user.id != request.user.id:
            messages.error(request, 'You Cant Edit This Message', 'danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, 'home/update.html', {'form': form})

    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request, 'Your Post Updated', 'success')
            return redirect('home:post_detail', post.id, post.slug)


class PostCreateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, 'home/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'Your Post Created', 'success')
            return redirect('home:post_detail', new_post.id, new_post.slug)


class PostAddReplyView(LoginRequiredMixin, View):
    form_class = CommentReplyForm

    def post(self, request, post_id, comment_id):
        post = Post.objects.get(id=post_id)
        comment = Comments.objects.get(id=comment_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(request, 'Your Comment Submited Successfully!', 'success')
        return redirect('home:post_detail', post.id, post.slug)


class PostLikeView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        like = Vote.objects.filter(post=post, user=request.user)
        if like.exists():
            like.delete()
            messages.warning(request, 'You Unliked This Post!', 'warning')
            # messages.error(request, 'You Have Already Like This Post!', 'danger')
        else:
            Vote.objects.create(post=post, user=request.user)
            messages.success(request, 'You Liked This Post!', 'success')
        return redirect('home:post_detail', post.id, post.slug)


