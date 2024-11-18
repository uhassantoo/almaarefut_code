from django.conf import settings
import json

from store.models import (Product, ProductSpecificationValue)



class Basket():
	"""
	A base Basket class, providing some default behaviors that can be inherited or overrided, as necessary.
	"""

	def __init__(self, request):
		self.session = request.session
		basket = self.session.get(settings.BASKET_SESSION_ID)
		delivery_charges = self.session.get(settings.DELIVERY_CHARGES_SESSION_ID)

		if settings.BASKET_SESSION_ID not in request.session:
			basket = self.session[settings.BASKET_SESSION_ID] = {}
		self.basket = basket

		if settings.DELIVERY_CHARGES_SESSION_ID not in request.session:
			delivery_charges = self.session[settings.DELIVERY_CHARGES_SESSION_ID] = {}
		self.delivery_charges = delivery_charges

	def add(self, product, qty, attributes):
		"""
		Adding and updating the users basket session data
		"""
		product_id = str(product.id)
		if attributes:
			for id in attributes:
				product_id += '-' + id

		if product.discount_price:
			discount_price = float(product.discount_price)
		else:
			discount_price = ''
		if product_id not in self.basket:
			self.basket[product_id] = {
				'regular_price': float(product.regular_price),
				'discount_price': discount_price,
				'qty': int(qty),
			}
		else:
			self.basket[product_id]['qty'] = int(self.basket[product_id]['qty']) + int(qty)

		self.save()
	
	def add_delivery_charges(self, dc):
		"""
		Add delivery charges for within or outside of city
		"""
		self.delivery_charges['DC'] = str(dc)
		self.save()

	def update(self, item_key, qty):
		"""
		Updating the users basket session data
		"""

		if item_key in self.basket:
			self.basket[item_key]['qty'] = int(qty)

		self.save()

	def delete(self, item_key):
		"""
		Deleting and updating the users basket session data
		"""
		if item_key in self.basket:
			del self.basket[item_key]
			self.save()

	def serialize_product(self, product, attributes, key):
		"""
		Convert the Product object to a dictionary
		"""
		try:
			return {
				'id': product.id,
				'title': product.title,
				'description': product.description,
				'image': product.images.first().image.url if product.images.exists() else None,
				'attributes': {key.specification.name: key.value for key in attributes},
				'get_absolute_url': product.get_absolute_url(),
				'key': key
			}
		except AttributeError as e:
			# Log the error
			print(f"Error serializing product {getattr(product, 'id', 'None')}: {str(e)}")
			# Return a minimal dict to avoid breaking the basket
			return {
				'id': getattr(product, 'id', None),
				'title': 'Product unavailable',
				'key': key
			}

	def __iter__(self):
		"""
		Collect the product_id in the session data to query the database and return products
		"""
		dict_keys: dict = self.basket.keys()
		product_ids: list = [pid.split('-')[0] for pid in dict_keys]
		products: Product = Product.products.filter(id__in=product_ids)
		product_dict: dict = {str(product.id): product for product in products}

		basket: dict = self.basket.copy()

		keys_to_delete: list = []

		for key in dict_keys:
			ids = key.split('-')
			product_id = ids[0]
			product = product_dict.get(product_id, None)
			print(product)

			attribute_ids = ids[1:]
			attributes = ProductSpecificationValue.objects.filter(id__in=attribute_ids)

			basket[str(key)]['product'] = self.serialize_product(product, attributes, key)

			if basket[str(key)]['product']['id'] is None:
				print(basket[str(key)]['product'])
				keys_to_delete.append(key)
		
		for key in keys_to_delete:
			self.delete(key)

		for item in basket.values():
			item['total_price'] = item['regular_price'] * item['qty']
			yield item

	def __len__(self):
		"""
		Get the basket data and count the qty of items
		"""
		return sum(item['qty'] for item in self.basket.values())

	def get_discount_price(self):
		return float(self.get_before_discount_subtotal_price()) - float(self.get_after_discount_subtotal_price())

	def get_before_discount_subtotal_price(self):
		return sum(item['regular_price'] * item['qty'] for item in self.basket.values())

	def get_after_discount_subtotal_price(self):
		return sum(item['discount_price'] * item['qty'] if item['discount_price'] != '' else item['regular_price'] * item['qty'] for item in self.basket.values())

	def get_total_price(self):
		return self.get_after_discount_subtotal_price() + float(self.delivery_charges.get('DC', 0))

	def save(self):
		self.session.modified = True

	def clear(self):
		del self.session[settings.BASKET_SESSION_ID]
		del self.session['delivery_charges']
		self.save()