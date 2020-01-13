from .dev import *

DATABASES['default'] = {
    'ENGINE': 'django.contrib.gis.db.backends.spatialite',
    'NAME': 'estateman',
}

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]