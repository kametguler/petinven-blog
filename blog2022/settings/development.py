from blog2022.settings.base import BASE_DIR

DEBUG = True

ALLOWED_HOSTS = []

SECRET_KEY = 'django-insecure-#sfr+%sg#mxffpue$m-3q(c-a1bakqh^ko!qglc0q@rn31qe)p'

META_SITE_PROTOCOL = 'http'
META_SITE_DOMAIN = "localhost:8000"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
