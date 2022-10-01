from blog2022.settings.base import BASE_DIR, INSTALLED_APPS

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS += ['django.contrib.sites', 'django.contrib.sitemaps', ]

SECRET_KEY = 'SECRET'

META_SITE_PROTOCOL = 'http'
META_SITE_DOMAIN = "localhost:8000"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',

    }
}

SITE_ID = 1
