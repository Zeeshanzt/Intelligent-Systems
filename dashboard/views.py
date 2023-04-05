from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product, Order
from .forms import ProductForm,OrderForm
from django.contrib.auth.models import User
from django.contrib import messages

import os
from django.conf import settings
import cv2
import numpy as np
from pyzbar import pyzbar
from datetime import date, timedelta



# def display_images(request):
#     # The path to the folder containing the images
#     folder_path = settings.PROJECT_ROOT
    
#     # An array to store the file paths of the images
#     image_paths = []
    

#     # Loop through the folder and add the file paths of the images to the array
#     for filename in os.listdir(folder_path):
#         if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png') or filename.endswith('.gif'):
#             image_paths.append(os.path.join(folder_path, filename))
    
#     # Pass the list of image file paths to the template
#     return render(request, 'dashboard/image_gallery.html', {'image_paths': image_paths})


def process_qr_codes(folder_path):
   for filename in os.listdir(folder_path):
        # Load image from the folder
        image = cv2.imread(os.path.join(folder_path, filename))
        # Decode QR codes in the image
        decoded_objs = pyzbar.decode(image)
        for obj in decoded_objs:
            # Extract data from the QR code
            qr_data = obj.data.decode("utf-8")
            # Split the data into fields
            fields = qr_data.split("&")
            data = {}
            for field in fields:
                key, value = field.split("=")
                data[key] = value
            # Create a Product object and save to the database
            #if data.get("name", "") and data.get("product_id", ""):
                # Create a Product object and save to the database
            product, created = Product.objects.get_or_create(product_id=data.get("product_id"))
            if created:
                product.name = data.get("name", "")
                product.category = data.get("category", "")
                product.product_id = data.get("product_id", "")
                product.manufacturing_date = data.get("manufacturing_date", "")
                product.expiration_date = data.get("expiration_date", "")
                product.manufacturer_name = data.get("manufacturer_name", "")
                product.product_price = data.get("product_price", "")
                product.quantity = int(data.get("quantity", 0))
                product.save()
                



@login_required
def process_images(request):
    process_qr_codes(settings.PROJECT_ROOT)

    return render(request, 'dashboard/process_images.html')


# Create your views here.
@login_required
def index(request):
    orders = Order.objects.all()
    products = Product.objects.all()
    order_count = orders.count()
    product_count = products.count()
    staff_count = User.objects.all().count()

    #For Product Quantities Calculations 
    product_quantity_dict = {}
    for product in products:
        if product.name in product_quantity_dict:
            product_quantity_dict[product.name.upper()] += product.quantity
        else:
            product_quantity_dict[product.name.upper()] = product.quantity

    # create separate lists for product names and total quantities
    product_names = []
    total_quantities = []
    for product_name, total_quantity in product_quantity_dict.items():
        product_names.append(product_name)
        total_quantities.append(total_quantity)




    #Processing For Order Products Graph 
    ordered_products = {}
    for order in orders:
        category = order.product.name.upper()  # Convert to lowercase for case insensitivity
        if category in ordered_products:
            ordered_products[category] += order.quantity
        else:
            ordered_products[category] = order.quantity

    # Convert categories dictionary to lists for use in chart
    order_labels = list(ordered_products.keys())
    order_quantities = list(ordered_products.values())


    #Processing For Number of Order per Bookers Graph 
    orderers = {}
    for order in orders:
        category = order.staff.username.upper()  # Convert to lowercase for case insensitivity
        if category in orderers:
            orderers[category] += 1
        else:
            orderers[category] = 1

    # Convert categories dictionary to lists for use in chart
    orderer_labels = list(orderers.keys())
    orderer_quantities = list(orderers.values())


    expiration_dates = {}
    for product in products:
        expiration_dates['name'] = product.name    
        expiration_dates['expiration_date'] = product.expiration_date




    #Processing For Product Categories Graph 
    categories = {}
    for product in products:
        category = product.category.upper()  # Convert to lowercase for case insensitivity
        if category in categories:
            categories[category] += product.quantity
        else:
            categories[category] = product.quantity

    # Convert categories dictionary to lists for use in chart
    category_labels = list(categories.keys())
    category_quantities = list(categories.values())


    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            instance = order_form.save(commit=False)
            instance.staff = request.user
            instance.save()
            return redirect('dashboard-home')
    else:
        order_form = OrderForm()

    context = {
        'orders': orders,
        'products': products,
        'order_form':order_form,
        'product_count':product_count,
        'staff_count':staff_count,
        'order_count':order_count,
        'category_labels': category_labels,
        'category_quantities': category_quantities,
        'order_labels': order_labels,
        'order_quantities': order_quantities,
        'orderer_labels': orderer_labels,
        'orderer_quantities': orderer_quantities,
        'product_names': product_names,
        'total_quantities': total_quantities,
        'expiration_dates':expiration_dates,
    }
    return render(request, 'dashboard/index.html',context)

@login_required
def staff(request):
    workers = User.objects.all()
    order_count = Order.objects.all().count()
    product_count = Product.objects.all().count()
    staff_count = User.objects.all().count()

    context = {
        'workers': workers,
        'product_count':product_count,
        'staff_count':staff_count,
        'order_count':order_count,
    }
    return render(request, 'dashboard/staff.html', context)


@login_required
def staff_update(request, pk):
    order_count = Order.objects.all().count()
    product_count = Product.objects.all().count()
    staff_count = User.objects.all().count()
    worker = User.objects.get(id = pk)
    context = {
        'worker': worker,
        'product_count':product_count,
        'staff_count':staff_count,
        'order_count':order_count,
    }

    return render(request, 'dashboard/staff_update.html', context)



@login_required
def product(request):
    order_count = Order.objects.all().count()
    product_count = Product.objects.all().count()
    staff_count = User.objects.all().count()
    if (request.method == 'POST'):
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            product_form.save()
            product_name = product_form.cleaned_data.get('name')
            messages.success(request, f'{product_name} has been added successfully')
            return redirect('dashboard-product')
    else:
        product_form = ProductForm()

    items = Product.objects.all()
    

    
    #items = Product.objects.raw('SELECT * FROM dashboard_product')
    context = {
        'items': items,
        'product_form':product_form,
        'product_count':product_count,
        'staff_count':staff_count,
        'order_count':order_count,
    }
    return render(request, 'dashboard/product.html',context)

@login_required    
def product_delete(request,pk):
    item = Product.objects.get(id = pk)
    if (request.method == 'POST'):
        item.delete()
        return redirect('dashboard-product')
    context={

    }
    return render(request, 'dashboard/product_delete.html', context)

    
@login_required    
def product_update(request,pk):
    order_count = Order.objects.all().count()
    product_count = Product.objects.all().count()
    staff_count = User.objects.all().count()
    item = Product.objects.get(id = pk)
    if (request.method == 'POST'):
        update_form = ProductForm(request.POST, instance=item)
        if update_form.is_valid():
            update_form.save()
            return redirect('dashboard-product')
    else:
        update_form = ProductForm(instance=item)

    context={
        'update_form': update_form,
        'product_count':product_count,
        'staff_count':staff_count,
        'order_count':order_count,
    }
    return render(request, 'dashboard/product_update.html', context)

    
@login_required    
def order(request):
    order_count = Order.objects.all().count()
    product_count = Product.objects.all().count()
    staff_count = User.objects.all().count()
    orders = Order.objects.all()
    context={
        'orders':orders,
        'product_count':product_count,
        'staff_count':staff_count,
        'order_count':order_count,

    }
    return render(request, 'dashboard/order.html', context)