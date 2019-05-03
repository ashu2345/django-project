from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/',views.SignUp.as_view(), name = 'signup'),
    path('add/<int:item_id>',views.addFood, name = "addFood"),
    path('cart/', views.showCart, name = "cart"),
    path('success/', views.confirmOrder, name = "confirmOrder"),
    path('orders/', views.displayFood, name = "displayFood"),
    path('paymentPage/', views.paymentPortal, name = "paymentPortal"),
    path('deleteorder/<int:cart_id>',views.deleteCartOrder,name = "deleteCartOrder"),
]