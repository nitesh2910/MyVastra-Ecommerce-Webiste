from django.contrib import admin
from .models import Cart
# Register your models here.

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'added_at')
    list_filter = ('user', )
    search_fields = ('product__name', )