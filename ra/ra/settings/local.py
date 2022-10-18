from .base import *
import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)(%=m#1$bbk#q=v=1dz61%2sz0y&zba2qu8&+m3mch*948$q2t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Static Details
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'django-static')

# Media Details
MEDIA_URL = '/media/'
MEDIA_LOCAL_URL = 'http://localhost:8000'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CSRF_COOKIE_SECURE = False
