from django.contrib import admin

from .models import Food, Extra, FoodCategory

admin.site.register(Food)
admin.site.register(Extra)
admin.site.register(FoodCategory)
