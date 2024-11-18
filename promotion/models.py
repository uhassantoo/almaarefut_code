import uuid
from datetime import timezone

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Promotion(models.Model):
    # PERCENTAGE = 'percentage'
    # FIXED = 'fixed'
    # FREE_SHIPPING = 'free_shipping'
    # DISCOUNT_TYPE_CHOICES = [
    #     (PERCENTAGE, 'Percentage'),
    #     (FIXED, 'Fixed '),
    #     (FREE_SHIPPING, 'Free Shipping')
    # ]
    
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)
    name = models.CharField(max_length=255, help_text="Promotion name like 'Holiday Sale'.")
    description = models.TextField(blank=True, null=True)
    promo_type = models.ForeignKey('PromoType', on_delete=models.CASCADE)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, help_text="Discount value (amount or percentage).")
    start_date = models.DateTimeField(help_text="Promotion start date and time.")
    end_date = models.DateTimeField(help_text="Promotion end date and time.")
    is_active = models.BooleanField(default=True)
    
    def is_valid(self):
        """Check if the promotion is valid and active."""
        now = timezone.now()
        return self.is_active and self.start_date <= now <= self.end_date

    def __str__(self):
        return self.name


class PromoType(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name


# class PromotionUsage(models.Model):
#     promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     usage_count = models.IntegerField(default=0)


# class PromotionUser(models.Model):
#     promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


# class PromotionCategory(models.Model):
#     promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)
#     category = models.ForeignKey("store.Category", on_delete=models.CASCADE)


class PromotionProduct(models.Model):
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)
    product = models.ForeignKey("store.Product", on_delete=models.CASCADE)
    min_quantity = models.IntegerField(default=1, help_text=_("Minimum quantity for promotion"))

    class Meta:
        unique_together = ('promotion', 'product')


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True, help_text="Coupon code like 'SUMMER20'.")
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, related_name="coupons")
    # usage_limit = models.IntegerField(default=1, help_text="Maximum number of times the coupon can be used.")
    # times_used = models.IntegerField(default=0)
    user_restricted = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="coupons", help_text="If restricted to certain users.")
    expiration_date = models.DateTimeField(blank=True, null=True, help_text="Coupon expiration date.")
    is_active = models.BooleanField(default=True)

    def is_valid(self, user=None):
        """Check if the coupon is valid and hasn't expired or exceeded usage limits."""
        now = timezone.now()
        if self.expiration_date and now > self.expiration_date:
            return False
        # if self.times_used >= self.usage_limit:
        #     return False
        if not self.is_active:
            return False
        if user and self.user_restricted.exists() and user not in self.user_restricted.all():
            return False
        return True

    def __str__(self):
        return self.code
