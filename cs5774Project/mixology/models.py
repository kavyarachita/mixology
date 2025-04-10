from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.

# USERS

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE, related_name='profile', null=True, blank=True)
    name = models.CharField(max_length=200)
    bio = models.TextField(max_length=2000, blank=True)
    follows = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    pfp = models.ImageField(upload_to='mixology/static/profile_pics', blank=True, null=True, default='mixology/static/assets/icons/user.svg')
    
    def __str__(self):
        return self.user.username
    
    def get_pfp_url(self):
        return self.pfp.url.replace('/mixology/static/', '')
    
    def get_drinks(self):
        return self.user.drinks.all()
    
    def get_followers(self):
         return self.followers.all()
    
    def get_following(self):
        return self.follows.all()
    
    def get_collections(self):
        return self.user.collections.all()
    
    def get_drafts(self):
        return self.user.drinks.filter(status='DR')
    
    def get_published(self):
        return self.user.drinks.filter(status='PU')
    
# OBJECTS

class Ingredient(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class Drink(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DR', 'Draft'
        PUBLISHED = 'PU', 'Published'
        DELETED = 'DE', 'Deleted'
    
    name = models.CharField(max_length=200)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name='drinks')
    description = models.TextField(max_length=2000)
    instructions = models.TextField(max_length=2000)
    last_updated = models.DateTimeField(default=datetime.now)
    image = models.ImageField(upload_to='mixology/static/posts', blank=True, null=True)
    ingredients = models.ManyToManyField(Ingredient, blank=True, related_name='drinks')
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

    def get_image_url(self):
        return self.image.url.replace('/mixology/static/', '')
    
    def get_ingredients(self):
        return self.ingredients.all()
    

# COLLECTIONS
class Collection(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')
    drinks = models.ManyToManyField(Drink, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Collections'
        
class Comment(models.Model):
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=2000)
    posted = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} - {self.drink.name}'
    
    class Meta:
        ordering = ['-posted']