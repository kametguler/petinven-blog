from .base import MIDDLEWARE, BASE_DIR, INSTALLED_APPS, TEMPLATES
import dj_database_url
import os

DEBUG = False

ALLOWED_HOSTS = ["petinven.herokuapp.com", "www.petinven.com", "petinven.com"]

SECRET_KEY = os.environ.get("SECRET_KEY")

INSTALLED_APPS += ['django.contrib.sites', 'django.contrib.sitemaps', 'storages', ]

META_SITE_PROTOCOL = 'https'
META_SITE_DOMAIN = "petinven.com"

# AWS SETTINGS
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = 'petinven-blog'

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES = {
    'default': {}
}
DATABASES['default'].update(db_from_env)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

SITE_ID = 1

TEMPLATES[0]["OPTIONS"]["context_processors"].append("blog2022.context_processors.export_vars")
