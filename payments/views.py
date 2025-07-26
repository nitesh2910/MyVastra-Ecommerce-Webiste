import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.views import View
from cart.models import Cart
from products.models import Product

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(View):
    def get(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, id=product_id)

        YOUR_DOMAIN = "http://127.0.0.1:9000"

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'inr',
                            'unit_amount': int(product.price * 100),  # Convert ₹ to paise
                            'product_data': {
                                'name': product.name,
                            },
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + '/payments/success/',
                cancel_url=YOUR_DOMAIN + '/payments/cancel/',
            )
            return redirect(checkout_session.url)
        except Exception as e:
            return JsonResponse({'error': str(e)})
        

class CartCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        YOUR_DOMAIN = "http://127.0.0.1:9000"

        try:
            user = request.user
            cart_items = Cart.objects.filter(user=user)

            if not cart_items.exists():
                return JsonResponse({'error': 'Cart is empty'}, status=400)

            line_items = []
            for item in cart_items:
                line_items.append({
                    'price_data': {
                        'currency': 'inr',
                        'unit_amount': int(item.product.price * 100),
                        'product_data': {
                            'name': item.product.name,
                        },
                    },
                    'quantity': item.quantity,
                })

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=YOUR_DOMAIN + '/payments/success/',
                cancel_url=YOUR_DOMAIN + '/payments/cancel/',
            )
            return redirect(checkout_session.url)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)