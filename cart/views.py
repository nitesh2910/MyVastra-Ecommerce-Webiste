from django.shortcuts import render,redirect,get_object_or_404
from .models import Cart
from products.models import Product
from django.views.decorators.http import require_POST
# Create your views here.

def add_to_cart(request, productid):
    cart = request.session.get('cart', {})
    cart[str(productid)] = cart.get(str(productid), 0) + 1
    request.session['cart'] = cart
    return redirect('cart_detail')


def cart_detail(request):
    cart = request.session.get('cart', {})
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
    
    return render(request, 'cart/cart_detail.html', {
        'cart_items' : cart_items,
        'total_price': total_price
    })
    
def remove_from_cart(request, productid):
    cart = request.session.get('cart', {})
    
    if str(productid) in cart:
        del cart[str(productid)]
        request.session['cart'] = cart
        
    return redirect('cart_detail')

@require_POST
def update_cart(request):
    cart = request.session.get('cart', {})
    for product_id, quantity in request.POST.items():
        if product_id.startswith('qty_'):
            pid = product_id.replace('qty_', '')
            try:
                qty = int(quantity)
                if qty > 0:
                    cart[pid] = qty
                else:
                    cart.pop(pid, None)
            except ValueError:
                continue
    
    request.session['cart'] = cart
    return redirect('cart_detail')