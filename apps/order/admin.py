from django.contrib import admin
from .models import *


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ('pk', 'user__id', 'user', 'address')

class OrderItemAdmin(admin.ModelAdmin):
    model = OrderItem
    list_display = ('pk', 'order__id', 'order', 'book', 'quantity', 'price_at_time')
    

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)