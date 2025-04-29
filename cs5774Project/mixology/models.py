from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

# USERS

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE, related_name='profile', null=True, blank=True)
    bio = models.TextField(max_length=2000, blank=True)
    follows = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    pfp = models.ImageField(upload_to='profile_pics/', blank=True, null=True, default='profile_pics/user.svg')
    
    def __str__(self):
        return self.user.username
    
    def get_absolute_url(self):
        return reverse("mixology:profile", kwargs={"username": self.user.username})
    
    def getJSON(self):
        return {
            'username': self.user.username,
            'bio': self.bio,
            'followers': self.followers.count(),
            'following': self.follows.count(),
            'drinks': self.drinks.count(),
            'pfp': self.get_pfp_url(),
            'url': self.get_absolute_url(),
        }
    
    def get_pfp_url(self):
        return self.pfp.url
    
    def get_drinks(self):
        return self.drinks.all()
    
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
    
    def __str__(self):
        return self.name.title()
    
    def save(self, *args, **kwargs):
        self.name = self.name.strip().lower()
        super().save(*args, **kwargs)

class Drink(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DR', 'Draft'
        PUBLISHED = 'PU', 'Published'
        DELETED = 'DE', 'Deleted'
    
    name = models.CharField(max_length=200)
    poster = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='drinks')
    description = models.TextField(max_length=2000)
    instructions = models.TextField(max_length=2000)
    last_updated = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='posts/', blank=True, null=True, default='mixology/static/assets/drink-default.jpg')
    ingredients = models.ManyToManyField(Ingredient, blank=True, related_name='drinks')
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    
    def __str__(self):
        return f'{self.name} ~ {self.poster.user.username}'
    
    def getJSON(self):
        return {
            'id': self.pk,
            'name': self.name,
            'description': self.description,
            'instructions': self.instructions,
            'last_updated': self.last_updated,
            'image': self.get_image_url(),
            'ingredients': [ingredient.name for ingredient in self.ingredients.all()],
            'status': self.status,
            'url': self.get_absolute_url(),
        }
    
    class Meta:
        ordering = ['name']

    def get_image_url(self):
        return self.image.url
    
    def get_ingredients(self):
        return self.ingredients.all()
    
    def get_absolute_url(self):
        return reverse("mixology:drink", kwargs={"did": self.pk})
    

# COLLECTIONS
class Collection(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='collections')
    drinks = models.ManyToManyField(Drink, blank=True, related_name='collections')
    
    def __str__(self):
        return f'{self.name} ~ {self.owner.user.username}'
    
    def getJSON(self):
        return {
            'id': self.pk,
            'name': self.name,
            'drinks': [drink.getJSON() for drink in self.drinks.all()],
            'owner': self.owner.user.username,
            'url': self.get_absolute_url(),
        }
    
    def get_absolute_url(self):
        return reverse("collections", kwargs={"username": self.owner.user.username})
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Collections'
        
class Comment(models.Model):
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=2000)
    posted = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.drink.name}: {self.text} ~ {self.user.username}'
    
    def getJSON(self):
        return {
            'id': self.pk,
            'drink': self.drink.getJSON(),
            'user': self.user.username,
            'text': self.text,
            'posted': self.posted,
            'url': self.get_absolute_url(),
        }
    
    def get_absolute_url(self):
        # get rid of the slash at the end of the URL
        return reverse("mixology:drink", kwargs={"did": self.drink.pk}).rstrip('/') + f"#comment-{self.pk}"
    class Meta:
        ordering = ['-posted']