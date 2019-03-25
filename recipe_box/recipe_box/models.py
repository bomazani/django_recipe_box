from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    bio = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    description = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    instructions = models.TextField()
    # *** Need to uncomment the following line, then makemigrations and migrate. ***
    # favorite = models.ManyToManyField("self", related_name='favorite_of', symmetrical=False)


    def __str__(self):
        return self.title