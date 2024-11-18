import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django.conf import settings


class BillingAddress (models.Model):
	CITY_CHOICES = (
		("", "City"),
		("abd", "Attock"),
		("abt", "Abbottabad"),
		("bhr", "Bahawalnagar"),
		("bwn", "Bhawana"),
		("bhk", "Bhakkar"),
		("bwp", "Bahawalpur"),
		("cwp", "Chishtian"),
		("dgh", "Dera Ghazi Khan"),
		("dnb", "Dinawali"),
		("dip", "Dipalpur"),
		("fdr", "Fateh Jhang"),
		("fsl", "Faisalabad"),
		("ghk", "Gujar Khan"),
		("gjr", "Gujranwala"),
		("grk", "Gwadar"),
		("grw", "Gujranwala"),
		("gjr", "Gujrat"),
		("hyd", "Hyderabad"),
		("isl", "Islamabad"),
		("jlm", "Jalalpur"),
		("jwn", "Jaranwala"),
		("jwp", "Jhelum"),
		("khr", "Khairpur"),
		("khi", "Karachi"),
		("khr", "Khanewal"),
		("ktt", "Kotli"),
		("kwb", "Kot Adu"),
		("lai", "Lalamusa"),
		("lhr", "Lahore"),
		("ldr", "Lodhran"),
		("lrd", "Larkana"),
		("ltr", "Layyah"),
		("mll", "Mian Channu"),
		("mlk", "Malakwal"),
		("mlt", "Mardan"),
		("mrd", "Multan"),
		("mnt", "Mansehra"),
		("mgw", "Mandi Bahauddin"),
		("mwm", "Mianwali"),
		("mtr", "Multan"),
		("mzt", "Murree"),
		("mzw", "Muzaffargarh"),
		("ngt", "Narowal"),
		("nwn", "Nankana Sahib"),
		("pwp", "Peshawar"),
		("phl", "Pattoki"),
		("qta", "Quetta"),
		("qrb", "Quetta Residency"),
		("rch", "Rajanpur"),
		("rnw", "Rawalpindi"),
		("rkn", "Rahim Yar Khan"),
		("rwp", "Rawalpindi"),
		("sgr", "Sargodha"),
		("skt", "Sialkot"),
		("shw", "Sheikhupura"),
		("swn", "Swat"),
		("sak", "Sargodha"),
		("sbq", "Sahiwal"),
		("ska", "Sakrand"),
		("skz", "Sukheki"),
		("stw", "Sialkot"),
		("suk", "Sukkur"),
		("swl", "Sahiwal"),
		("sgr", "Sargodha"),
		("swl", "Sialkot"),
		("saw", "Sawat"),
		("ttn", "Toba Tek Singh"),
		("vhn", "Vehari"),
		("wah", "Wah Cantt"),
		("wln", "Wazirabad"),
	)

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	# Customer
	customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("Customer"), blank=True, null=True)
	first_name = models.CharField(_("First Name"), max_length=150)
	last_name = models.CharField(_("Last Name"), max_length=150)
	email = models.EmailField()
	# Delivery Details
	phone_number = models.CharField(_("Phone Number"), max_length=15)
	address_line_1 = models.CharField(_("Address Line 1"), max_length=150)
	address_line_2 = models.CharField(_("Address Line 2"), max_length=150, blank=True)
	city = models.CharField(_("City"), choices=CITY_CHOICES, max_length=150)
	state = models.CharField(_("State/Province"), max_length=150)
	country = CountryField(_("Country"), blank_label='Country', default='PK')
	zip_code = models.CharField(_("Zip Code"), max_length=12)
	default = models.BooleanField(_("Default"), default=False)

	class Meta:
		verbose_name = 'Billing Address'
		verbose_name_plural = 'Billing Addresses'

	def __str__(self):
		return self.customer.username