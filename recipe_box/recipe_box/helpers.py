def add_favorite(request, recipe):
    request.user.author.favorite.add(recipe)

def remove_favorite(request, recipe):
    current_user = request.user.all()
    current_recipe = request.recipe.all()
    current_user.favorite.remove(current_recipe)

    data ={
        
    }

    return render(request, 'recipe.html', data)
