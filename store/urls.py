from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
	# Home Url
	path('', views.HomeView.as_view(), name='index'),
	# Category Url
	path('category/<uuid:category_id>/', views.CategoryListView.as_view(), name='products-by-category'),
	# Features Url
	path('featured-products/<slug:featured_slug>/', views.FeaturedCategoryListView.as_view(), name='products-by-featured-category'),
	# Product Detail Url
	path('product/<slug>/', views.ProductDetailView.as_view(), name='product'),
	# About Us Url
	path('about-us/', views.AboutView.as_view(), name='about-us'),
	# Contact Us API Url
	path('contact/', views.contact_view, name='contact-us')
]
