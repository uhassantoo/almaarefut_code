from django.contrib import admin
from django.utils.translation import gettext as _

from .models import (Order, OrderItem, OrderItemAttribute)
from store.models import Product


# Order Items Model
class OrderItemAttributeInline(admin.TabularInline):
	model = OrderItemAttribute
	fk_name = 'order_item'
	verbose_name = _("Order Item Attribute")
	verbose_name_plural = _("Order Item Attributes")

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
	inlines = [OrderItemAttributeInline,]
	list_filter = ('item', 'order', 'order__id')
	list_display = ('item', 'order', 'quantity', 'is_cancelled')


class OrderItemInline(admin.TabularInline):
	model = OrderItem
	fk_name = 'order'
	verbose_name = _("Order Item")
	verbose_name_plural = _("Order Items")


# Order Model
@admin.register(Order)
class OrderAdmin (admin.ModelAdmin):
	inlines = [OrderItemInline,]
	list_display = ('user', 'total_payment', 'is_cancelled', 'paid', 'delivered', 'order_status', 'delivery_status', 'order_created', 'order_updated', 'delivered_date')
	list_filter = ('user', 'paid', 'items', 'delivered', 'order_created', 'order_status', 'delivery_status', 'delivered_date')
	list_editable = ['paid', 'order_status', 'delivery_status', 'delivered']
	empty_value_display = '-empty-'