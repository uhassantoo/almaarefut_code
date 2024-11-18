from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils.crypto import get_random_string
from django.core.files.base import ContentFile
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Image Resize and Upload
from PIL import Image as PillowImage
from io import BytesIO

class AbstractMediaModel(models.Model):
    """
    Abstract media model for common attributes and methods
    """
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='%(class)s')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def directory_path(instance, filename):
        return f'{instance.content_type.model}_media/item_{instance.content_object.title}/{filename}'

    image = models.ImageField(verbose_name=_("image"), upload_to=directory_path)
    alt_text = models.CharField(verbose_name=_("Alternative text"), max_length=255, help_text=_("Description of the image for SEO purposes"), default='this is image')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" style="width: 45px; height:45px;" />') if self.image else 'No image found'
    image_tag.short_description = 'Image'

    def save(self, *args, **kwargs):
        if not self.image:
            return super().save(*args, **kwargs)

        img = PillowImage.open(self.image)
        # Resize image
        output_size = (800, 800)
        img.thumbnail(output_size)

        # Save the resized image to a BytesIO buffer
        output_buffer = BytesIO()
        img.save(output_buffer, format='WebP')
        output_buffer.seek(0)

        # Generate a unique name for the image
        random_string = get_random_string(length=8)
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        filename = f'{random_string}_{timestamp}.webp'

        # Save the buffer content to the image field with the unique filename
        self.image.save(filename, ContentFile(output_buffer.read()), save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image for {self.content_object.title}"