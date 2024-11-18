from .base import *

ALLOWED_HOSTS = ['.zubies.co', '67.223.119.66']

## CSRF TOKEN CLEARANCE
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_DOMAIN = '.zubies.co'
CSRF_TRUSTED_ORIGINS = ['https://zubies.co', 'https://www.zubies.co']

## Secure-Only Session Cookie
SESSION_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True

DATABASES = {
	'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': os.environ.get("DB_NAME"),
        'USER': os.environ.get("DB_USER"),
        'PASSWORD': os.environ.get("DB_PASSWORD"),
        'HOST': os.environ.get("DB_HOST"),
        'PORT': os.environ.get("DB_PORT"),
        'OPTIONS': {
            'unix_socket': '/var/lib/mysql/mysql.sock',  # SHOW VARIABLES LIKE 'socket';
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}



ADMINS = ['talhamalik25.tm@gmail.com']

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_SIGNATURE_NAME = 's3v4',
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
AWS_S3_CUSTOM_DOMAIN = F'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
AWS_DEFAULT_ACL =  None
AWS_S3_VERITY = True

AWS_LOCATION = 'static'

# Media
DEFAULT_FILE_STORAGE = 'core.storages.MediaStore'

# Static Configuration S3
STATICFILES_STORAGE = 'core.storages.StaticManifestS3Storage'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')