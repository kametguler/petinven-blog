from .base import MIDDLEWARE, BASE_DIR
import dj_database_url
import os

DEBUG = False

ALLOWED_HOSTS = ["petinven.herokuapp.com"]

SECRET_KEY = 'django-insecure-#sfr+%sg#mxffpue$m-3q(c-a1bakqh^ko!qglc0q@rn31qe)p'

META_SITE_PROTOCOL = 'https'
META_SITE_DOMAIN = "petinven.herokuapp.com"

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES = {
    'default': {}
}
DATABASES['default'].update(db_from_env)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
