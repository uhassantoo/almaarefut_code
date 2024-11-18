import logging
import json

from django.http import JsonResponse
from django.core.mail import send_mail
from django.views.generic import DetailView, ListView, TemplateView
from django.views.decorators.csrf import csrf_protect

from store.decorators import rate_limit
from store.forms import ContactForm

from .models import Product, Category, FeaturedCategory


logger = logging.getLogger(__name__)


class HomeView(TemplateView):
    template_name = 'store/index.html'


class AboutView(TemplateView):
    template_name = 'store/about_us.html'


class CategoryListView (ListView):
	model = Product
	paginate_by = 12
	template_name = 'store/products.html'

	def setup(self, request, *args, **kwargs):
		super().setup(request, *args, **kwargs)
		self.category = Category.objects.get(category_id=self.kwargs['category_id'])

	def get_queryset(self, **kwargs):
		return Product.products.filter(category__in=self.category.get_descendants(include_self=True))

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		wishlist_listings = []
		if self.request.user.is_authenticated:
			wishlist_listings = self.request.user.user_wishlist.all()
		context['wishlist_listings'] = wishlist_listings
		context['heading'] = self.category.title
		return context


class FeaturedCategoryListView (ListView):
	model = Product
	paginate_by = 12
	template_name = 'store/products.html'

	def setup(self, request, *args, **kwargs):
		super().setup(request, *args, **kwargs)
		self.featured_category: FeaturedCategory = FeaturedCategory.objects.get(slug=self.kwargs['featured_slug'])

	def get_queryset(self, **kwargs):
		return Product.products.filter(featured_category=self.featured_category)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		wishlist_listings = []
		if self.request.user.is_authenticated:
			wishlist_listings = self.request.user.user_wishlist.all()
		context['wishlist_listings'] = wishlist_listings
		context['heading'] = self.featured_category.name
		return context


class ProductDetailView (DetailView):
    model = Product
    template_name = 'store/product.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     post = Product.products.get(slug=self.kwargs['slug'])
    #     is_added_to_wishlist = False

    #     if request.user.is_authenticated:
    #         is_added_to_wishlist = post.user_wishlist.filter(id=request.user.id).exists()
    #         if request.user.username == post.creator.username:
    #             active = True
        
    #     context['is_added_to_wishlist'] = is_added_to_wishlist
    #     return context


@rate_limit(limit=5, period=60)
@csrf_protect
def contact_view(request):
	# Composing a new message must be via POST
	if request.method != "POST":
		return JsonResponse({"error": "POST request required."}, status=405)

	# Check sender data
	try:
		data = json.loads(request.body)
	except json.JSONDecodeError as e:
		logger.error(f"Error in contact form submission: {str(e)}")
		return JsonResponse({"error": "Invalid JSON in request.body."}, status=400)

	form = ContactForm(data)

	# Validate contact form
	if form.is_valid():
		# process form data
		cleaned_data = form.cleaned_data
        # Send email or save to database
		message = f"""
        New contact form submission:
        Name: {cleaned_data['fname']} {cleaned_data['lname']}
        Email: {cleaned_data['email']}
        Message: {cleaned_data['message']}
        """
		# send_mail('New Contact Form Submission', message, cleaned_data['email'], ['info@zubies.co'], fail_silently=False)
		return JsonResponse({"message": "Thankyou for contacting us."}, status=201)
	else:
		return JsonResponse({"error": form.errors}, status=400)

	# Create contact
	# contact = Contact(
	# 	fname=fname,
	# 	lname=lname,
	# 	phone_number=phone_number,
	# 	email=email,
	# 	message=message,
	# )
	# contact.save()
