import os
from pathlib import Path
from mongoengine import connect
import re

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure--9n-1!tr$$uu2(sgwm*-e52u#67!(d#_vj8_@juures&tmpb5v'

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'authentication',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'authentication.middleware.TokenAuthMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    "https://medbooksrl.onrender.com",
    "http://medbooksrl.onrender.com"
]
CORS_ALLOW_CREDENTIALS = True
CORS_EXPOSE_HEADERS = ['Content-Type', 'Authorization']

ROOT_URLCONF = 'mymedbook.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'mymedbook.wsgi.application'

# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# MongoDB connection
connect(
    db='mymedbook_db',
    host='mongodb+srv://mymedbook_admin:admin123@cluster1.cd8mi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1'
)

# Static files settings
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Media files settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'authentication.backends.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'UNAUTHENTICATED_USER': None,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ],
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler'
}

# OAuth2 Settings
OAUTH2_PROVIDER = {
    'TOKEN_URL': 'https://mymedbook.it/api/v1/oauth/token/',
    'CLIENT_ID': 'it.netfarm.mymedbook.web',
    'CLIENT_SECRET': '',
    'AUTHORIZATION_HEADER': 'Basic J2l0Lm5ldGZhcm0ubXltZWRib29rLndlYic6',
}

# Add CORS settings if not already present
CORS_ALLOW_ALL_ORIGINS = True  # For development only
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Security settings
SESSION_COOKIE_SECURE = False  # Set to True in production
CSRF_COOKIE_SECURE = False    # Set to True in production
SECURE_SSL_REDIRECT = False   # Set to True in production

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Rome'
USE_I18N = True
USE_TZ = True


# Define public paths using raw regex patterns
PUBLIC_PATHS = [
    r'^$',
    r'^health/?$',
    r'^auth/token/?$',
    r'^auth/verify/?$',  # Add verify endpoint
    r'^favicon\.ico$',
    r'^static/.*$',
    r'^admin/.*$',
    r'^media/.*$',
    r'^api/.*$'  # Temporarily allow all API endpoints for testing
]

# Update the middleware to use the compiled patterns
# Update the middleware to use the compiled patterns
class PublicPathsList:
    def __init__(self, patterns):
        self.patterns = [re.compile(pattern) for pattern in patterns]
    
    def match(self, path):
        return any(pattern.match(path) for pattern in self.patterns)

# Initialize the public paths
PUBLIC_PATHS = PublicPathsList(PUBLIC_PATHS)