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
import datetime
from datetime import date, timedelta, timezone
from django.db.models import Count
import random
from faker import Faker
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Product, CATEGORY

# add multiline comments down here instead of single line
orders = Order.objects.all()
products = Product.objects.all()
order_count = orders.count()
product_count = products.count()
staff_count = User.objects.all().count()
     # format these counts with commas to separate thousands
formatted_order_count = '{:,}'.format(order_count)
formatted_product_count = '{:,}'.format(product_count)
formatted_staff_count = '{:,}'.format(staff_count)

"""
products_random = [
    # Electronics
    'Smartwatch',
    'Laptop',
    'Wireless earphones',
    'Bluetooth speaker',
    'Gaming console',
    'Smart TV',
    'Digital camera',
    'Virtual reality headset',
    'Smart home assistant',
    'Drone',
    'Fitness tracker',
    'Portable charger',
    'Headphones',
    'Wireless charging pad',
    'Security camera',
    'External hard drive',
    'Gaming mouse',
    'Gaming keyboard',
    'Gaming headset',
    'Smart thermostat',

    # Clothing and Apparel
    'T-shirt',
    'Hoodie',
    'Sweatpants',
    'Shorts',
    'Dress',
    'Skirt',
    'Suit',
    'Coat',
    'Jacket',
    'Sweater',
    'Scarf',
    'Hat',
    'Sunglasses',
    'Belt',
    'Watch',
    'Socks',
    'Underwear',
    'Gloves',
    'Boots',
    'Sneakers',

    # Home and Kitchen Appliances
    'Coffee maker',
    'Toaster',
    'Microwave',
    'Blender',
    'Food processor',
    'Slow cooker',
    'Stand mixer',
    'Air fryer',
    'Vacuum cleaner',
    'Air purifier',
    'Humidifier',
    'Dehumidifier',
    'Iron',
    'Handheld vacuum',
    'Electric kettle',
    'Pressure cooker',
    'Rice cooker',
    'Juicer',
    'Bread maker',
    'Waffle maker',

    # Beauty and Personal Care Products
    'Shampoo',
    'Conditioner',
    'Body wash',
    'Face wash',
    'Moisturizer',
    'Sunscreen',
    'Lip balm',
    'Face serum',
    'Hair oil',
    'Face mask',
    'Eye cream',
    'Facial toner',
    'Body lotion',
    'Hair conditioner',
    'Perfume',
    'Nail polish',
    'Lipstick',
    'Mascara',
    'Foundation',
    'Bronzer',

    # Food
    'Chocolate',
    'Chips',
    'Cookies',
    'Bread',
    'Cheese',
    'Yogurt',
    'Cereal',
    'Granola bars',
    'Trail mix',
    'Popcorn',
    'Nuts',
    'Dried fruit',
    'Protein bars',
    'Energy drinks',
    'Soda',
    'Tea',
    'Coffee',
    'Juice',
    'Ice cream',
    'Pizza',
]

@login_required
def dummy_data(request):
    fake = Faker()


    # Create 1000 Product objects
    for i in range(1000):
        # Choose a random category
        category = random.choice(CATEGORY)[0]

        # Generate random data for the object
        name = products_random[random.randint(0, len(products_random) - 1)]
        quantity = random.randint(1, 100)
        product_id = fake.isbn10()
        manufacturing_date = fake.date_between(start_date='-5y', end_date='today')
        expiration_date = fake.date_between(start_date='today', end_date='+5y')
        manufacturer_name = fake.company()
        product_price = round(random.uniform(10.0, 100.0), 2)
        is_available = random.choice([True, False])

        # Create and save the Product object
        product = Product(
            name=name,
            category=category,
            quantity=quantity,
            product_id=product_id,
            manufacturing_date=manufacturing_date,
            expiration_date=expiration_date,
            manufacturer_name=manufacturer_name,
            product_price=product_price,
            is_available=is_available,
        )
        product.save()
    return render(request, 'dashboard/dummy_data.html')

@login_required
def dummy_orders(request):
    products = Product.objects.all()
    staff = User.objects.filter()
    for i in range(1000):
        product = random.choice(products)
        staff_member = random.choice(staff)
        quantity = random.randint(1, 10)
        date = datetime.now() - timedelta(days=random.randint(1, 365))
        is_delivered = random.choice([True, False])
        order = Order(product=product, staff=staff_member, quantity=quantity, date=date, is_delivered=is_delivered)
        order.save()

    return render(request, 'dashboard/dummy_orders.html')
"""
'''
 def display_images(request):
     # The path to the folder containing the images
     folder_path = settings.PROJECT_ROOT
   
     # An array to store the file paths of the images
     image_paths = []
   
     # Loop through the folder and add the file paths of the images to the array
     for filename in os.listdir(folder_path):
         if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png') or filename.endswith('.gif'):
             image_paths.append(os.path.join(folder_path, filename))
    
     # Pass the list of image file paths to the template
     return render(request, 'dashboard/image_gallery.html', {'image_paths': image_paths})
'''

def process_qr_codes(folder_path):
    exceptions_count = 0
    processed_count = 0
    change_folder_path = os.path.join(str(folder_path),'formatted/')
    
    try:
        # iterate through the files in the folder
        for filename in os.listdir(change_folder_path):
            try:
                # Load image from the folder
                image = cv2.imread(os.path.join(change_folder_path, filename))
                
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
                
                processed_count += 1
                
            except Exception as e:
                print(f"Exception occurred while processing {filename}: {e}")
                
                # move the file causing the exception to a new folder named "Unformatted"
                if not os.path.exists(os.path.join(folder_path, "Unformatted")):
                    os.mkdir(os.path.join(folder_path, "Unformatted"))
                
                os.rename(os.path.join(change_folder_path, filename), os.path.join(folder_path, "Unformatted", filename))
                
                exceptions_count += 1
            
    except ValueError:
        print("ValueError: Please check the correct QR folder path")

    return processed_count, exceptions_count
            



@login_required
def process_images(request):
    product_count = Product.objects.count()
    order_count = Order.objects.count()
    staff_count = User.objects.count()
    products = Product.objects.all()
    total_stock_quantity = 0
    for product in products:
            total_stock_quantity += product.quantity
    formatted_order_count = '{:,}'.format(order_count)
    formatted_product_count = '{:,}'.format(product_count)
    formatted_staff_count = '{:,}'.format(staff_count)
    total_stock_quantity = '{:,}'.format(total_stock_quantity)
    exception_count = 0
    processed_count = 0
    processed_count,exception_count = process_qr_codes(settings.PROJECT_ROOT)
    context = {
        'processed_count': processed_count,
        'exception_count': exception_count,
        'product_count': product_count,
        'order_count': order_count,
        'staff_count': staff_count, 
        'total_stock_quantity': total_stock_quantity,
        'formatted_order_count': formatted_order_count,
        'formatted_staff_count': formatted_staff_count,
        'formatted_product_count': formatted_product_count,
    }
    return render(request, 'dashboard/process-images.html', context)

# Search Results View
@login_required
def search_results(request):
    orders_count = Order.objects.count()
    products_count = Product.objects.count()
    staff_count = User.objects.count()
    total_stock_quantity = 0
    formatted_order_count = '{:,}'.format(orders_count)
    formatted_product_count = '{:,}'.format(products_count)
    formatted_staff_count = '{:,}'.format(staff_count)
    products = Product.objects.all()
    for product in products:
            total_stock_quantity += product.quantity
    total_stock_quantity = '{:,}'.format(total_stock_quantity)
    if request.method == 'POST':
        searched = request.POST['searched']
        orders = Order.objects.filter(product__name__contains=searched)
        products = Product.objects.filter(name__contains=searched)
        context = {
            'searched': searched,
            'orders': orders,
            'products': products,
            'formatted_order_count': formatted_order_count,
            'formatted_product_count': formatted_product_count,
            'formatted_staff_count': formatted_staff_count,
            'total_stock_quantity': total_stock_quantity,
        }
        return render(request, 'dashboard/search_results.html', context)
    else:
        context = {
            'formatted_order_count': formatted_order_count,
            'formatted_product_count': formatted_product_count,
            'formatted_staff_count': formatted_staff_count,
            'total_stock_quantity': total_stock_quantity,
        }
        return render(request, 'dashboard/search_results.html', context)


# Create your views here.
@login_required
def index(request):
    orders = Order.objects.all()
    products = Product.objects.all()
    order_count = orders.count()
    product_count = products.count()
    staff_count = User.objects.all().count()
     # format these counts with commas to separate thousands
    formatted_order_count = '{:,}'.format(order_count)
    formatted_product_count = '{:,}'.format(product_count)
    formatted_staff_count = '{:,}'.format(staff_count)
    
    #For Product with most orders
    product_most_orders = orders.values('product__name').annotate(total_orders=Count('product')).order_by('-total_orders')[:10]
    product_most_orders_names = [item['product__name'] for item in product_most_orders]
    product_most_orders_data = [item['total_orders'] for item in product_most_orders]


    #for filtering productts with quantity less than 20 and sort them in ascending order
    critical_products = Product.objects.filter(quantity__lt=10).order_by('quantity')

    #for filtering products expiring in 3 months and sort them in ascending order
    expiring_products = Product.objects.filter(expiration_date__lte=date.today() + timedelta(days=90)).order_by('expiration_date')
    total_stock_quantity = 0
    for product in products:
            total_stock_quantity += product.quantity
    
    total_stock_quantity = '{:,}'.format(total_stock_quantity)

    #for product total quantity maintaining their expiry date
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
        'product_most_orders_names':product_most_orders_names,
        'product_most_orders_data':product_most_orders_data,
        'critical_products':critical_products,
        'expiring_products':expiring_products,
        'formatted_order_count':formatted_order_count,
        'formatted_product_count':formatted_product_count,
        'formatted_staff_count':formatted_staff_count,
        'total_stock_quantity':total_stock_quantity,
    }
    return render(request, 'dashboard/index.html',context)



@login_required
def analytics(request):
    orders = Order.objects.all()
    products = Product.objects.all()
    order_count = orders.count()
    product_count = products.count()
    staff_count = User.objects.all().count()
    # format these counts with commas to separate thousands
    formatted_order_count = '{:,}'.format(order_count)
    formatted_product_count = '{:,}'.format(product_count)
    formatted_staff_count = '{:,}'.format(staff_count)
    total_stock_quantity = 0
    for product in products:
            total_stock_quantity += product.quantity
    
    total_stock_quantity = '{:,}'.format(total_stock_quantity)
    
    #For Product with most orders
    product_most_orders = orders.values('product__name').annotate(total_orders=Count('product')).order_by('-total_orders')[:10]
    product_most_orders_names = [item['product__name'] for item in product_most_orders]
    product_most_orders_data = [item['total_orders'] for item in product_most_orders]

    #for finding the number of orders per booker
    orderers = {}
    for order in orders:
        category = order.staff.username.upper()
        if category in orderers:
            orderers[category] += 1
        else:
            orderers[category] = 1

    # Convert categories dictionary to lists for use in chart
    orderer_labels = list(orderers.keys())
    orderer_quantities = list(orderers.values())

    #finding monthly orders to make a graph with respect to months
    monthly_orders = {}
    for order in orders:
        category = order.date.strftime("%B")
        if category in monthly_orders:
            monthly_orders[category] += 1
        else:
            monthly_orders[category] = 1
    # Convert categories dictionary to lists for use in chart
    monthly_order_labels = list(monthly_orders.keys())
    monthly_order_quantities = list(monthly_orders.values())




    #for product total quantity maintaining their expiry date
    product_quantity_dict = {}
    for product in products:
        if product.name in product_quantity_dict:
            product_quantity_dict[product.name.upper()] += product.quantity
        else:
            product_quantity_dict[product.name.upper()] = product.quantity

    # create separate lists for product names and total quantities
    product_names = []
    total_quantities = []
    critical_product_names = []
    critical_product_quantity = []
    for product_name, total_quantity in product_quantity_dict.items():
        product_names.append(product_name)
        total_quantities.append(total_quantity)
        # if total quantity is less than 100 add product and its quantity in critical quantity list
        if total_quantity < 30:
            critical_product_names.append(product_name)
            critical_product_quantity.append(total_quantity)
    # filter all products whose is_available is false
    sold_products = Product.objects.filter(is_available=False)

    # filter the delivered orders
    delivered_orders = Order.objects.filter(is_delivered=True)

    #for calcualting the revenue  through multiplying the order quantity with the price of the product
    monthly_revenue = {}
    for order in delivered_orders:
        category = order.date.strftime("%B")
        if category in monthly_revenue:
            monthly_revenue[category] += order.product.product_price * order.quantity
        else:
            monthly_revenue[category] = order.product.product_price * order.quantity
    # Convert categories dictionary to lists for use in chart
    monthly_revenue_labels = list(monthly_revenue.keys())
    monthly_revenue_quantities = list(monthly_revenue.values())
    
    #find the total stock quantity by adding the quantity of all products that are available
    





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

    

    colors = [
    'rgba(255, 99, 132, 1)',
    'rgba(54, 162, 235, 1)',
    'rgba(255, 206, 86, 1)',
    'rgba(75, 192, 192, 1)',
    'rgba(153, 102, 255, 1)',
    'rgba(255, 159, 64, 1)',
    'rgba(255, 99, 132, 0.5)',
    'rgba(54, 162, 235, 0.5)',
    'rgba(255, 206, 86, 0.5)',
    'rgba(75, 192, 192, 0.5)',
    'rgba(153, 102, 255, 0.5)',
    'rgba(255, 159, 64, 0.5)',
    'rgba(255, 99, 132, 0.75)',
    'rgba(54, 162, 235, 0.75)',
    'rgba(255, 206, 86, 0.75)',
    'rgba(75, 192, 192, 0.75)',
    'rgba(153, 102, 255, 0.75)',
    'rgba(255, 159, 64, 0.75)',
    'rgba(255, 99, 132, 0.25)',
    'rgba(54, 162, 235, 0.25)',
    'rgba(255, 206, 86, 0.25)',
    'rgba(75, 192, 192, 0.25)',
    'rgba(153, 102, 255, 0.25)',
    'rgba(255, 159, 64, 0.25)',
    'rgba(255, 99, 132, 0.9)',
    'rgba(54, 162, 235, 0.9)',
    'rgba(255, 206, 86, 0.9)',
    'rgba(75, 192, 192, 0.9)',
    'rgba(153, 102, 255, 0.9)',
    'rgba(255, 159, 64, 0.9)',
    'rgba(255, 99, 132, 0.1)',
    'rgba(54, 162, 235, 0.1)',
    'rgba(255, 206, 86, 0.1)',
    'rgba(75, 192, 192, 0.1)',
    'rgba(153, 102, 255, 0.1)',
    'rgba(255, 159, 64, 0.1)',
    'rgba(255, 99, 132, 0.8)',
    'rgba(54, 162, 235, 0.8)',
    'rgba(255, 206, 86, 0.8)',
    'rgba(75, 192, 192, 0.8)',
    'rgba(153, 102, 255, 0.8)',
    'rgba(255, 159, 64, 0.8)',
    'rgba(255, 99, 132, 0.3)',
    'rgba(54, 162, 235, 0.3)',
    ]



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
        'formatted_order_count':formatted_order_count,
        'formatted_product_count':formatted_product_count,
        'formatted_staff_count':formatted_staff_count,
        'category_labels': category_labels,
        'category_quantities': category_quantities,
        'order_labels': order_labels,
        'order_quantities': order_quantities,
        'orderer_labels': orderer_labels,
        'orderer_quantities': orderer_quantities,
        'product_names': product_names,
        'total_quantities': total_quantities,
        'product_most_orders_names':product_most_orders_names,
        'product_most_orders_data':product_most_orders_data,
        'critical_product_names':critical_product_names,
        'critical_product_quantity':critical_product_quantity,
        'colors':colors,
        'monthly_order_labels':monthly_order_labels,
        'monthly_order_quantities':monthly_order_quantities,
        'monthly_revenue_labels':monthly_revenue_labels,
        'monthly_revenue_quantities':monthly_revenue_quantities,
        'total_stock_quantity':total_stock_quantity,
    }
    return render(request, 'dashboard/analytics.html',context)



@login_required
def staff(request):
    workers = User.objects.all()
    order_count = Order.objects.all().count()
    product_count = Product.objects.all().count()
    staff_count = User.objects.all().count()
     # format these counts with commas to separate thousands
    formatted_order_count = '{:,}'.format(order_count)
    formatted_product_count = '{:,}'.format(product_count)
    formatted_staff_count = '{:,}'.format(staff_count)
    total_stock_quantity = 0
    for product in products:
        total_stock_quantity += product.quantity
    total_stock_quantity = '{:,}'.format(total_stock_quantity)
    


    context = {
        'workers': workers,
        'product_count':product_count,
        'staff_count':staff_count,
        'order_count':order_count,
        'formatted_order_count':formatted_order_count,
        'formatted_product_count':formatted_product_count,
        'formatted_staff_count':formatted_staff_count,
        'total_stock_quantity':total_stock_quantity,
    }
    return render(request, 'dashboard/staff.html', context)


@login_required
def staff_update(request, pk):
    order_count = Order.objects.all().count()
    product_count = Product.objects.all().count()
    staff_count = User.objects.all().count()
    products = Product.objects.all()
     # format these counts with commas to separate thousands
    formatted_order_count = '{:,}'.format(order_count)
    formatted_product_count = '{:,}'.format(product_count)
    formatted_staff_count = '{:,}'.format(staff_count)
    total_stock_quantity = 0
    for product in products:
        total_stock_quantity += product.quantity
    total_stock_quantity = '{:,}'.format(total_stock_quantity)
    worker = User.objects.get(id = pk)
    
    context = {
        'worker': worker,
        'product_count':product_count,
        'staff_count':staff_count,
        'order_count':order_count,
        'formatted_order_count':formatted_order_count,
        'formatted_product_count':formatted_product_count,
        'formatted_staff_count':formatted_staff_count,
        'total_stock_quantity':total_stock_quantity,
    }

    return render(request, 'dashboard/staff_update.html', context)



@login_required
def product(request):
    order_count = Order.objects.all().count()
    product_count = Product.objects.all().count()
    staff_count = User.objects.all().count()
     # format these counts with commas to separate thousands
    formatted_order_count = '{:,}'.format(order_count)
    formatted_product_count = '{:,}'.format(product_count)
    formatted_staff_count = '{:,}'.format(staff_count)
    products = Product.objects.all()
    total_stock_quantity = 0
    for product in products:
        total_stock_quantity += product.quantity
    total_stock_quantity = '{:,}'.format(total_stock_quantity)
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
        'formatted_order_count':formatted_order_count,
        'formatted_product_count':formatted_product_count,
        'formatted_staff_count':formatted_staff_count,
        'total_stock_quantity':total_stock_quantity,
    }
    return render(request, 'dashboard/product.html',context)

@login_required
def stock(request):
    order_count = Order.objects.all().count()
    product_count = Product.objects.all().count()
    staff_count = User.objects.all().count()
     # format these counts with commas to separate thousands
    formatted_order_count = '{:,}'.format(order_count)
    formatted_product_count = '{:,}'.format(product_count)
    formatted_staff_count = '{:,}'.format(staff_count)
    products = Product.objects.all()
    total_stock_quantity = 0
    for product in products:
        total_stock_quantity += product.quantity
    total_stock_quantity = '{:,}'.format(total_stock_quantity)
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
        'formatted_order_count':formatted_order_count,
        'formatted_product_count':formatted_product_count,
        'formatted_staff_count':formatted_staff_count,
        'total_stock_quantity':total_stock_quantity,
    }
    return render(request, 'dashboard/stock.html',context)



@login_required    
def product_delete(request,pk):
    item = Product.objects.get(id = pk)
    order_count = Order.objects.all().count()
    product_count = Product.objects.all().count()
    staff_count = User.objects.all().count()
        # format these counts with commas to separate thousands
    formatted_order_count = '{:,}'.format(order_count)
    formatted_product_count = '{:,}'.format(product_count)
    formatted_staff_count = '{:,}'.format(staff_count)
    products = Product.objects.all()
    total_stock_quantity = 0
    for product in products:
        total_stock_quantity += product.quantity
    total_stock_quantity = '{:,}'.format(total_stock_quantity)
    #remove the object with product_id equal to pk"""

    if (request.method == 'POST'):
        item.delete()
        return redirect('dashboard-product')
    context={
        'formatted_order_count':formatted_order_count,
        'formatted_product_count':formatted_product_count,
        'formatted_staff_count':formatted_staff_count,
        'total_stock_quantity':total_stock_quantity,
       
    }
    return render(request, 'dashboard/product_delete.html', context)

    
@login_required    
def product_update(request,pk):
    order_count = Order.objects.all().count()
    product_count = Product.objects.all().count()
    staff_count = User.objects.all().count()
     # format these counts with commas to separate thousands
    formatted_order_count = '{:,}'.format(order_count)
    formatted_product_count = '{:,}'.format(product_count)
    formatted_staff_count = '{:,}'.format(staff_count)
    products = Product.objects.all()
    total_stock_quantity = 0
    for product in products:
        total_stock_quantity += product.quantity
    total_stock_quantity = '{:,}'.format(total_stock_quantity)
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
        'formatted_order_count':formatted_order_count,
        'formatted_product_count':formatted_product_count,
        'formatted_staff_count':formatted_staff_count,
        'total_stock_quantity':total_stock_quantity,
    }
    return render(request, 'dashboard/product_update.html', context)

    
@login_required    
def order(request):
    order_count = Order.objects.all().count()
    product_count = Product.objects.all().count()
    staff_count = User.objects.all().count()
     # format these counts with commas to separate thousands
    formatted_order_count = '{:,}'.format(order_count)
    formatted_product_count = '{:,}'.format(product_count)
    formatted_staff_count = '{:,}'.format(staff_count)
    products = Product.objects.all()
    total_stock_quantity = 0
    for product in products:
        total_stock_quantity += product.quantity
    total_stock_quantity = '{:,}'.format(total_stock_quantity)
    orders = Order.objects.all()
    context={
        'orders':orders,
        'product_count':product_count,
        'staff_count':staff_count,
        'order_count':order_count,
        'formatted_order_count':formatted_order_count,
        'formatted_product_count':formatted_product_count,
        'formatted_staff_count':formatted_staff_count,
        'total_stock_quantity':total_stock_quantity,

    }
    return render(request, 'dashboard/order.html', context)