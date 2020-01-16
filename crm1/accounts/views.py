from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory  # it create platform for multiple orders for every individual customer
from .filters import OrderFilter
from .models import *
from .forms import OrderForm # importing orderform for updating and creating order 

from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

def registerPage(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was successfully created for' + user)
            return redirect("login")

    
    context={'form' : form}
    return render(request,'accounts/register.html',context)


def loginPage(request):
    
    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username,password=password)

        if user is not None :
            login(request , user)
            return redirect('home')

        else:
            messages.error(request,'Username or Password is inccorect ')
        
    
    context ={}
    return render(request,'accounts/login.html',context)

@login_required(login_url="login")
def home(request):
    customers = Customer.objects.all()
    orders= Order.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status ='Pending').count()

    context ={'customers':customers ,'orders': orders,
              'total_orders':total_orders,'delivered':delivered,'pending':pending}
    return render(request,'accounts/dashboard.html',context)

def products(request):
    products = Product.objects.all()
    context ={'products':products}
    return render(request,'accounts/products.html', context)

def customer(request,pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    myFilter = OrderFilter(request.GET,queryset=orders)
    orders = myFilter.qs
    total_orders = orders.count()

    context ={'customer':customer,'orders':orders,'total_orders':total_orders,
    'myFilter':myFilter}
    return render(request,'accounts/customer.html',context)


def createOrder(request,pk):
    customer = Customer.objects.get(id=pk)
    OrderFormSet = inlineformset_factory(Customer ,Order ,fields=('product','status'),extra=6)
    formset = OrderFormSet(queryset= Order.objects.none() ,instance = customer)

               
               # form = OrderForm(initial ={'customer':customer})
    
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance = customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context ={'formset':formset}
    return render (request, 'accounts/order_form.html',context)


def updateOrder(request,pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance = order)
    
    if request.method == 'POST':
        form =OrderForm(request.POST , instance=order )
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render (request, 'accounts/order_form.html',context)

'''
    def deleteOrder(request,pk):
        order = Order.objects.get(id=pk)

        if request.method == 'POST':
            order.delete()
            return redirect('/')

        context ={'items':order}
        return render (request, 'accounts/delete_form.html',context)

        '''