from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import OrderForm, ProductForm
from .models import Order, Product, Cart, CartItem, OrderItem, Rewards
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
import json
from django.contrib.sessions.backends.db import SessionStore

# Create your views here.


def home(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, completed=True).first()
        context = {"cart": cart}
        return render(request, 'home.html', context)
    else:
        cart = Cart.objects.filter(session_key=request.session.session_key, completed=True).first()
        
    context = {"cart": cart}
    return render(request, 'home.html', context)

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
                Points = Rewards.objects.create(User=request.user, Quantity = 10)
                Points.save()
                return redirect('products')
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
    # orders = Order.objects.all()
    carts = Cart.objects.all()
    if request.user.is_authenticated:
        # order, created = Order.objects.get_or_create(user=request.user)
        carts = Cart.objects.filter(completed=True, listo=False)

    if carts:
        context = {"carts": carts, "cart": carts[0]}
    else:
        context = {"carts": [0], "cart": [0]}
    return render(request, 'orders.html', context)

def my_orders(request):
    # orders = Order.objects.all()
    carts = Cart.objects.all()
    if request.user.is_authenticated:
        # order, created = Order.objects.get_or_create(user=request.user)
        carts = Cart.objects.filter(user=request.user,completed=True)

    if carts:
        context = {"carts": carts, "cart": carts[0]}
    else:
        context = {"carts": []}
    return render(request, 'orders.html', context)

def products(request):
    products = Product.objects.all()
    if request.session.session_key is None:
            request.session.create()

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        points = Rewards.objects.get(User=request.user)
        context = {"products": products, "cart": cart, "points": points}
        return render(request, 'products.html', context)
    else:
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key, completed=False)
        context = {'products': products, 'cart': cart,}
        return render(request, 'products.html', context)

  
def product_admin(request):
    products = Product.objects.all()
    if request.user.is_staff:
        context = {"products": products}
        return render(request, 'product_admin.html', context)
    else:
        return HttpResponse(401, 'No tiene permisos para esta área')

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
        

def product_detail(request, products_id):
    if request.method == 'GET':
        product = get_object_or_404(Product, pk=products_id)
        form = ProductForm(instance=product)
        return render(request, 'product_detail.html', {'product': product, 'form': form})
    else:
        try:
            product = get_object_or_404(Product, pk=products_id)
            form = ProductForm(request.POST, instance=product)
            form.save()
            return redirect('products')
        except ValueError:
            return render(request, 'product_detail.html', {'product': product, 'form': form, 
            'error': "Error actualizando producto"})

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
            return redirect('products')


def cart(request, cart_id=None):
    if cart_id:
        try:
            cart = Cart.objects.get(pk=cart_id, completed=False)
            cartitems = cart.cartitems.all()
            context = {"cart": cart, "items": cartitems}
            return render(request, "cart.html", context)
        except Cart.DoesNotExist:
            return redirect('products')
    else:
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
            cartitems = cart.cartitems.all()
            context = {"cart": cart, "items": cartitems}
            return render(request, "cart.html", context)
        else:
            cart, created = Cart.objects.get_or_create(session_key=request.session.session_key, completed=False)
            cartitems = cart.cartitems.all()
            context = {"cart": cart, "items": cartitems}
            return render(request, "cart.html", context)
    

def cart_admin(request, cart_id):
    if request.user.is_staff:
        try:
            # Obtener el carrito activo del usuario
            cart = Cart.objects.get(pk=cart_id, completed=True)
            cartitems = cart.cartitems.all()
            context = {"cart": cart, "items": cartitems}
            return render(request, "cart.html", context)
        except Cart.DoesNotExist:
            # Si no se encuentra un carrito activo, redirigir a la página de productos
            return redirect('orders')
    else:
        # Si el usuario no está autenticado, redirigir a la página de productos
        return redirect('products')
    
def cart_client(request, cart_id):
    if request.user.is_authenticated:
        try:
            # Obtener el carrito activo del usuario
            cart = Cart.objects.get(pk=cart_id, completed=True)
            cartitems = cart.cartitems.all()
            context = {"cart": cart, "items": cartitems}
            return render(request, "cart.html", context)
        except Cart.DoesNotExist:
            # Si no se encuentra un carrito activo, redirigir a la página de productos
            return redirect('orders')
    else:
        # Si el usuario no está autenticado, redirigir a la página de productos
        return redirect('products')
    

def add_to_cart(request):
    data = json.loads(request.body)
    product_id = data["id"]
    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        cartitem, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cartitem.quantity += 1
        cartitem.save()

        num_of_item = cart.num_of_items

        print(cartitem)
    else:
        if request.session.session_key is None:
            request.session.create()
            
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key, completed=False)
        if request.session.session_key:
            print(request.session.session_key)
        else:
            print('No hay')
        cartitem, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cartitem.quantity += 1
        cartitem.save()

        num_of_item = cart.num_of_items

    return JsonResponse(num_of_item, safe=False)
    

def complete_cart(request, cart_id):
    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, pk=cart_id, user=request.user)
        if request.method == 'POST':
            cart.completed = True
            cart.save()
        return redirect('products')
    else:
        cart = get_object_or_404(Cart, pk=cart_id, session_key=request.session.session_key)
        if request.method == 'POST':
            cart.completed = True
            cart.save()
        return redirect('products')

@login_required
def complete_client_order(request, cart_id):
    cart = get_object_or_404(Cart, pk=cart_id)
    
    # Verificar si el cart tiene un usuario asociado
    if cart.user is not None:
        try:
            get_user = User.objects.get(id=cart.user.id)
            puntos = get_object_or_404(Rewards, User=get_user)

            if request.method == 'POST':
                cart.listo = True
                puntos.Quantity = puntos.Quantity + 10
                cart.save()
                puntos.save()
                
                return redirect('orders')
        except User.DoesNotExist:
            return HttpResponse("User not found", status=404)
        except Rewards.DoesNotExist:
            return HttpResponse("Rewards not found for user", status=404)
    else:
        if request.method == 'POST':
            cart.listo = True
            cart.save()
            
            return redirect('orders')


def delete_cart(request, cart_id):
    cart = get_object_or_404(Cart, id=cart_id)
    if request.method == 'POST':
        cart.delete()
    return redirect('products')
