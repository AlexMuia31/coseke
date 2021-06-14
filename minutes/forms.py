from django import forms
from .models import *
from ckeditor.fields import RichTextField


class MinutesForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(),
                            required=True, max_length=256)
    content = RichTextField()

    class Meta:
        model = Post
        fields = ('title', 'content',)
