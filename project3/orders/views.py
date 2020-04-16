from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from .models import Menu, MenuItem, Topping, OrderItem, Order, Variation, Pizza

from .forms import SignUpForm

import json

# Create your views here.

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'orders/signup.html'

# index page
def index(request):

    context = {
        'menus':  Menu.objects.all(),
    }
    return render(request, 'orders/index.html', context)

# cart page
@login_required
@csrf_exempt
def order(request):

    if request.method == 'POST':
        try:
            order = json.loads(request.body)
            menu_item = MenuItem.objects.get(name=order['name'])
            variation = ''

            if order['variation'] != '':
                variation = menu_item.variations.get(name=order['variation'])
                order_price = variation.price * int(order['quantity'])
            else:
                order_price = menu_item.price * int(order['quantity'])
            
            order_obj = Order.objects.create(
                user = request.user,
                price = order_price,
                quantity = int(order['quantity'])
            )
            
            order_item = OrderItem.objects.create(
                name = menu_item.name,
                category = menu_item.category,
                veg = menu_item.veg,
                price = menu_item.price,
                order = order_obj
            )

            if variation != '':
                Variation.objects.create(
                    name = variation.name,
                    price = variation.price,
                    order_item = order_item
                )

            if len(order['toppings']) > 0:
                pizza = Pizza.objects.create(
                    order_item = order_item,
                    num_of_toppings = len(order['toppings'])
                )
                for topping in order['toppings']:
                    Topping.objects.get(name=topping['name']).pizza.add(pizza)
        
        except Exception as e:
            return JsonResponse(
                {
                    'success': False,
                    'error': str(e)
                }
            )

        return JsonResponse(
            {
                'id': menu_item.id,
                'success': True
            }
        )
    
    else:
        return render(request, 'orders/cart.html')

# logout
@login_required
def logout_view(request):
    logout(request)
    return redirect(request, 'index')

# menu items api
def item_api(request, item_id):

    try:    
        item = MenuItem.objects.get(pk=item_id)
    except:
        return JsonResponse(
            {
                'error': 'No item found' 
            }
        )

    variations = []
    features = []
    
    for variation in item.variations.all():
        variations.append({'name':variation.name, 'price':variation.price})

    try:
        if item.pizza:
            features.append({'num_of_toppings':item.pizza.num_of_toppings})
    except:
        pass

    return JsonResponse(
        {
            'id': item.id,
            'name': item.name,
            'img': item.img,
            'price': item.price,
            'veg': item.veg,
            'variations': variations,
            'more_features': features
        },
        safe=False
    )

# get toppings
def toppings_api(request):
        
    toppings = []

    for topping in Topping.objects.all():
        toppings.append({'name': topping.name})

    return JsonResponse(
        {
            'toppings': toppings
        },
        safe=False
    )

# get menus
def menus_api(request):

    menus = []

    for menu in Menu.objects.all():
        items = []
        
        for item in menu.menu_items.all():
            
            variations = []
            
            for variation in item.variations.all(): 
                variations.append({'name':variation.name, 'price':variation.price})
            
            items.append({'id':item.id, 'name':item.name, 'img':item.img, 'description':item.description, 'variations':variations})
        
        menus.append({
            'name': menu.name,
            'items': items,
        })
    
    return JsonResponse(
        {
            'menus': menus
        },
        safe=False
    )