from django.contrib import admin
from .models import *
from actions.models import Action

# Register your models here.
admin.site.register(Drink)
admin.site.register(UserProfile)
# admin.site.register(AdminUser)
admin.site.register(Ingredient)
admin.site.register(Collection)
admin.site.register(Comment)
admin.site.register(Action)
