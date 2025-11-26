# products84/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required   # ← THIS WAS MISSING!
from django.contrib import messages
from .models import Product, Order
from dublindistance import calculate_distance   # your library
import boto3
from django.conf import settings

def landing_page(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome {user.username}!")
            return redirect('landing')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('landing')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('landing')

@login_required
def order_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Use real Dublin area codes your library knows
    distance = calculate_distance("D1", "D15")  # Dublin 1 to Dublin 15
    
    if distance is None:
        distance = 12.5  # fallback

    order = Order.objects.create(
        user=request.user,
        product=product,
        delivery_distance_km=distance
    )
    messages.success(request, f"Order #{order.id} placed! Delivery distance: {distance} km (D1 → D15)")
    return redirect('landing')