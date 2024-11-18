from django.db import models
from django.utils.translation import gettext_lazy as _


class DeliveryOptions(models.Model):
	"""
	The Delivery methods table containing all delivery
	"""

	delivery_name = models.CharField(help_text=_('Required - e.g., Standard Delivery or Express Delivery e.t.c.'), max_length=255)
	within_city_dc = models.DecimalField(verbose_name=_("Within City Delivery Charges"), max_digits=5, decimal_places=2, help_text=_("Price must be between 0 and 999.99"))
	other_city_dc = models.DecimalField(verbose_name=_("Other Cities Delivery Charges"), max_digits=5, decimal_places=2, help_text=_("Price must be between 0 and 999.99"))
	delivery_timeframe = models.CharField(verbose_name=_("Delivery Time-Frame"), help_text=_("Required - e.g., '3-4 days'"), max_length=255)
	delivery_window = models.CharField(verbose_name=_("Delivery Window"), help_text=_("Required - e.g., '9:00am - 5:00pm'"), max_length=255)
	order = models.IntegerField(verbose_name=_("Delivery Option Order Number"), help_text=_("Required - Order number of which it should be displayed in delivery option list on checkout page"), default=0)
	is_active = models.BooleanField(default=True)

	class Meta:
		verbose_name = ("Delivery Option")
		verbose_name_plural = ("Delivery Options")
		ordering = (('order'),)
	
	def __str__(self):
		return self.delivery_name
