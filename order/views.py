from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import (
	redirect,
	render,
	get_object_or_404,
)
from django.contrib.auth.decorators import login_required

from .models import Order, OrderItem, OrderItemAttribute

from store.models import Product, ProductSpecificationValue

from address.billingaddress import Billing

from basket.basket import Basket


def Order_placement(request):
	"""
	Orders and Orderitems are fetched from basket_session if exist, and are stored in actual order and orderitem models respectively.
	Then if billing address exists in databases, then it's attached to the order otherwise billing address details are fetched from billing_session and stored respectively in order.
	At last basket_session is cleared but not billing_session so can be used next time the user places order(s)
	"""
	basket_session = Basket(request)
	basketqty = basket_session.__len__()
	if basketqty <= 0:
		messages.error(request, "Your basket is empty.")
		return redirect("store:index")

	billing_session = Billing(request)
	if billing_session.__len__() != 0:
		billing_address = billing_session.billing_address[
			str(request.user.id) if request.user.is_authenticated else "Anonymous"
		]
	else:
		messages.error(request, "You have not filled billing details")
		return redirect("checkout:checkout")

	order = Order.objects.create(
		user=request.user if request.user.is_authenticated else None,
		total_payment=basket_session.get_total_price(),
	)
	order.phone_number = billing_address["phone_number"]
	order.address_line_1 = billing_address["address_line_1"]
	order.address_line_2 = billing_address["address_line_2"]
	order.city = billing_address["city"]
	order.state = billing_address["state"]
	order.country = billing_address["country"]
	order.zip_code = billing_address["zip_code"]
	order.first_name = billing_address["first_name"]
	order.last_name = billing_address["last_name"]
	order.email = billing_address["email"]

	order.save()

	for item in basket_session:
		prdt = get_object_or_404(Product, id=item["product"].get("id"))
		order_item = OrderItem.objects.create(
			item=prdt,
			order=order,
			quantity=item["qty"],
		)
		key = item['product'].get('key').split('-')[1:]
		attributes = ProductSpecificationValue.objects.filter(id__in=key)
		if attributes.exists():
			for attribute in attributes:
				OrderItemAttribute.objects.create(order_item=order_item, attribute=attribute)
		# order.items.add(order_item)

	basket_session.clear()

	messages.success(
		request, "Thanks for shopping! Your order has been placed successfully."
	)
	return redirect("store:index")


@login_required
def remove_from_cart(request, slug):
	item = get_object_or_404(Product, slug=slug)
	order_qs = Order.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		# check if the order item is in the order
		if order.items.filter(item__slug=item.slug).exists():
			order_item = OrderItem.objects.filter(
				item=item, user=request.user, ordered=False
			)[0]
			order_item.quantity = 1
			order_item.save()
			order.items.remove(order_item)
			messages.success(
				request, f"{order_item.item.title} item was removed from your cart."
			)
		else:
			# add a message saying the user doesn't have an order
			messages.error(request, "This item was not in your cart.")
			return redirect("order:product", slug=slug)

	else:
		# add a message saying the user doesn't have an order
		messages.error(request, "You do not have an active order.")
		return redirect("order:product", slug=slug)
	return redirect("order:order-summary")


@login_required
def orders_history(request):
	orders = Order.objects.filter(user=request.user.id)
	return render(request, 'order/orders_history.html', {
		'orders': orders
	})


@login_required
def order_cancel(request):
	"""
	Cancel Order using order_id if time_stamp is within one day i.e., on the same day order was created
	"""
	if request.POST.get('action') == 'cancel':
		order_id = request.POST.get('order_id')
		order = Order.objects.get(pk=order_id)
		order.is_cancelled = True
		order.order_status = 'C'
		order.save()
		response = JsonResponse({'message': 'Order has been successfully cancelled', 'order_status': order.get_order_status_display()})
	return response


@login_required
def order_item_remove(request):
	"""
	Remove Order Item using item_id if time_stamp is within one day i.e., on the same day order was created
	"""
	if request.POST.get('action') == 'remove':
		item_id = request.POST.get('item_id')
		orderitem = OrderItem.objects.get(pk=item_id)
		orderitem.is_cancelled = True
		orderitem.save()

		order = Order.objects.get(order_items=orderitem)
		order_item_objects = OrderItem.objects.filter(order=order, is_cancelled=False)
		if not order_item_objects.exists():
			order.is_cancelled = True
			order.order_status = 'C'
			order.save()
		response = JsonResponse({'message': 'Order item has been successfully remove', 'cancelled': order.is_cancelled})

		return response