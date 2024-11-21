import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.utils.safestring import mark_safe



from abstract.models import AbstractMediaModel

# Image Resize and Upload
from PIL import Image as PillowImage
from io import BytesIO


# Model Managers
class ProductManager(models.Manager):
	def get_queryset(self):
		return super(ProductManager, self).get_queryset().filter(is_active=True, in_stock=True)


# Models
class Category (models.Model):
	"""
	Category table implimented
	"""
	category_id = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)
	title = models.CharField(
		verbose_name=_("Category Name"),
		help_text=_("Required and unique"),
		max_length=124,
	)
	is_active = models.BooleanField(default=True)
	



	class Meta:
		verbose_name = _("Category")
		verbose_name_plural = _("Categories")

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('store:products-by-category', kwargs={
			'category_id': self.category_id
		})

	def get_images(self):
		return CategoryMedia.objects.filter(content_type__model='category', object_id=self.id)


class CategoryMedia(AbstractMediaModel):
	"""
	Category Images
	"""

	class Meta:
		verbose_name = _("Category Image")
		verbose_name_plural = _("Category Images")



class FeaturedCategory (models.Model):
	"""
	Featured Categories for products like seasoned, new articles, best-selling
	"""
	name = models.CharField(verbose_name=_("Featured Category Name"), help_text=_("Required"), max_length=255)
	slug = models.SlugField(verbose_name=_("Featured Category Safe URL"), max_length=255, unique=True, editable=False)

	class Meta:
		verbose_name = _("Featured Category")
		verbose_name_plural = _("Featured Categories")

	def __str__(self):
		return self.name
	
	def get_absolute_url(self):
		return reverse('store:product-by-featured-categories', kwargs={
			'featured_slug': self.slug
		})

	def save (self, *args, **kwargs):
		value = self.name.replace(" ", "-")
		self.slug = slugify(value, allow_unicode=True)
		super().save(*args, **kwargs)


class Material (models.Model):
	"""
	Product made by which material
	"""

	name = models.CharField(verbose_name=_("Material Name"), help_text=_("Required"), max_length=255)

	def __str__(self):
		return self.name


class ProductSpecification(models.Model):
	"""
	The Product Specification Table contains product specification of features for the product types
	"""

	name = models.CharField(verbose_name=_("Attribute Name"), help_text=_("Required"), max_length=255)
	

	class Meta:
		verbose_name = _("Product Specification")
		verbose_name_plural = _("Product Specifications")

	def __str__(self):
		return self.name


class ProductSpecificationValue(models.Model):
	"""
	The Product Specification Value table holds each of the products individual specification or bespoke features
	"""
	
	product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="specification")
	specification = models.ForeignKey("ProductSpecification", on_delete=models.CASCADE)
	value = models.CharField(verbose_name=_("Attribute Value"), max_length=255, help_text=_("Product Specification Value (maximum of 255 characters)"))


	class Meta:
		verbose_name = _("Product Specification Value")
		verbose_name_plural = _("product Specification Values")

	def __str__(self):
		return self.value


class Product (models.Model):
	"""
	The Product table containing all product items
	"""

	title = models.CharField(max_length=255, unique=True, help_text=_("Required"))
	slug = models.SlugField(max_length=255, unique=True, editable=False)
	regular_price = models.DecimalField(verbose_name=_("Regular Price"), max_digits=10, decimal_places=2, help_text=_("Maximum 99999999.99"), error_messages={
		"name": {
			"max_length": _("The price must be between 0 and 99999999.99."),
		},
	})
	discount_price = models.DecimalField(verbose_name=_("Discount Price"), max_digits=10, decimal_places=2, help_text=_("Maximum 99999999.99"), error_messages={
		"name": {
			"max_length": _("The price must be between 0 and 99999999.99."),
		},
	}, blank=True, null=True)
	description = models.TextField(help_text=_("Required"))
	sku = models.CharField(default='123', max_length=124)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="posts")
	featured_category = models.ForeignKey(FeaturedCategory, on_delete=models.CASCADE, related_name="posts", blank=True, null=True)
	material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name="posts", blank=True, null=True)
	weight = models.IntegerField(default=0, help_text=_('kg'))
	stock = models.IntegerField(default=0)
	in_stock = models.BooleanField(default=True)
	is_active = models.BooleanField(verbose_name=_("Product Visibility"), help_text=_("Change Product Visibility"), default=True)
	user_wishlist = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_wishlist', blank=True)
	created = models.DateTimeField(verbose_name=_("Created At"), auto_now_add=True, editable=False)
	updated = models.DateTimeField(verbose_name=_("Updated At"), auto_now=True)

	objects = models.Manager()
	products = ProductManager()

	class Meta:
		verbose_name = _("Product")
		verbose_name_plural = _("Products")
		ordering = ('-created',)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('store:product', kwargs={
			'slug': self.slug
		})
	
	def image_tag(self):
		f_image = ProductMedia.objects.filter(content_type__model='product', object_id=self.id).first()
		if f_image:
			return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % f_image.image.url)
		else:
			return 'No image found'
	image_tag.short_description = 'Image'

	def save (self, *args, **kwargs):
		value = self.title.replace(" ", "-")
		self.slug = slugify(value, allow_unicode=True)

		self.in_stock = self.stock > 0

		super().save(*args, **kwargs)


class ProductMedia (AbstractMediaModel):
	"""
    Product Images
    """
   

	class Meta:
		verbose_name = _("Product Image")
		verbose_name_plural = _("Product Images")
  