from django.contrib import admin
from django.urls import path
from django.http import FileResponse
from django.utils.html import format_html
from .models import Order, OrderItem
from .utils import generate_invoice  # Make sure this exists in orders/utils.py

# Inline to show Order Items in Order view
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'total_price', 'status', 'ordered_at', 'invoice_link')  # added invoice_link
    list_filter = ('status', 'ordered_at')
    search_fields = ('name', 'user__username', 'phone')
    inlines = [OrderItemInline]
    list_editable = ('status',)
    readonly_fields = ('total_price', 'ordered_at')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:order_id>/invoice/', self.admin_site.admin_view(self.download_invoice), name='order-invoice'),
        ]
        return custom_urls + urls

    def download_invoice(self, request, order_id):
        order = Order.objects.get(id=order_id)
        buffer = generate_invoice(order)
        return FileResponse(buffer, as_attachment=True, filename=f'invoice_order_{order.id}.pdf')

    def invoice_link(self, obj):
        return format_html(
            '<a class="button" href="{}">Download Invoice</a>',
            f'{obj.id}/invoice/'
        )
    invoice_link.short_description = 'Invoice'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('order__id', 'product__name')
    list_filter = ('product',)
