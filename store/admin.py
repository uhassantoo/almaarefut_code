import os

from django.forms import ModelForm
from django.contrib import admin, messages
from django.utils.translation import gettext as _
from django.core.files.uploadedfile import UploadedFile
from django.contrib.contenttypes.admin import GenericTabularInline


from .forms import MultipleFileField
from .models import (
    Category,
    CategoryMedia,
    FeaturedCategory,
    Material,
    Product,
    ProductSpecification,
    ProductSpecificationValue,
    ProductMedia,
)


# Featured Category Model
@admin.register(FeaturedCategory)
class FeaturedCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]


# Material Model
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ["name"]


# Product Specification Model
admin.site.register(ProductSpecification)


# ProductSpecificationValue Inline Model
class ProductSpecificationValueInline(admin.TabularInline):
    model = ProductSpecificationValue


# Image Inline Model
class CategoryMediaInline(GenericTabularInline):
    model = CategoryMedia
    extra = 0
    can_delete = True
    verbose_name_plural = "Images"
    fields = ("image", "alt_text")


class CategoryAdminForm(ModelForm):
    images = MultipleFileField(required=False)

    class Meta:
        model = Category
        fields = "__all__"


class ProductAdminForm(ModelForm):
    images = MultipleFileField(required=False)

    class Meta:
        model = Product
        fields = "__all__"


class ProductMediaInline(GenericTabularInline):
    model = ProductMedia
    extra = 0
    can_delete = True
    verbose_name_plural = "Images"
    fields = ("image", "alt_text")


# Product Model
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    inlines = [
        ProductSpecificationValueInline,
        ProductMediaInline,
    ]
    list_display = (
        "title",
        "regular_price",
        "discount_price",
        "sku",
        "stock",
        "in_stock",
        "is_active",
        "category",
        "created",
        "updated",
        "image_tag",
    )
    list_filter = (
        "regular_price",
        "discount_price",
        "in_stock",
        "is_active",
        "category",
        "created",
    )
    list_editable = ("regular_price", "discount_price", "stock", "is_active")
    empty_value_display = "-empty-"

    def save_model(self, request, obj, form, change) -> None:
        super().save_model(request, obj, form, change)
        images = request.FILES.getlist("images")

        for image in images:
            if isinstance(image, UploadedFile):
                # Get the filename without extension
                filename = os.path.splitext(image.name)[0]

                # Create ProductImage with alt_text
                ProductMedia.objects.create(content_object=obj, image=image, alt_text=filename)
            else:
                print(f"Unexpected type for image: {type(image)}")

    @admin.action
    def make_active(self, request, queryset):
        queryset.update(active=True)
        messages.success(request, "Selected Record(s) Marked as Active Successfully !!")

    @admin.action
    def make_inactive(self, request, queryset):
        queryset.update(active=False)
        messages.success(
            request, "Selected Record(s) Marked as Inactive Successfully !!"
        )

    actions = ["make_active", "make_inactive"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    inlines = [ProductMediaInline]
    list_display = ('title', 'is_active', 'image_tag')
    list_filter = ('is_active',)
    search_fields = ('title', 'category_id')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        images = request.FILES.getlist('images')

        for image in images:
            if isinstance(image, UploadedFile):
                filename = os.path.splitext(image.name)[0]
                CategoryMedia.objects.create(
                    content_object=obj,
                    image=image,
                    alt_text=filename
                )
            else:
                print(f"Unexpected type for image: {type(image)}")

    def image_tag(self, obj):
        media = CategoryMedia.objects.filter(content_type__model='category', object_id=obj.id).first()
        if media:
            return media.image_tag()
        return "No image"
    image_tag.short_description = 'Image'


# Image Model
@admin.register(ProductMedia)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("content_type", "image_tag")
    list_filter = ("content_type",)
