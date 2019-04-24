from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from .models import Orders, CustomUser
# Create your views here.
class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'

def addFood(request,food):
    customer = CustomUser.objects.get(username__exact = request.user.username)
    order = Orders(customer = customer, item_name = food)
    order.save()
    return render(request,"users/success.html",{'food':food})

def displayFood(request):
    customer = CustomUser.objects.get(username__exact = request.user.username)
    return render(request,"users/ordlist.html",{'customer':customer})