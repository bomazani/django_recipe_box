from django.shortcuts import render, HttpResponseRedirect, reverse
from recipe_box.models import Author, Recipe, User
from recipe_box.forms import RecipeAddForm, AuthorAddForm
from recipe_box.forms import SignupForm, LoginForm
from recipe_box.forms import AddFavoriteForm, RemoveFavoriteForm
from recipe_box.helpers import add_favorite, remove_favorite
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


def index(request):
    recipes = Recipe.objects.all()
    return render(request, 'index.html', {'data':recipes})

def recipe(request, r_id):
    # recipe_id = Recipe.objects.get(id=r_id)
    recipe = Recipe.objects.filter(id=r_id).first()
    current_user = request.user
    current_recipe = Recipe.objects.get(id=r_id)
    # *** need to determine whether to pass through favorite or unfavorite
    # *** depending on whether the current recipe is or is not currently in "favorites"
    current_favorites = request.user.author.favorites.all()
    favorite = False
    unfavorite = False
    if recipe in current_favorites:
        favorite = True
        unfavorite = False
    else:
        favorite = False
        unfavorite = True
    data = {
        'current_user': current_user,
        'current_recipe': current_recipe,
        'current_favorites': current_favorites,
        'favorite':favorite,
        'unfavorite':unfavorite,
    }
    
    return render(request, 'recipe.html', data)

def author(request, a_id):
    author_recipes = Recipe.objects.filter(author=a_id)
    return render(request, 'author.html', {'data':author_recipes})

@login_required()
def recipeadd(request):
    html = 'recipeadd.html'
    form = None

    if request.method == "POST":
        form = RecipeAddForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            Recipe.objects.create(
                title=data['title'],
                description=data['description'],
                time=data['time'],
                instructions=data['instructions'],
                author=data['author']
            )
            return render(request, 'thanks.html')
    else:
        form = RecipeAddForm

    return render(request, html, {'form': form})

@staff_member_required()
def authoradd(request):
    html = 'authoradd.html'
    form = None

    if request.method == "POST":
        form = AuthorAddForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                username = data['username']
            )
            Author.objects.create(
                bio=data['bio'],
                user=user,
                name=data['name']
            )
            return render(request, 'thanks.html')
    else:
        form = AuthorAddForm

    return render(request, html, {'form': form})

def signup_view(request):
    html = 'signup.html'
    form = None

    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                data['username'], data['password'])
            login(request, user)
            Author.objects.create(
                bio=data['bio'],
                user=user,
                name=data['name']
            )
            return HttpResponseRedirect(reverse('homepage'))
    else:
        form = SignupForm()

    return render(request, html, {'form': form})

    
def login_view(request):
    html = 'signup.html'
    form = None

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', '/'))
    else:
        form = LoginForm()
    return render(request, html, {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def add_favorite_view(request, recipe_id):
    recipe = Recipe.objects.filter(id=recipe_id).first()
    html = 'recipe.html'
    add_favorite(request, recipe)
    data = {
        'current_user': request.user.author,
        'current_recipe': recipe,
        'unfavorite': True
    }
    return render(request, html, data)

def remove_favorite_view(request, recipe_id):
    recipes = Recipe.objects.filter(id=recipe_id).first()
    html = 'recipe.html'
    remove_favorite(request, recipe)
    data = {
        'current_user': request.user.author,
        'current_recipe': recipe,
        'favorite': True
    }
    return render(request, html, data)
     