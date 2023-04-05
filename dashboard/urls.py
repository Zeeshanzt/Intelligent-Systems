from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.index, name = 'dashboard-home'),
    path('staff/', views.staff, name = 'dashboard-staff'),
    path('staff/update/<int:pk>', views.staff_update, name = 'dashboard-staff-update'),
    path('product/', views.product, name = 'dashboard-product'),
    path('product/delete/<int:pk>', views.product_delete, name = 'dashboard-product-delete'),
    path('product/update/<int:pk>', views.product_update, name = 'dashboard-product-update'),
    path('order/', views.order, name = 'dashboard-order'),    
    path('process_images/', views.process_images, name='dashboard-process-images'),
    # path('display_images/', views.display_images, name='dashboard-display-images'),
]
