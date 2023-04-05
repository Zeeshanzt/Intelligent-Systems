from django.db import models
from django.contrib.auth.models import User


CATEGORY = (
('Electronics', 'Electronics'),
('Clothing and Apparel', 'Clothing and Apparel'),
('Home and Kitchen Appliances', 'Home and Kitchen Appliances'),
('Beauty and Personal Care Products', 'Beauty and Personal Care Products'),
('Food', 'Food'),
('Sporting Goods and Fitness Equipment', 'Sporting Goods and Fitness Equipment'),
('Automotive Parts and Accessories', 'Automotive Parts and Accessories'),
('Medical and Healthcare Supplies', 'Medical and Healthcare Supplies'),
('Office Supplies and Equipment', 'Office Supplies and Equipment'),
('Industrial and Construction Materials', 'Industrial and Construction Materials'),
)


class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY, null=True)
    quantity = models.PositiveIntegerField(null=True)
    product_id = models.CharField(max_length=50, null=True)
    manufacturing_date = models.DateField(null=True)
    expiration_date = models.DateField(null=True)
    manufacturer_name = models.CharField(max_length=100, null=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return f'{self.name}'

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    staff = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(null = True)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.product} ordered by {self.staff.username}'

    

