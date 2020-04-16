from django.contrib import admin

from .models import Menu, MenuItem, Order, Topping, Variation, Pizza, OrderItem

class MenuItemAdmin(admin.ModelAdmin):
    fields = ('name', 'img', 'description', 'category', 'veg', 'price', 'menu')

# Register your models here.
admin.site.register(Menu)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Pizza)
admin.site.register(Topping)
admin.site.register(Variation)