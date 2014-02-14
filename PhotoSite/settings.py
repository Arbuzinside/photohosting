"""
Django settings for PhotoSite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


TEMPLATE_DIRS = (
  BASE_DIR + '/PhotoAlbum/Templates/'
)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%@30nk@)59895i)i*cb-@k$(uwu9j3g53$s-)k$0xi682hekgn'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'PhotoAlbum',
    'social_auth',
    'social.apps.django_app.default',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_auth.middleware.SocialAuthExceptionMiddleware',
)

ROOT_URLCONF = 'PhotoSite.urls'

WSGI_APPLICATION = 'PhotoSite.wsgi.application'

#Social auth
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/home/'
LOGIN_ERROR_URL = '/'

AUTH_PROFILE_MODULE = "auth.User"

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.facebook.FacebookBackend',
   'django.contrib.auth.backends.ModelBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = (
                            'django.contrib.auth.context_processors.auth',
                            'social_auth.context_processors.social_auth_by_type_backends',
                          
)

SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'
SOCIAL_AUTH_UID_LENGTH = 16
SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 16
SOCIAL_AUTH_NONCE_SERVER_URL_LENGTH = 16
SOCIAL_AUTH_ASSOCIATION_SERVER_URL_LENGTH = 16
SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 16

SOCIAL_AUTH_ENABLED_BACKENDS = ('facebook')
#SOCIAL_AUTH_USER_MODEL = 'django.contrib.auth.models.User'


SOCIAL_AUTH_FACEBOOK_KEY = '558139250949505'
SOCIAL_AUTH_FACEBOOK_SECRET = '40d43486cc9885c35db222d13a82e9ac'
FACEBOOK_EXTENDED_PERMISSIONS = ['email']
# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

#DATABASES = {
 #   'default': {
  #      'ENGINE': 'django.db.backends.postgresql_psycopg2',
   #     'NAME': 'postgres',
    #    'USER': 'postgres',
     #   'PASSWORD': 'admin',
      #  'HOST': 'localhost',
       # 'PORT': '', 
    #}
#}

# we only need the engine name, as heroku takes care of the rest
DATABASES = {
"default": {
   "ENGINE": "django.db.backends.postgresql_psycopg2",
}
}


# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration



# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/Static/'

STATICFILES_DIRS = (
    BASE_DIR + '/PhotoAlbum/Static/',
)

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'moments.albums@gmail.com'
EMAIL_HOST_PASSWORD = 'Software'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
