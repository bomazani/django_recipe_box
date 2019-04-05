def add_favorite(request, recipe):
    request.user.author.favorite.add(recipe)

def remove_favorite(request, recipe):
    request.user.author.favorite.remove(recipe)