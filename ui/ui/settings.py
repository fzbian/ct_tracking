from pathlib import Path

from django.conf.global_settings import STATIC_ROOT

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-zliqz3b=nr$q6p3m5vl-4qo=o2#+h6hz6r%#(1h$3*8nw7dbad'

DEBUG = False

ALLOWED_HOSTS = ['*']

# URL para acceder a los archivos estáticos
STATIC_URL = '/static/'

# Directorio en el que se recopilan los archivos estáticos para producción
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Directorio donde almacenas archivos estáticos durante el desarrollo
STATICFILES_DIRS = [BASE_DIR / "app/templates/static"]

# Locale paths
LOCALE_PATHS = [
    BASE_DIR / 'locale',  # Asegúrate de que esta carpeta exista
]

# Languages
LANGUAGES = [
    ('es', 'Español'),
    ('en', 'English'),
    ('zh', 'Chino simplificado'),
]

# Internationalization settings
LANGUAGE_CODE = 'es'  # Define el idioma predeterminado
USE_I18N = True
USE_L10N = True
USE_TZ = True

TIME_ZONE = 'UTC'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.auth',
    'app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # Para permitir cambiar idiomas
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ui.urls'

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

WSGI_APPLICATION = 'ui.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
