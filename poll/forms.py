from django import forms
from django.contrib.auth.models import User
from .models import Comment


class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(
        max_length=100, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput,
        }


class ChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['body'].widget.attrs['placeholder'] = 'Write a comment here...'
        self.fields['body'].label = "Kindly Comment Below..."

    class Meta:
        model = Comment
        fields = ['body']
