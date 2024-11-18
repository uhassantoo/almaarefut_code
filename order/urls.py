from django.urls import path

from . import views

app_name = 'order'

urlpatterns = [
	path('remove-from-cart/<slug>/', views.remove_from_cart, name='remove-from-cart'),
	path('order_placement/', views.Order_placement, name='order-placement'),
	# orders history
	path('orders-history/', views.orders_history, name="orders-history"),
	# order cancel
	path('cancel-order/', views.order_cancel, name='order-cancel'),
	# order item cancel/remove
	path('order-item-remove/', views.order_item_remove, name='order-item-remove'),
]