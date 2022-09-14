from django import forms
from .models import Post, Comments


class PostCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body', )


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('body', )
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'})
        }