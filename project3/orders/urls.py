from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path(r"", views.index, name="index"),
    path(r"cart/", views.cart, name="cart"),
    path(r"orders/display/", views.display_orders, name="display orders"),
    path(r"orders/history/", views.orders_history, name="order history"),  
    path(r"accounts/signup/", views.SignUpView.as_view(), name='signup'),
    path(r"accounts/logout/", views.logout_view, name='logout'),
    path(r"api/item/<int:item_id>", views.item_api, name="item api"),
    path(r"api/menus", views.menus_api, name="menus"),
    path(r"api/toppings", views.toppings_api, name="toppings"),
    path(r"api/order", views.order, name="order"),
    path(r"api/orders/update/", views.update_order, name="order update"),
    path(r"accounts/login/", auth_views.LoginView.as_view(template_name='orders/login.html')),
]
