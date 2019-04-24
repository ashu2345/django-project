from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/',views.SignUp.as_view(), name = 'signup'),
    path('add/<slug:food>',views.addFood, name = "addFood"),
    path('orders/', views.displayFood, name = "displayFood"),
]