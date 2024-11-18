# Generated by Django 5.0.4 on 2024-11-18 13:59

import abstract.models
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('title', models.CharField(help_text='Required and unique', max_length=124, verbose_name='Category Name')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='FeaturedCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Required', max_length=255, verbose_name='Featured Category Name')),
                ('slug', models.SlugField(editable=False, max_length=255, unique=True, verbose_name='Featured Category Safe URL')),
            ],
            options={
                'verbose_name': 'Featured Category',
                'verbose_name_plural': 'Featured Categories',
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Required', max_length=255, verbose_name='Material Name')),
            ],
        ),
        migrations.CreateModel(
            name='ProductSpecification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Required', max_length=255, verbose_name='Attribute Name')),
            ],
            options={
                'verbose_name': 'Product Specification',
                'verbose_name_plural': 'Product Specifications',
            },
        ),
        migrations.CreateModel(
            name='CategoryMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('image', models.ImageField(upload_to=abstract.models.AbstractMediaModel.directory_path, verbose_name='image')),
                ('alt_text', models.CharField(default='this is image', help_text='Description of the image for SEO purposes', max_length=255, verbose_name='Alternative text')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s', to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'Category Image',
                'verbose_name_plural': 'Category Images',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Required', max_length=255, unique=True)),
                ('slug', models.SlugField(editable=False, max_length=255, unique=True)),
                ('regular_price', models.DecimalField(decimal_places=2, error_messages={'name': {'max_length': 'The price must be between 0 and 99999999.99.'}}, help_text='Maximum 99999999.99', max_digits=10, verbose_name='Regular Price')),
                ('discount_price', models.DecimalField(blank=True, decimal_places=2, error_messages={'name': {'max_length': 'The price must be between 0 and 99999999.99.'}}, help_text='Maximum 99999999.99', max_digits=10, null=True, verbose_name='Discount Price')),
                ('description', models.TextField(help_text='Required')),
                ('sku', models.CharField(default='123', max_length=124)),
                ('weight', models.IntegerField(default=0, help_text='kg')),
                ('stock', models.IntegerField(default=0)),
                ('in_stock', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True, help_text='Change Product Visibility', verbose_name='Product Visibility')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='store.category')),
                ('featured_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='store.featuredcategory')),
                ('material', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='store.material')),
                ('user_wishlist', models.ManyToManyField(blank=True, related_name='user_wishlist', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='ProductMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('image', models.ImageField(upload_to=abstract.models.AbstractMediaModel.directory_path, verbose_name='image')),
                ('alt_text', models.CharField(default='this is image', help_text='Description of the image for SEO purposes', max_length=255, verbose_name='Alternative text')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s', to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'Product Image',
                'verbose_name_plural': 'Product Images',
            },
        ),
        migrations.CreateModel(
            name='ProductSpecificationValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(help_text='Product Specification Value (maximum of 255 characters)', max_length=255, verbose_name='Attribute Value')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specification', to='store.product')),
                ('specification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.productspecification')),
            ],
            options={
                'verbose_name': 'Product Specification Value',
                'verbose_name_plural': 'product Specification Values',
            },
        ),
    ]
