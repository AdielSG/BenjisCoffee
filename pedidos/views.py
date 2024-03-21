from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import OrderForm
from .models import Order
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('orders')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'Username Already exists'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            "error": 'Password do not match'
        })

@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user, Completado__isnull=False)
    return render(request, 'orders.html', {'orders': orders})
@login_required
def orders_completed(request):
    orders = Order.objects.filter(user=request.user, Completado__isnull=True).order_by('-datecompleted')
    return render(request, 'orders.html', {'orders': orders})

@login_required
def create_order(request):
    if request.method == 'GET':
        return render(request, 'create_order.html', {
            "form": OrderForm
        })
    else:
        try:
            form = OrderForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('orders')
        except ValueError:
            return render(request, 'create_order.html', {
                "form": OrderForm,
                "error": 'Please provide a valid data'
            })

@login_required
def order_detail(request, orders_id):
    if request.method == 'GET':
        order = get_object_or_404(Order, pk=orders_id, user=request.user)
        form = OrderForm(instance=order)
        return render(request, 'order_detail.html', {'order': order, 'form': form})
    else:
        try:
            order = get_object_or_404(Order, pk=orders_id, user=request.user)
            form = OrderForm(request.POST, instance=order)
            form.save()
            return redirect('orders')
        except ValueError:
            return render(request, 'order_detail.html', {'order': order, 'form': form, 
            'error': "Error actualizando orden"})

@login_required
def complete_order(request, orders_id):
    order = get_object_or_404(Order, pk=orders_id, user=request.user)
    if request.method == 'POST':
        order.Completado = True
        order.save()
        return redirect('orders')

@login_required    
def delete_order(request, orders_id):
    order = get_object_or_404(Order, pk=orders_id, user=request.user)
    if request.method == 'POST':
        order.delete()
        return redirect('orders')

@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'],
            password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or Password is incorrect'
            })
        else:
            login(request, user)
            return redirect('orders')
