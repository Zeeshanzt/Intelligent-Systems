from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm,UserUpdateForm,ProfileUpdateForm
from django.contrib import messages
#import product models
from dashboard.models import Product, Order
from .models import User

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user_name = form.cleaned_data.get('username')
            messages.success(request, f'Account for {user_name} has been successfully created. Now You may Login')
            return redirect('user-login')
    else:
        form = CreateUserForm()

    context = {
        'form':form
    }
    return render(request, 'user/register.html', context)

def profile(request):
    order_count = Order.objects.count()
    product_count = Product.objects.count()
    staff_count = User.objects.count()
    products = Product.objects.all()
    total_stock_quantity = 0
    for product in products:
            total_stock_quantity += product.quantity
    formatted_order_count = '{:,}'.format(order_count)
    formatted_product_count = '{:,}'.format(product_count)
    formatted_staff_count = '{:,}'.format(staff_count)
    total_stock_quantity = '{:,}'.format(total_stock_quantity)
    context = {
        'formatted_order_count': formatted_order_count,
        'formatted_product_count': formatted_product_count,
        'formatted_staff_count': formatted_staff_count,
        'total_stock_quantity': total_stock_quantity,
    }
    return render(request, 'user/profile.html',context)

def profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance= request.user)
        profile_form = ProfileUpdateForm(request.POST,  request.FILES, instance= request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user-profile')
    else:
        user_form = UserUpdateForm( instance= request.user)
        profile_form = ProfileUpdateForm(instance= request.user.profile)
    context = {
        'user_form':user_form,
        'profile_form':profile_form
    }
    return render(request, 'user/profile_update.html', context)