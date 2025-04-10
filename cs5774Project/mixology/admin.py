from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Drink)
admin.site.register(UserProfile)
# admin.site.register(AdminUser)
admin.site.register(Ingredient)
admin.site.register(Collection)
admin.site.register(Comment)
