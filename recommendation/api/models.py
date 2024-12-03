from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#Define the theme options for our users. Exmaples include Sci-fi, Romance, Action ect.
class Theme(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name

#Define the language setting for our users. Examples include English, Chinese, Japanese, Spanish, etc. 
#These languages are pre-seeded into the db with the following file: # dokudog/management/commands/seed_languages.py
class Language(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

#Define the type of work. Eg: book, article, movie, games, etc. 
class Type(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

#Define a work. This by default currently does not support differentiating between multiple types.
class Work(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    difficulty = models.FloatField()
    themes = models.ManyToManyField(Theme, related_name="works")
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True, related_name='works')
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, related_name='works')
    # Additional fields as needed

    def __str__(self):
        return self.title

#define a user profile for users of the website. Users can only have one native language and one target langauge currently. 
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    difficulty_score = models.FloatField(default=0.5)
    native_language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, related_name='native_users')
    target_language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, related_name='target_users')
    themes = models.ManyToManyField(Theme)

    def __str__(self):
        return f"{self.user.username}'s profile"