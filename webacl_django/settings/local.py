from base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '42c6!-_xyxl^tj@)jwde4ld+ukb11(gts803=kxw^%jpv@x@fb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

