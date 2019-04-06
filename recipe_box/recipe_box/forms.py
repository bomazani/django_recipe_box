from django import forms
from recipe_box.models import Recipe, Author, User
from django.contrib.auth import logout

class RecipeAddForm(forms.Form):
    title = forms.CharField(max_length=50)
    instructions = forms.CharField(widget=forms.Textarea)
    author = forms.ModelChoiceField(queryset=Author.objects.all())
    description = forms.CharField(max_length=50)
    time = forms.CharField(max_length=50)

class AuthorAddForm(forms.Form):
    bio = forms.CharField(widget=forms.Textarea)
    name = forms.CharField(max_length=50)
    username = forms.CharField(max_length=50)

class SignupForm(forms.Form):
    name = forms.CharField(max_length=50)
    bio = forms.CharField(widget=forms.Textarea)
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())

class RecipeEditForm(forms.Form):
    title = forms.CharField(max_length=50)
    instructions = forms.CharField(widget=forms.Textarea)
    description = forms.CharField(max_length=50)
    time = forms.CharField(max_length=50)
