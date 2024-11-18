from django.conf import settings


class Billing():
	"""
	A base billing class, providing some default behaviors that can be inherited or overrided, as necessary.
	"""

	def __init__(self, request):
		self.session = request.session
		billing_address = self.session.get(settings.BILLING_ADDRESS_SESSION_ID)

		if settings.BILLING_ADDRESS_SESSION_ID not in request.session:
			billing_address = self.session[settings.BILLING_ADDRESS_SESSION_ID] = {}
		self.billing_address = billing_address

	def add(self, bform, uid):
		"""
		Adding and updating the users billing session data via billing form
		"""
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

		self.billing_address[str(uid)] = {
			'first_name': bform.cleaned_data['first_name'],
			'last_name': bform.cleaned_data['last_name'],
			'email': bform.cleaned_data['email'],
			'phone_number': bform.cleaned_data['phone_number'],
			'address_line_1': bform.cleaned_data['address_line_1'],
			'address_line_2': bform.cleaned_data['address_line_2'],
			'city': dict(CITY_CHOICES).get(bform.cleaned_data['city']),
			'state': bform.cleaned_data['state'],
			'country': bform.cleaned_data['country'],
			'zip_code': bform.cleaned_data['zip_code'],
			'payment_method': bform.cleaned_data['payment_method'],
		}
		self.save()

	def addBillingObject(self, address, uid):
		"""
		Adding and updating the users billing session data via Billing object
		"""
		self.billing_address[str(uid)] = {
			'first_name': str(address.first_name),
			'last_name': str(address.last_name),
			'email': str(address.email),
			'phone_number': str(address.phone_number),
			'address_line_1': str(address.address_line_1),
			'address_line_2': str(address.address_line_2),
			'city': str(address.city),
			'state': str(address.state),
			'country': str(address.country),
			'zip_code': str(address.zip_code),
			'payment_method': 'COD'
		}
		self.save()

	def __len__(self):
		"""
		Returns true total number of addresses stored in billing_address session
		"""
		key = len(self.billing_address.keys())
		return key

	def save(self):
		self.session[settings.BILLING_ADDRESS_SESSION_ID] = self.billing_address
		self.session.modified = True

	def clear(self):
		del self.session[settings.BILLING_ADDRESS_SESSION_ID]
		self.save()