from django import forms
from recipe_box.models import Recipe, Author, User

class RecipeAddForm(forms.Form):
    title = forms.CharField(max_length=50)
    instructions = forms.CharField(widget=forms.Textarea)
    author = forms.ModelChoiceField(queryset=Author.objects.all())
    description = forms.CharField(max_length=50)
    time = forms.CharField(max_length=50)

    # title = models.CharField(max_length=50)
    # author = models.ForeignKey(Author, on_delete=models.CASCADE)
    # description = models.CharField(max_length=50)
    # time = models.CharField(max_length=50)
    # instructions = models.TextField()

class AuthorAddForm(forms.Form):
    bio = forms.CharField(widget=forms.Textarea)
    name = forms.CharField(max_length=50)
    username = forms.CharField(max_length=50)
    # author = forms.ModelChoiceField(queryset=User.objects.all())


    # bio = models.TextField()
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    # name = models.CharField(max_length=50)