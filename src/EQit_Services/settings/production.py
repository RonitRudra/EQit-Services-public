from decouple import Config, RepositoryEnv
from .common import *

# Go up two directories from project base and then into config
env_path = os.path.join(BASE_DIR,'..','..','config','production.env')

env_config = Config(RepositoryEnv(env_path))

SECRET_KEY = env_config.get('PROJECT_SECRET_KEY')
# Key for GEOCODE and MAPS API
GOOGLE_GEOCODE_API_KEY = env_config.get('GOOGLE_GEOCODE_API_KEY')
# Key for PLACES API
GOOGLE_PLACES_API_KEY = env_config.get('GOOGLE_PLACES_API_KEY')
# Key for DIRECTIONS API
GOOGLE_DIRECTIONS_API_KEY = env_config.get('GOOGLE_DIRECTIONS_API_KEY')

DEBUG = env_config.get('DEBUG',cast=bool)
ALLOWED_HOSTS = env_config.get('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])

DATABASES = {
    'default': {
        'ENGINE': env_config.get('DB_ENGINE'), 
        'NAME': env_config.get('DB_NAME'),
        'USER': env_config.get('DB_USER'),
        'PASSWORD': env_config.get('DB_PASSWORD'),
        'HOST': env_config.get('DB_HOST'),   # Or an IP Address that your DB is hosted on
        'PORT': env_config.get('DB_PORT'),
    }
}