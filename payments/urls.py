from django.urls import path
from .views import CreateCheckoutSessionView, CartCheckoutSessionView
from django.views.generic import TemplateView
from orders.views import stripe_payment_success 
urlpatterns = [
    path('buy-now/<int:product_id>/', CreateCheckoutSessionView.as_view(), name='buy_now_checkout'),
    path('cart-checkout/', CartCheckoutSessionView.as_view(), name='cart_checkout'),
    path('success/', stripe_payment_success, name='payment-success'),
    # path('success/', TemplateView.as_view(template_name="payments/payment_success.html"), name='payment-success'),
    path('cancel/', TemplateView.as_view(template_name="payments/payment_cancel.html"), name='payment-cancel'),
]
