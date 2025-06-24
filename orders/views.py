from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from .forms import OrderForm
from .models import Order, OrderItem
from products.models import Product
from .utils import generate_invoice

# Checkout View
@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
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
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = total_price
            order.save()

            # Create OrderItems
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['product'].price
                )

            # Clear the session cart
            request.session['cart'] = {}

            return redirect('order_success')
    else:
        form = OrderForm()

    return render(request, 'orders/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price,
    })

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
