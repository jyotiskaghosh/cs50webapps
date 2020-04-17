from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# menu
class Menu(models.Model):

    name = models.CharField(max_length=64, unique=True)

    def no_space_name(self):
        return self.name.replace(' ', '-')

    def __str__(self):
        return f"{self.name} menu"

# abstract item
class AbstractItem(models.Model):

    name = models.CharField(max_length=64)
    description = models.CharField(max_length=250, default="enter description")
    img = models.CharField(max_length=100, default='orders/images/dish1.png')
    category = models.CharField(max_length=20,
        choices=[
            ('pizza','pizza'),
            ('dinner platter','dinner_platter'),
            ('pasta','pasta'),
            ('salad','salad'),
            ('sub','sub')
    ])
    veg = models.BooleanField()
    
    price = models.FloatField()

    class Meta:
        abstract = True

    def __str__(self):
        return f"food item: {self.name}, price: {self.price}"

# order
class Order(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    description = models.CharField(max_length=100, default="enter description")
    datetime = models.DateTimeField(auto_now=True)
    price = models.FloatField()
    completed = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"""user {self.user} has ordered ({self.description}) x {self.quantity} at {self.datetime}.
        price of order: {self.price}"""

# menu item
class MenuItem(AbstractItem):

    name = models.CharField(max_length=64, unique=True)
    menu = models.ManyToManyField(Menu, related_name='menu_items', blank=True)

# order item
class OrderItem(AbstractItem):

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='order')
    
# variation
class Variation(models.Model):

    name = models.CharField(max_length=64)
    price = models.FloatField()

    menu_item = models.ManyToManyField(MenuItem, related_name='variations')
    order_item = models.OneToOneField(OrderItem, related_name='variation', blank=True, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"item: {self.menu_item}, variation name: {self.name}, price: {self.price}"

# pizza
class Pizza(models.Model):

    menu_item = models.OneToOneField(MenuItem, related_name='pizza', blank=True, on_delete=models.CASCADE, null=True)
    order_item = models.OneToOneField(OrderItem, related_name='pizza', blank=True, on_delete=models.CASCADE, null=True)
    num_of_toppings = models.IntegerField()

    def __str__(self):
        return f"pizza with {self.num_of_toppings} toppings"

# topping
class Topping(models.Model):
    
    pizza = models.ManyToManyField(Pizza, blank=True, related_name='toppings')
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"{self.name}"