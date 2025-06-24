from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.order_success, name='order_success'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('track/', views.track_order, name='track_order'),
    path('invoice/<int:order_id>/', views.download_invoice, name='download_invoice'),
     path('invoice/view/<int:order_id>/', views.invoice_view, name='invoice_view'),
]
