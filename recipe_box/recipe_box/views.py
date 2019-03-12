from django.shortcuts import render
from recipe_box.models import Author, Recipe

def index(request):
    recipes = Recipe.objects.all()
    return render(request, 'index.html', {'data':recipes})

def recipe(request, r_id):
    recipe_id = Recipe.objects.get(id=r_id)
    return render(request, 'recipe.html', {'data':recipe_id})

def author(request, a_id):
    author_recipes = Recipe.objects.filter(author=a_id)
    return render(request, 'author.html', {'data':author_recipes})