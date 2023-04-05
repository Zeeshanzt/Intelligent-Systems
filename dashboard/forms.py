from .models import Product,Order
from django import forms

class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = ['name', 'category','quantity','product_id','expiration_date','manufacturer_name','product_price']

class OrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ['product','quantity']
