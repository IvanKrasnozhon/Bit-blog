from dataclasses import field
from multiprocessing import AuthenticationError
from django import forms
from .models import Post, Profile, Comment
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class AddPostForm(forms.ModelForm):
    post_info = forms.CharField(label='Description', widget=forms.TextInput(attrs={'class': 'form-input post-info'}))
    class Meta:
        model = Post
        fields = ['post_img', 'post_info']
        widgets = {
            'post_img': forms.FileInput(attrs={'class': 'form-img'}),
        }

class AddCommentForm(forms.ModelForm):
    comment_info = forms.CharField(label='Comment', widget=forms.TextInput(attrs={'class': 'form-input post-info'}))
    class Meta:
        model = Comment
        fields = ['comment_info']

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user_img']
        widgets = {
            'user_img': forms.FileInput(attrs={'class': 'form-img'})
        }

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input login'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-label'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input p1'}))
    password2 = forms.CharField(label='Password repeating', widget=forms.PasswordInput(attrs={'class': 'form-input p2'}))
    class Meta:
        model = User
        fields = ('username', 'email','password1', 'password2')

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label = 'Login', widget=forms.TextInput(attrs={'class': 'form-label'}))
    password = forms.CharField(label = 'Password', widget=forms.PasswordInput(attrs={'class': 'form-label'}))

