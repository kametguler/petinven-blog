from .base import MIDDLEWARE, BASE_DIR, INSTALLED_APPS, TEMPLATES
import dj_database_url
import os

DEBUG = False

ALLOWED_HOSTS = ["petinven.herokuapp.com"]

SECRET_KEY = 'django-insecure-#sfr+%sg#mxffpue$m-3q(c-a1bakqh^ko!qglc0q@rn31qe)p'

INSTALLED_APPS += ['django.contrib.sites', 'django.contrib.sitemaps', 'storages', 'django_q', ]

META_SITE_PROTOCOL = 'https'
META_SITE_DOMAIN = "petinven.herokuapp.com"

# AWS SETTINGS
AWS_ACCESS_KEY_ID = 'AKIAQKSY4ZHKB2CAY647'
AWS_SECRET_ACCESS_KEY = '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'
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

Q_CLUSTER = {
    'name': 'blog2022',
    'workers': 8,
    'recycle': 500,
    'timeout': 60,
    'compress': True,
    'save_limit': 250,
    'queue_limit': 500,
    'cpu_affinity': 1,
    'label': 'Django Q',
    'redis': {
        'host': os.environ('REDIS_HOST'),
        'password': os.environ('REDIS_PASSWORD'),
        'port': os.environ('REDIS_PORT'),
        'db': 0, }
}
