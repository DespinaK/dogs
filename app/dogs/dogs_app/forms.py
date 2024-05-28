from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    location = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Post
        fields = ('title', 'content', 'image')