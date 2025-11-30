# products84/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm
from .models import Product, Order
from dublindistance import calculate_distance, suggest_transport #MY PYPI library
import boto3,json
from django.conf import settings
from django.shortcuts import render
from .models import Order
import boto3
import json
from django.shortcuts import redirect, get_object_or_404
from datetime import datetime, timedelta

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')  # Latest first
    return render(request, 'my_orders.html', {'orders': orders})

def landing_page(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.area_code = form.cleaned_data['area_code']
            user.save()
            login(request, user)
            return redirect('landing')
    else:
        form = RegisterForm()
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


def calculate_delivery_time(user_area_code):
    distance = calculate_distance("D1", user_area_code)
    
    # Base = 3 days processing
    base_time = timedelta(days=3)
    
    # Travel time estimation from your library (assume average 40 km/h in Dublin)
    # You can tweak speed if you want
    travel_hours = distance / 40.0
    travel_time = timedelta(hours=travel_hours)
    
    total_time = base_time + travel_time
    return total_time, distance, suggest_transport(distance)

from datetime import datetime, timedelta
from dublindistance import calculate_distance, suggest_transport

@login_required
def order_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user_area = getattr(request.user, 'area_code', 'D15').strip().upper()

    distance_km = calculate_distance("D1", user_area) or 11.53
    transport = suggest_transport(distance_km)

    # Realistic Dublin delivery van speed: 20 km/h average (traffic, stops, etc.)
    travel_hours = distance_km / 10
    total_hours = 72 + travel_hours  # 72 = 3 days processing

    days = int(total_hours // 24)
    hours = int(total_hours % 24)
    minutes = int((total_hours * 60) % 60)

    time_parts = []
    if days > 0:
        time_parts.append(f"{days} day{'s' if days > 1 else ''}")
    if hours > 0:
        time_parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
    if minutes > 0:
        time_parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")

    delivery_estimate = " and ".join(time_parts) if time_parts else "3 days"

    delivery_date = (datetime.now() + timedelta(hours=total_hours)).strftime("%A, %B %d")

    order = Order.objects.create(
        user=request.user,
        product=product,
        delivery_distance_km=round(distance_km, 2)
    )

    payload = {
        'order_id': order.id,
        'username': request.user.username,
        'product': product.name,
        'area_code': user_area,
        'distance_km': round(distance_km, 2),
        'delivery_estimate': delivery_estimate,
        'expected_date': delivery_date,
        'transport': transport,
        'collect_message': f"Collect from D1 – best route: {transport}"
    }

    # Send to SQS
    sqs = boto3.client('sqs', region_name='us-east-1')
    sqs.send_message(
        QueueUrl="https://sqs.us-east-1.amazonaws.com/815527707232/bevman84-queue",
        MessageBody=json.dumps(payload)
    )

    # Send to SNS
    sns = boto3.client('sns', region_name='us-east-1')
    sns.publish(
        TopicArn="arn:aws:sns:us-east-1:815527707232:BevMan84-Notifications",
        Message=json.dumps(payload),
        Subject="New Order"
    )

    messages.success(request,
        f"Order #{order.id} placed! "
        f"Est. delivery: {delivery_estimate} → {delivery_date}. "
        f"Collect from D1 ({transport})")
    return redirect('landing')