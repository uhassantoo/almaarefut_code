from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import (render, redirect)
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.auth import (login, logout)
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import (force_bytes, force_str)
from django.utils.http import (urlsafe_base64_decode, urlsafe_base64_encode)
from django.views.generic import ListView

from .forms import (RegistrationForm, ProfileEditForm)
from .token import account_activation_token

# Store App
from store.models import Product


class WishlistView(LoginRequiredMixin, ListView):
	template_name = 'account/user/wishlist.html'
	paginate_by = 12

	def get_queryset(self, *kwargs):
		return Product.products.filter(user_wishlist=self.request.user)
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		wishlist_listings = []
		if self.request.user.is_authenticated:
			wishlist_listings = self.request.user.user_wishlist.all()
		context['wishlist_listings'] = wishlist_listings
		return context


@login_required
def Add_to_wishlist_view(request, slug):
	try:
		product = Product.products.get(slug=slug)
		if product.user_wishlist.filter(id=request.user.id).exists():
			product.user_wishlist.remove(request.user)
		else:
			product.user_wishlist.add(request.user)
			
	except ObjectDoesNotExist:
		messages.error(request, 'Product doesn\'t exist.')
	
	return redirect(request.META['HTTP_REFERER'])

@login_required
def dashboard(request):
	return render(request, 'account/user/dashboard.html')


@login_required
def edit_details(request):
	if request.method == 'POST':
		user_form = ProfileEditForm(instance=request.user, data=request.POST)
		if user_form.is_valid():
			user_form.save()
	else:
		user_form = ProfileEditForm(instance=request.user)

	return render(request, 'account/user/edit_details.html', {
		'form': user_form
	})


@login_required
def delete_user(request):
	user = get_user_model().objects.get(email=request.user)
	user.is_active = False
	user.save()
	logout(request)
	return redirect('account:delete_confirm')


class CustomLoginView(LoginView):
	def dispatch(self, request, *args, **kwargs):
		if self.request.user.is_authenticated:
			next_url = self.request.GET.get('next')
			if next_url != None:
				return redirect(next_url)
			else:
				return redirect('store:index')
		return super().dispatch(request, *args, **kwargs)

	def form_invalid(self, form):
		try:
			user = get_user_model().objects.get(email=form.cleaned_data.get('username'))
			# Check if the user is active
			if not user.is_active and not user.is_verified:
				# Resend verification email to the user
				# Setup email
				current_site = get_current_site(self.request)
				subject = 'Activate your Account'
				message = render_to_string('account/registration/account_verification_resent_email.html', {
					'user': user,
					'domain': current_site.domain,
					'uid': urlsafe_base64_encode(force_bytes(user.pk)),
					'token': account_activation_token.make_token(user),
				})
				user.send_verification_email(subject=subject, message=message)
				# Add a message to inform the user about the email resent
				messages.info(self.request, 'A verification email has been resent. Please check your email and activate your account.')
				self.user.send_verification_email(self.request.user)
				
				
				# Redirect the user to a page indicating that the verification email has been resent
				return redirect('account:login')
		except:
			pass
		
		return super().form_invalid(form)

	def get_success_url(self):
		# Get the value of the 'next' parameter from the request's GET parameters
		next_url = self.request.GET.get('next')
		messages.success(self.request, "Welcome back! We knew you couldn't stay away for long!")

		if next_url != None:
			return next_url
		else:
			return reverse('store:index')


def register(request):
	if request.user.is_authenticated:
		return redirect('/')

	if request.method == "POST":
		registerForm = RegistrationForm(request.POST)
		if registerForm.is_valid():
			user = registerForm.save(commit=False)
			user.is_active = False
			user.is_verified = False
			user.save()

			# Setup email
			current_site = get_current_site(request)
			subject = 'Activate your Account'
			message = render_to_string('account/registration/account_activation_email.html', {
				'user': user,
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': account_activation_token.make_token(user),
			})
			user.send_verification_email(subject=subject, message=message)
			messages.success(request, "Your account is officially alive! Now, go check your email for verification magic.")

	else:
		registerForm = RegistrationForm()
	return render(request, 'account/registration/register.html', {
		'form': registerForm
	})


def account_activate(request, uid64, token):
	try:
		uid = force_str(urlsafe_base64_decode(uid64))
		user = get_user_model().objects.get(pk=uid)
	except():
		pass
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.is_verified = True
		user.save()
		messages.success(request, "Your account has been verified! You're all set to start shopping. Enjoy your experience!")
		login(request, user)
		return redirect('account:dashboard')
	else:
		messages.error(request, 'Invalid User/token')
		return redirect('account:login')


def logout_view(request):
	logout(request)
	messages.info(request, "Logged out! We'll miss you... but not for long, right?")
	return redirect("store:index")
