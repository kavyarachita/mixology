from django.db import models
from datetime import datetime

# Create your models here.

# USERS

class User():
    def __init__(self, username, password, email, name, bio, slug, follows, drinks, collections):
        self.username = username
        self.password = password
        self.email = email
        self.name = name
        self.bio = bio
        self.slug = slug
        self.follows = follows
        self.drinks = drinks
        self.collections = collections
    
    def __str__(self):
        return self.name


user_0 = User('johndoe', 'password123', 'johndoe@example.com', 'John Doe', 'I love mixing cocktails!', 'user-0', ['user-3'], [], []) # regular user
user_1 = User('janedoe', 'password456', 'janedoe@example.com', 'Jane Doe', 'Passionate about mixology.', 'user-1', ['user-2', 'user-3'], [], [])
user_2 = User('mikesmith', 'password789', 'mikesmith@example.com', 'Mike Smith', 'Mixology enthusiast.', 'user-2', [], [], [])
user_3 = User('sarahjones', 'passwordabc', 'sarahjones@example.com', 'Sarah Jones', 'Exploring new cocktail recipes.', 'user-3', ['user-3', 'user-1'], [], [])
admin = User('admin', 'admin', 'admin@example.com', 'Admin Jones', 'Admin', 'user-4', ['user-2'], [], [])
    
users = {user_0.username: user_0, user_1.username: user_1, user_2.username: user_2, user_3.username: user_3, admin.username: admin}
    
# OBJECTS

class Ingredient():
    def __init__(self, name, slug):
        self.name = name
        self.slug = slug

    def __str__(self):
        return self.name
        
ingredient_0 = Ingredient('tequila', 'tequila')
ingredient_1 = Ingredient('lime juice', 'lime-juice')
ingredient_2 = Ingredient('triple sec', 'triple-sec')
ingredient_3 = Ingredient('gin', 'gin')
ingredient_4 = Ingredient('vermouth', 'vermouth')
ingredient_5 = Ingredient('rum', 'rum')
ingredient_6 = Ingredient('soda water', 'soda-water')
ingredient_7 = Ingredient('mint', 'mint')
ingredient_8 = Ingredient('whiskey', 'whiskey')
ingredient_9 = Ingredient('sugar', 'sugar')
ingredient_10 = Ingredient('bitters', 'bitters')
ingredient_11 = Ingredient('vodka', 'vodka')
ingredient_12 = Ingredient('cranberry juice', 'cranberry-juice')
ingredient_13 = Ingredient('matcha powder', 'matcha-powder')
ingredient_14 = Ingredient('milk', 'milk')
ingredient_15 = Ingredient('water', 'water')
ingredient_16 = Ingredient('coconut cream', 'coconut-cream')
ingredient_17 = Ingredient('pineapple juice', 'pineapple-juice')

ingredients = [ingredient_0, ingredient_1, ingredient_2, ingredient_3, ingredient_4, ingredient_5, ingredient_6, ingredient_7, ingredient_8, ingredient_9, ingredient_10, ingredient_11, ingredient_12, ingredient_13, ingredient_14, ingredient_15, ingredient_16, ingredient_17]

class Drink():
    class Status():
        DRAFT = 'DR', 'Draft'
        PUBLISHED = 'PU', 'Published'
        DELETED = 'DE', 'Deleted'
        
    def __init__(self, name, poster, description, instructions, last_updated, image, ingredients, slug, status):
        self.name = name
        self.poster = poster
        self.description = description
        self.instructions = instructions
        self.last_updated = last_updated
        self.image = image
        self.ingredients = ingredients
        self.slug = slug
        self.status = status
    
    def __str__(self):
        return self.name
        
drink_0 = Drink('Margarita', user_0, 'A classic margarita with a twist!', 'Mix all ingredients in a shaker and serve in a salt-rimmed glass.', datetime(2025, 3, 1, 12, 0, 0), 'images/drink-1.avif', [ingredient_0, ingredient_1, ingredient_2], 'drink-0', Drink.Status.PUBLISHED)
drink_1 = Drink('Martini', user_1, 'A classic martini with a twist!', 'Mix all ingredients in a shaker and serve in a chilled glass.', datetime(2025, 3, 26, 12, 0, 0), 'images/drink-2.jpg', [ingredient_3, ingredient_4], 'drink-1', Drink.Status.PUBLISHED)
drink_2 = Drink('Mojito', user_2, 'A classic mojito with a twist!', 'Muddle mint and lime in a glass, add rum and soda water.', datetime(2025, 3, 23, 12, 0, 0), 'images/drink-3.jpg', [ingredient_1, ingredient_5, ingredient_6, ingredient_7], 'drink-2', Drink.Status.PUBLISHED)
drink_3 = Drink('Old Fashioned', user_2, 'A classic old fashioned with a twist!', 'Muddle sugar and bitters in a glass, add whiskey and ice.', datetime(2024, 12, 4, 12, 0, 0), 'images/drink-4.jpg', [ingredient_8, ingredient_9, ingredient_10], 'drink-3', Drink.Status.PUBLISHED)
drink_4 = Drink('Cosmopolitan', user_3, 'A classic cosmopolitan with a twist!', 'Mix all ingredients in a shaker and serve in a chilled glass.', datetime(2025, 3, 5, 12, 0, 0), 'images/drink-5.jpg', [ingredient_11, ingredient_1, ingredient_12, ingredient_2], 'drink-4', Drink.Status.PUBLISHED)
drink_5 = Drink('Matcha Latte', user_1, 'A classic matcha latte with a twist!', 'Mix matcha powder with hot water, add milk and ice.', datetime(2025, 3, 1, 12, 0, 0), 'images/drink-6.jpg', [ingredient_13, ingredient_14, ingredient_15], 'drink-5', Drink.Status.PUBLISHED)
drink_6 = Drink('Pina Colada', user_0, 'A classic pina colada with a twist!', 'Mix all ingredients in a blender and serve in a chilled glass.', datetime(2025, 3, 1, 12, 0, 0), 'images/drink-3.jpg', [ingredient_5, ingredient_16, ingredient_17], 'drink-6', Drink.Status.PUBLISHED)

drinks = [drink_0, drink_1, drink_2, drink_3, drink_4, drink_5, drink_6]

user_0.drinks = [drink_0, drink_6]
user_1.drinks = [drink_1, drink_5]
user_2.drinks = [drink_2, drink_3]
user_3.drinks = [drink_4]

# COLLECTIONS
class Collection():
    def __init__(self, name, owner, drinks, slug):
        self.name = name
        self.owner = owner
        self.drinks = drinks
        self.slug = slug
    
    def __str__(self):
        return self.name
        
collection_0 = Collection('Favorites', user_0, [drink_1, drink_2], 'collection-0')
collection_1 = Collection('Classics', user_1, [drink_2, drink_3, drink_4,drink_2, drink_3, drink_4,drink_2, drink_3, drink_4,drink_2, drink_3, drink_4], 'collection-1')
collection_2 = Collection('New Recipes', user_3, [drink_5], 'collection-2')
collection_3 = Collection('Sweet Cocktails', user_1, [drink_4, drink_5, drink_6], 'collection-3')


collections = [collection_0, collection_1, collection_2, collection_3]

user_0.collections = [collection_0]
user_1.collections = [collection_1, collection_3]
user_3.collections = [collection_2]