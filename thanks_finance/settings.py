"""
Django settings for thanks_finance project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



BASE_DIR1 = os.path.dirname(os.path.dirname(os.path.abspath(__package__)))
env_file_path = os.path.join(BASE_DIR1, "venv/.env")
load_dotenv(os.path.join(env_file_path))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "rest_framework_swagger",
    'drf_yasg',
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'users',
    # 'photoapp'
    
    'rest_framework',
    'oauth2_provider',
    'cities_light',
    'multiselectfield'
     ]

AUTH_USER_MODEL = 'users.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


TEMPLATES_DIRS =(
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'templates')
)

URL_TYPE = "http://0.0.0.0:8000"
URL_TYPE = "http://0.0.0.0:7000"


ROOT_URLCONF = 'thanks_finance.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR,'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {  # Adding this section should work around the issue.
                'staticfiles': 'django.templatetags.static',
            },
        },
    },
]

WSGI_APPLICATION = 'thanks_finance.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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



REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    )
}

# OAUTH2_PROVIDER = {
#     # this is the list of available scopes
#     'SCOPES': {'administration': 'All operation do',
#                'Basic':'basice user',
#                'Premium':'premium user',
#                'Professional':'professional user',
#                }
# }

SWAGGER_SETTINGS = {

    'exclude_url_names': [],
    'exclude_namespaces': [],
    'api_version': '1.0',
    'api_path': '/',
    'relative_paths': False,
    'enabled_methods': [
        'get',
        'post',
        'put',
        'patch',
        'delete'
    ],
    'api_key': '',
    'is_authenticated': False,
    'is_superuser': False,
    'unauthenticated_user': 'django.contrib.auth.models.AnonymousUser',
    'permission_denied_handler': None,
    'resource_access_handler': None,
    'base_path':'helloreverb.com/docs',
    'info': {
        'contact': 'apiteam@wordnik.com',
        'description': 'This is a sample server Petstore server. '
                       'You can find out more about Swagger at '
                       '<a href="http://swagger.wordnik.com">'
                       'http://swagger.wordnik.com</a> '
                       'or on irc.freenode.net, #swagger. '
                       'For this sample, you can use the api key '
                       '"special-key" to test '
                       'the authorization filters',
        'license': 'Apache 2.0',
        'licenseUrl': 'http://www.apache.org/licenses/LICENSE-2.0.html',
        'termsOfServiceUrl': 'http://helloreverb.com/terms/',
        'title': 'Swagger Sample App',
    },
    'doc_expansion': 'none',
}

LOGIN_URL='/admin/login/'

CLIENT_SECRET= os.getenv("CLIENT_SECRET")
CLIENT_ID = os.getenv("CLIENT_ID")



# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_ID")
EMAIL_HOST_PASSWORD = os.getenv("PASSWORD")



JAZZMIN_SETTINGS={
     # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Thanks Finance Admin",

    # Title on the brand, and login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Thanks Finance",

    # # square logo to use for your site, must be present in static files, used for favicon and brand on top left
    "site_logo": "logo.jpg",

    # Welcome text on the login screen
    "welcome_sign": "Welcome to the Thanks Finance",

    # # Copyright on the footer
    "copyright": "Thanks Finance Ltd",

    # The model admin to search from the search bar, search bar omitted if excluded
    # "search_model": "[auth.User, city_light]",

    # Field name on user model that contains avatar image
    "user_avatar": None,

    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free
    # for a list of icon classes
    "icons": {
        "cities_light.country": "fas fa-globe-americas",
        "cities_light.region": "fas fa-map-marker-alt",
        "users.country": "fas fa-globe-americas",
        "users.state":"fas fa-map-marker-alt",
        "users.plan":"fas fa-map",
        "users.subscriptions":"fas fa-clock",
        "users.transaction":"fas fa-dollar-sign",
        "users.user":"fas fa-users",
        "users.bookmark":"far fa-bookmark",
    },
}

JAZZMIN_SETTINGS["show_ui_builder"] = True

JAZZMIN_UI_TWEAKS = {
    "theme": "simplex",
}