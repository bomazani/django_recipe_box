"""recipe_box URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from recipe_box.models import Author, Recipe
from recipe_box.views import index, recipe, author, recipeadd, authoradd
from recipe_box.views import signup_view, login_view, logout_view, add_favorite_view, remove_favorite_view


admin.site.register(Author)
admin.site.register(Recipe)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='homepage'),
    path('recipe/<int:r_id>', recipe, name="recipedetail"),
    path('recipe/favorite/<int:r_id>', add_favorite_view),
    path('recipe/remove_favorite/<int:r_id>', remove_favorite_view),
    path('author/<int:a_id>', author),
    path('recipeadd/', recipeadd),
    path('authoradd/', authoradd),
    path('signup/', signup_view),
    path('login/', login_view),
    path('logout/', logout_view),
]
