from django import forms
from .models import Comments, Forum, Post, Thread


class CreateForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = '__all__'


class CreateThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = '__all__'


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('body',)
