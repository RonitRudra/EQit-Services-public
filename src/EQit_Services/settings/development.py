#import configparser

from decouple import Config, RepositoryEnv
from .common import *
## LOAD CONFIG DATA
#config = configparser.ConfigParser()
#config.read('config.ini')
## SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = config['DEFAULT']['PROJECT_SECRET_KEY']
## Key for GEOCODE and MAPS API
#GOOGLE_GEOCODE_API_KEY = config['DEFAULT']['GOOGLE_GEOCODE_API_KEY']
## Key for PLACES API
#GOOGLE_PLACES_API_KEY = config['DEFAULT']['GOOGLE_PLACES_API_KEY']
## Key for DIRECTIONS API
#GOOGLE_DIRECTIONS_API_KEY = config['DEFAULT']['GOOGLE_DIRECTIONS_API_KEY']
env_path = os.path.join(BASE_DIR,'..','..','config','development.env')
print(env_path)
env_config = Config(RepositoryEnv(env_path))

SECRET_KEY = env_config.get('PROJECT_SECRET_KEY')
# Key for GEOCODE and MAPS API
GOOGLE_GEOCODE_API_KEY = env_config.get('GOOGLE_GEOCODE_API_KEY')
# Key for PLACES API
GOOGLE_PLACES_API_KEY = env_config.get('GOOGLE_PLACES_API_KEY')
# Key for DIRECTIONS API
GOOGLE_DIRECTIONS_API_KEY = env_config.get('GOOGLE_DIRECTIONS_API_KEY')

DEBUG = env_config.get('DEBUG',cast=bool)
ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Email Debugging Server Settings----------------------------------------------

EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
#------------------------------------------------------------------------------

# Media Settings---------------------------------------------------------------
MEDIA_URL ='/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')
#------------------------------------------------------------------------------