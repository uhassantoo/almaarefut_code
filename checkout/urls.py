from django.urls import path

from . import views

app_name = 'checkout'

urlpatterns = [
	path('', views.CheckoutView, name='checkout'),
	path('update-delivery-charges', views.UpdateDeliveryChargesInBasket, name='update-dc-in-basket')
]