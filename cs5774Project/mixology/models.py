from django.db import models

# Create your models here.

# USERS

class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    bio = models.TextField(max_length=2000, blank=True)
    slug = models.SlugField(unique=True, max_length=200)
    
    class Meta:
        ordering = ['username']
        
    def get_all_drinks(self):
        return self.drinks.all()
    
    def get_published_drinks(self):
        return self.drinks.filter(status=Drink.Status.PUBLISHED)
    
    def get_drafts(self):
        return self.drinks.filter(status=Drink.Status.DRAFT)
    
    def get_followers(self):
        return self.followers.all()
    
    def get_following(self):
        return self.following.all()
        
    def __str__(self):
        return self.username  
    
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'followed'], name='unique_follow')
        ]
        
    def __str__(self):
        return f'{self.follower} follows {self.followed}'
    
# OBJECTS

class Drink(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DR', 'Draft'
        PUBLISHED = 'PU', 'Published'
        DELETED = 'DE', 'Deleted'
        
    name = models.CharField(max_length=200)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name='drinks')
    description = models.TextField(max_length=2000)
    instructions = models.TextField(max_length=2000)
    last_updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='mixology/static/images/', default='mixology/static/images/default.jpg')
    # ingredients = models.ManyToManyField('Ingredient')
    ingredients = models.CharField(max_length=2000)
    slug = models.SlugField(unique=True, max_length=200)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    
    class Meta:
        ordering = ['name']
        
    def get_image_url(self):
        return self.image.url.replace('/mixology/static/', '')

    def __str__(self):
        return self.name
    
class DrinkManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Drink.Status.PUBLISHED)

# class Ingredient(models.Model):
#     name = models.CharField(max_length=200)
#     drinks = models.ManyToManyField(Drink)

#     def __str__(self):
#         return self.name
    
