from django.shortcuts import render, HttpResponseRedirect, reverse, redirect, get_object_or_404
from recipe_box.models import Author, Recipe, User
from recipe_box.forms import RecipeAddForm, AuthorAddForm, RecipeEditForm
from recipe_box.forms import SignupForm, LoginForm
from recipe_box.helpers import add_favorite, remove_favorite
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse

def index(request):
    recipes = Recipe.objects.all()
    return render(request, 'index.html', {'data':recipes})


def recipe(request, r_id):
    recipe = Recipe.objects.filter(id=r_id).first()
    current_user = request.user
    current_recipe = Recipe.objects.get(id=r_id)
    r_id = current_recipe.id

    if current_user.is_authenticated:
        current_user_name = request.user.author.name
        current_favorites = request.user.author.favorite.all()
        if recipe in current_favorites:
            favorite = False
            unfavorite = True
        else:
            favorite = True
            unfavorite = False

        if (str(current_user_name) == str(current_recipe.author)):
            match = True
        elif current_user.is_superuser:
            match = True
        else:
            match = False

        data = {
            'current_user': current_user,
            'current_user_name': current_user_name,
            'current_recipe': current_recipe,
            'r_id': r_id,
            'current_favorites': current_favorites,
            'favorite': favorite,
            'unfavorite': unfavorite,
            'match': match,
        }

    else:
        match = False
        data = {
            'current_user': current_user,
            'current_recipe': current_recipe,
            'r_id': r_id,
            'match': match,
        }
    
    return render(request, 'recipe.html', data)


def author(request, a_id):
    current_user = request.user
    recipes = Recipe.objects.filter(author=a_id)
    author = Author.objects.get(id=a_id)
    selected_author = Author.objects.get(id=a_id)
    selected_author_favorites = selected_author.favorite.all()

    if current_user.is_authenticated:
        current_user_favorites = request.user.author.favorite.all()
        context = {
            'recipes':recipes,
            'author':author,
            'current_user_favorites':current_user_favorites,
            'selected_author_favorites': selected_author_favorites
        }
    else:
        context = {
            'recipes':recipes,
            'author':author,
            'selected_author_favorites': selected_author_favorites
        }
        
    return render(request, 'author.html', context)


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
        form = RecipeAddForm()

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


def add_favorite_view(request, r_id):
    recipe = Recipe.objects.filter(id=r_id).first()
    html = 'recipe.html'
    add_favorite(request, recipe)
    return HttpResponseRedirect(reverse('recipedetail', kwargs={'r_id': r_id}))


def remove_favorite_view(request, r_id):
    recipe = Recipe.objects.filter(id=r_id).first()
    html = 'recipe.html'
    remove_favorite(request, recipe)
    return HttpResponseRedirect(reverse('recipedetail', kwargs={'r_id': r_id}))


def edit_view(request, r_id):
    r_instance = get_object_or_404(Recipe, id=r_id)
    
    if request.method == 'POST':
        form = RecipeEditForm(request.POST)

        if form.is_valid():
            r_instance.title = form.cleaned_data['title'] #form.title
            r_instance.instructions = form.cleaned_data['instructions']
            r_instance.description = form.cleaned_data['description']
            r_instance.time = form.cleaned_data['time']
            r_instance.save()
            return redirect('/recipe/' + str(r_id))
    else:
        initial_form_data = {
                            'title': r_instance.title, 
                            'author': r_instance.author, 
                            'instructions': r_instance.instructions, 
                            'description': r_instance.description, 
                            'time': r_instance.time
                            }
        form = RecipeEditForm(initial=initial_form_data)

    return render(request, 'recipeedit.html', {'form': form})
