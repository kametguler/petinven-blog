from .base import MIDDLEWARE, BASE_DIR
import os

DEBUG = False

ALLOWED_HOSTS = ["petinven.herokuapp.com"]

SECRET_KEY = 'django-insecure-#sfr+%sg#mxffpue$m-3q(c-a1bakqh^ko!qglc0q@rn31qe)p'

META_SITE_PROTOCOL = 'https'
META_SITE_DOMAIN = "petinven.com"

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
