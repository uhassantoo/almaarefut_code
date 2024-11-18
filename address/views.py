from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import (render, redirect)

from .billingaddress import Billing
from .forms import UserAddressForm
from .models import BillingAddress


def AddressView(request):
	return BillingAddress.objects.filter(customer=request.user)

@login_required
def AddressSessionView(request):
	billing_session = Billing(request)
	if request.POST.get('action') == 'post':
		address = BillingAddress.objects.get(customer=request.user, default=True)
		billing_session.addBillingObject(address=address, uid=request.user.id)
	response = JsonResponse('successfully added address', safe=False)
	return response

@login_required
def AddressListView(request):
	addresses = BillingAddress.objects.filter(customer=request.user)
	return render(request, "address/addresses.html", {
		'addresses': addresses,
	})

@login_required
def add_address(request):
	if request.POST:
		address_form = UserAddressForm(request.POST)
		if address_form.is_valid():
			address_form = address_form.save(commit=False)
			address_form.customer = request.user
			address_form.default = True
			address_form.save()
			messages.success(request, 'New Delivery Address has been added')
			return redirect('address:addresses')
		else:
			return render(request, 'address/add', {
				'form': address_form
			})

	address_form = UserAddressForm()
	return render(request, 'address/add.html', {
		'form': address_form
	})

@login_required
def edit_address(request, id):
	address = BillingAddress.objects.get(pk=id, customer=request.user)
	if request.POST:
		address_form = UserAddressForm(request.POST, instance=address)
		if address_form.is_valid():
			address_form.save()
			return redirect('address:addresses')
		else:
			return render(request, 'address/add', {
				'form': address_form
			})

	address_form = UserAddressForm(instance=address)
	return render(request, 'address/add.html', {
		'form': address_form
	})

@login_required
def delete_address(request, id):
	try:
		BillingAddress.objects.get(pk=id, customer=request.user).delete()
		messages.success(request, 'Address successfully deleted.')
	except ObjectDoesNotExist:
		messages.error(request, 'Address doesn\'t exist.')
	return redirect('address:addresses')


@login_required
def default_address(request, id):
	try:
		address = BillingAddress.objects.get(pk=id, customer=request.user)
		BillingAddress.objects.filter(customer=request.user).update(default=False)
		address.default = True
		address.save()
	except ObjectDoesNotExist:
		messages.error(request, 'Error: Address doesn\'t exist.')
	return redirect('address:addresses')
