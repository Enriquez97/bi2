from pathlib import Path
import os
from decouple import config
from celery.schedules import crontab
from .defaults import *
import pymysql
os.environ['S3_USE_SIGV4'] = 'True'
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


pymysql.install_as_MySQLdb()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')
#print(config('DATABASE_NAME_MYSQL'))
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

CORS_ORIGIN_ALLOW_ALL = True
# CORS_ALLOW_CREDENTIALS = False
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]

CSRF_TRUSTED_ORIGINS = ["https://example.com"]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'apoloappauth',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Application definition

BANNED_DOMAINS = ['trash-mail.com', 'you-spam.com',
                  're-gister.com', 'fake-box.com', 'trash-me.com', 'opentrash.com']


# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'django_celery_beat',
    'celery',
    'django_elasticsearch_dsl',
    'rest_framework',
    'drf_yasg',
    'whitenoise.runserver_nostatic',
    'corsheaders',
    'silk',
    'channels',
    'crum',
    'django_plotly_dash.apps.DjangoPlotlyDashConfig',
    'dpd_static_support',
]

PROJECT_APPS = [
   'apps.bi',
   'apps.handler_data',
   'apps.handler_layout',
   'apps.management',
   'apps.oldapp'
]
INSTALLED_APPS = DJANGO_APPS  + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'silk.middleware.SilkyMiddleware',  # SilkyMiddleware before CacheMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # make sure to add this line
    
    'django.middleware.csrf.CsrfViewMiddleware',
    'crum.CurrentRequestUserMiddleware',
    
    'django_plotly_dash.middleware.ExternalRedirectionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django_plotly_dash.middleware.BaseMiddleware',
]


ROOT_URLCONF = 'backend.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates/'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
"""
DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
     }
}
"""
DATABASES = {
    'default': {
        # 'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'ENGINE': 'django.db.backends.mysql',
        'NAME':     config('DATABASE_NAME_MYSQL'),
        'USER':     config('DATABASE_USER_MYSQL'),
        'PASSWORD': config('DATABASE_PASSWORD_MYSQL'),
        'HOST':     config('DATABASE_HOST_MYSQL'),
        'PORT':     config('DATABASE_PORT_MYSQL'),
    }
}





# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Lima'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join (BASE_DIR, 'static')

STATICFILES_DIRS=[
    os.path.join(BASE_DIR,'backend/static')
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": (config('REDIS_HOST'), config('REDIS_PORT')),
        },
    },
}

# https://medium.com/@ksarthak4ever/django-handling-periodic-tasks-with-celery-daaa2a146f14
BROKER_URL = config('BROKER_URL')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND')
CELERY_ACCEPT_CONTENT = ['pickle']
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_TIMEZONE = 'UTC'
CELERY_TASK_TIME_LIMIT = 30 * 60


ELASTICSEARCH_DSL = {
    'default': {
        'hosts':  "elasticsearch:9200",
        'timeout': 50,  # Increase timeout to 30 seconds or more
      
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Celery Beat

CELERY_BEAT_SCHEDULE = {
    "sample_task": {
        "task": "backend.celery_conf.sample_task",
        "schedule": crontab(minute="*/1"),
    },
}

CACHES = {
    "alternate": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:@redis:6379/1",
        "OPTIONS": {
            "DB": 1,
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:@redis:6379/1",
        "OPTIONS": {
            "DB": 2,
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django_plotly_dash.finders.DashAssetFinder',
    'django_plotly_dash.finders.DashComponentFinder',
    'django_plotly_dash.finders.DashAppDirectoryFinder',
]

PLOTLY_COMPONENTS = [
    'dash_mantine_components',
    'dash_core_components',
    'dash_html_components',
    'dash_renderer',
    'dpd_components',
    'dpd_static_support',
    'dash_bootstrap_components',
    'dash_bootstrap_templates',
]

LOGIN_URL = '/user/login/'
LOGIN_REDIRECT_URL='/user/login/'

DATA_UPLOAD_MAX_MEMORY_SIZE=1000000000
MAX_ACTIVE_TASKS  = 100