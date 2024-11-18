from storages.backends.s3boto3 import S3Boto3Storage
from django.contrib.staticfiles.storage import ManifestFilesMixin
from django.core.files.base import ContentFile
from django.contrib.staticfiles.utils import matches_patterns

class MediaStore(S3Boto3Storage):
    location = 'media'
    file_overwrite = True

class StaticManifestS3Storage(ManifestFilesMixin, S3Boto3Storage):
    location = 'static'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def hashed_name(self, name, content=None, filename=None):
        # First, check if the file exists
        if not self.exists(name):
            # If it doesn't exist, return the original name
            return name
        return super().hashed_name(name, content, filename)

    def post_process(self, paths, dry_run=False, **options):
        if dry_run:
            return

        # Call the parent's post_process method
        processed_paths = super().post_process(paths, dry_run, **options)

        # Iterate through the processed paths
        for name, hashed_name, processed in processed_paths:
            if isinstance(processed, Exception):
                # If processing failed, try to handle it
                if not self.exists(name):
                    # If the file doesn't exist, create an empty file
                    self.save(name, ContentFile(b''))
                # Yield the result, even if it's an exception
                yield name, hashed_name, processed
            else:
                # If processing succeeded, yield the result
                yield name, hashed_name, processed

    def stored_name(self, name):
        # Check if the file exists before trying to hash it
        if self.exists(name):
            return super().stored_name(name)
        return name