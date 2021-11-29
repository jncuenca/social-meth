from django import forms
from django.db.models import fields
from .models import Post, Comment

class PostModelForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':2}))
    class Meta:
        model = Post
        fields = ['content', 'image']

class CommentModelForm(forms.ModelForm):
    body = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder':'Comment something...'}))
    class Meta:
        model = Comment
        fields = ['body']