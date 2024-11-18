import uuid
from django.conf import settings
from django_countries.fields import CountryField
from django.db import models
from django.utils import timezone

from store.models import Product, ProductSpecificationValue

# Create your models here.


class Order(models.Model):
	ORDER_STATUS_CHOICES = (
		("F", "Fullfilled"),
		("P", "In Process"),
		("C", "Is Cancelled"),
	)
	DELIVERY_STATUS_CHOICES = (
		("D", "Delivered"),
		("P", "In Process"),
		("C", "Is Cancelled"),
	)

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name="order",
		blank=True,
		null=True,
	)
	items = models.ManyToManyField("store.Product", through='OrderItem')

	# payment
	total_payment = models.DecimalField(max_digits=10, decimal_places=2)
	paid = models.BooleanField(default=False)
	PAYMENT_CHOICES = (("COD", "Cash on Delivery"),)
	payment = models.CharField(max_length=15, choices=PAYMENT_CHOICES, default="COD")

	# order
	order_created = models.DateTimeField(auto_now_add=True)
	order_updated = models.DateTimeField(auto_now=True)
	order_status = models.CharField(
		max_length=2, choices=ORDER_STATUS_CHOICES, default="P"
	)

	# cancel
	is_cancelled = models.BooleanField(default=False)

	# delivery
	delivery_status = models.CharField(
		max_length=2, choices=DELIVERY_STATUS_CHOICES, default="P"
	)
	delivered_date = models.DateTimeField(blank=True, null=True)
	delivered = models.BooleanField(default=False)

	# billing address details
	# required
	first_name = models.CharField(max_length=25)
	last_name = models.CharField(max_length=25)
	email = models.EmailField()
	# optional, that if billing address exits then no need to reenter data into these fields
	phone_number = models.CharField(max_length=15, blank=True, null=True)
	address_line_1 = models.CharField(max_length=150, blank=True, null=True)
	address_line_2 = models.CharField(max_length=150, blank=True, null=True)
	city = models.CharField(max_length=150, blank=True, null=True)
	state = models.CharField(max_length=150, blank=True, null=True)
	country = CountryField(blank_label="Country", blank=True, null=True)
	zip_code = models.CharField(max_length=12, blank=True, null=True)

	class Meta:
		ordering = ("-order_created",)
	
	def __str__(self):
		if self.user:
			f_name = self.user.first_name
			l_name = self.user.last_name
		else:
			f_name = self.first_name
			l_name = self.last_name
		order_placed = self.order_created.strftime("%I:%M %p | %d-%m-%Y")
		return f"{f_name} {l_name} | {order_placed}"

	def can_be_cancelled(self):
		return (timezone.now() - self.order_created).total_seconds() <= 12 * 60 *60



class OrderItem(models.Model):
	order = models.ForeignKey(
		Order,
		on_delete=models.CASCADE,
		related_name="order_items"
	)
	item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
	quantity = models.IntegerField(default=1)
	is_cancelled = models.BooleanField(default=False)

	def __str__(self):
		if self.is_cancelled:
			option = 'Cancelled'
		else:
			option = ', '.join(str(attr) for attr in self.order_item_attribute.all())
		return f"{self.order.id} ----- {self.quantity} of {self.item.title} ----- {option}"


class OrderItemAttribute(models.Model):
	order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name="order_item_attribute")
	attribute = models.ForeignKey(ProductSpecificationValue, on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.attribute.specification.name}: {self.attribute.value}'