from .base import *
import os

# SECRET_KEY = os.environ['SECRET_KEY']
SECRET_KEY = '5iki-^6er%sd0hjtkp_mk)5j)tm1pfcd!z(@(zcqmbwfxy#*5@'
DEBUG = False
ALLOWED_HOSTS = ['*', 'ashudihatti.in', 'www.ashudihatti.in']
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'