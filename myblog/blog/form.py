from django import forms
from .models import Comments, Post
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text_comments', )


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'description', 'date', 'img')

