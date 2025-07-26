import stripe
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse, Http404
from .forms import OrderForm
from .models import Order, OrderItem
from products.models import Product
from .utils import generate_invoice
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY

# Checkout View
@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('cart_detail')

    cart_items = []
    total_price = 0

    for product_id, qty in cart.items():
        product = get_object_or_404(Product, id=product_id)
        item_total = product.price * qty
        total_price += item_total
        cart_items.append({
            'product': product,
            'quantity': qty,
            'item_total': item_total,
        })

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            request.session['order_data'] = form.cleaned_data

            line_items = []
            for item in cart_items:
                line_items.append({
                    'price_data': {
                        'currency': 'inr',
                        'unit_amount': int(item['product'].price * 100),
                        'product_data': {
                            'name': item['product'].name,
                        },
                    },
                    'quantity': item['quantity'],
                })

            try:
                YOUR_DOMAIN = 'http://127.0.0.1:9000'
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=line_items,
                    mode='payment',
                    success_url=YOUR_DOMAIN + '/payments/success/',
                    cancel_url=YOUR_DOMAIN + '/payments/cancel/',
                    metadata={
                        'user_id': str(request.user.id),
                    }
                )
                return redirect(checkout_session.url, code=303)

            except stripe.error.StripeError as e:
                messages.error(request, f"Stripe Error: {e.user_message or str(e)}")
            except Exception as e:
                messages.error(request, f"Something went wrong: {str(e)}")
        else:
            messages.warning(request, "Please correct the errors in the form.")
    else:
        form = OrderForm()

    return render(request, 'orders/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price,
    })
    
    
@login_required
def stripe_payment_success(request):
    try:
        cart = request.session.get('cart', {})
        order_data = request.session.get('order_data')

        if not cart or not order_data:
            messages.error(request, "Payment success, but no cart or order data found.")
            return redirect('product_list')

        cart_items = []
        total_price = 0

        for product_id, qty in cart.items():
            product = get_object_or_404(Product, id=product_id)
            item_total = product.price * qty
            total_price += item_total
            cart_items.append({
                'product': product,
                'quantity': qty,
                'item_total': item_total,
            })

        order = Order.objects.create(
            user=request.user,
            name=order_data['name'],
            phone=order_data['phone'],
            address=order_data['address'],
            total_price=total_price
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price
            )

        request.session['cart'] = {}
        request.session['order_data'] = {}

        messages.success(request, "Your order has been placed successfully!")
        return redirect('order_success')

    except Exception as e:
        messages.error(request, f"Something went wrong during order processing: {str(e)}")
        return redirect('product_list')


# Order Success Page
def order_success(request):
    return render(request, 'orders/order_success.html')


# User's Orders
@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-ordered_at')
    return render(request, 'orders/my_orders.html', {'orders': orders})


# Track Order (for logged-in users)
@login_required
def track_order(request):
    order = None
    not_found = False

    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        phone = request.POST.get('phone')

        try:
            order = Order.objects.get(id=order_id, phone=phone, user=request.user)
        except Order.DoesNotExist:
            not_found = True

    return render(request, 'orders/track_order.html', {
        'order': order,
        'not_found': not_found
    })

# PDF Invoice Download
@login_required
def download_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    buffer = generate_invoice(order)
    return FileResponse(buffer, as_attachment=True, filename=f'invoice_order_{order.id}.pdf')

# HTML Invoice View (for printing)
@login_required
def invoice_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/invoice_view.html', {'order': order})
