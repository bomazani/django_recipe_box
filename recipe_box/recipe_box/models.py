from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    bio = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

class Recipe(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    description = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    instructions = models.TextField()