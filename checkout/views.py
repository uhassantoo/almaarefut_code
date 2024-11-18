from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.contrib import messages

from address.forms import BillingForm
from address.models import BillingAddress
from address.billingaddress import Billing

from .models import DeliveryOptions
from basket.basket import Basket


def CheckoutView(request):
	"""
	Order checkout to add address.
	"""
	billing_session = Billing(request)
	basket = Basket(request)
	basketqty = basket.__len__()
	if basketqty <= 0:
		messages.error(request, "Your basket is empty.")
		return redirect("store:index")

	delivery_options = DeliveryOptions.objects.filter(is_active=True)
	print("Session contents:", dict(request.session))

	if request.POST:
		if request.user.is_authenticated:
			try:
				billing = BillingAddress.objects.get(
					customer=request.user, default=True
				)
				bform = BillingForm(request.POST, instance=billing)
			except ObjectDoesNotExist:
				bform = BillingForm(request.POST)

			if bform.is_valid():
				if bform.cleaned_data["save_info"]:
					billingsave = bform.save(commit=False)
					billingsave.customer = request.user
					billingsave.default = True
					billingsave.save()
				billing_session.add(bform, request.user.id)
			else:
				return render(request, "checkout/checkout.html", {"form": bform, 'delivery_options': delivery_options})
		else:
			bform = BillingForm(request.POST)
			if bform.is_valid():
				billing_session.add(bform, "Anonymous")
			else:
				return render(request, "checkout/checkout.html", {"form": bform, 'delivery_options': delivery_options})

		return HttpResponseRedirect(reverse("order:order-placement"))
	else:
		if request.user.is_authenticated:
			try:
				address = BillingAddress.objects.get(
					customer=request.user, default=True
				)
				return render(
					request, "checkout/checkout.html", {"address": address, 'delivery_options': delivery_options}
				)

			except ObjectDoesNotExist:
				bform = BillingForm(
					initial={
						"first_name": request.user.first_name,
						"last_name": request.user.last_name,
						"email": request.user.email,
					}
				)
		elif billing_session.__len__() != 0:
			billing_address = billing_session.billing_address["Anonymous"]
			bform.initial = {
				"first_name": billing_address["first_name"],
				"last_name": billing_address["last_name"],
				"email": billing_address["email"],
				"phone_number": billing_address["phone_number"],
				"address_line_1": billing_address["address_line_1"],
				"address_line_2": billing_address["address_line_2"],
				"city": billing_address["city"],
				"state": billing_address["state"],
				"country": billing_address["country"],
				"zip_code": billing_address["zip_code"],
			}
		else:
			bform = BillingForm()
		
		return render(request, "checkout/checkout.html", {"form": bform, 'delivery_options': delivery_options})


def UpdateDeliveryChargesInBasket(request):
	basket = Basket(request)

	if request.POST.get('action') == 'post':
		delivery_option_id = int(request.POST.get('delivery_option_id'))
		city = request.POST.get('city')
		delivery_option = DeliveryOptions.objects.get(id=delivery_option_id)

		if city == 'lhr':
			dc = delivery_option.within_city_dc
		else:
			dc = delivery_option.other_city_dc

		basket.add_delivery_charges(dc)
		
		response = JsonResponse({'dc': dc, 'total_price': basket.get_total_price()})
		return response

