# settings.py (revised for env / docker-friendly usage)
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------
# Helper: read env with defaults
# -------------------------
def getenv(key, default=None):
    return os.environ.get(key, default)

def getenv_bool(key, default=False):
    val = os.environ.get(key)
    if val is None:
        return default
    return val.lower() in ("1", "true", "yes", "on")

# -------------------------
# SECRET & DEBUG (from env)
# -------------------------
SECRET_KEY = getenv('4drVaYJcfYoUjSxZmx2knjMIlYMYnx0VaiNZUWOJzAYPbcAa2CuiH73_UGiNakElm2o')
DEBUG = getenv_bool('DEBUG', True)

# -------------------------
# Hosts
# -------------------------
# ALLOWED_HOSTS can be a comma-separated string in env, e.g. "localhost,127.0.0.1,mydomain.com"
raw_hosts = getenv('ALLOWED_HOSTS', '')
if raw_hosts:
    ALLOWED_HOSTS = [h.strip() for h in raw_hosts.split(',') if h.strip()]
else:
    # default local/dev hosts
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# -------------------------
# Installed apps & middleware
# -------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # If you want whitenoise for simple static serving without nginx, enable below:
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'JELAYAN_CAPITAL.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # keep your template dirs; BASE_DIR / 'templates' is safer than relative path
        'DIRS': [ BASE_DIR / 'templates' ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'JELAYAN_CAPITAL.wsgi.application'

# -------------------------
# Database (env-driven)
# -------------------------
# Default settings tuned for MariaDB/MySQL. Use DB_HOST=db for docker-compose.
DB_NAME = getenv('DB_NAME', 'jelayancapital_db')
DB_USER = getenv('DB_USER', 'jelayuser')
DB_PASS = getenv('DB_PASS', 'S0methingG00d!')
DB_HOST = getenv('DB_HOST', '127.0.0.1')   # in docker use 'db'
DB_PORT = getenv('DB_PORT', '3306')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASS,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# -------------------------
# Password validation
# -------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# -------------------------
# Internationalization
# -------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = getenv('TIME_ZONE', 'UTC')
USE_I18N = True
USE_TZ = True

# -------------------------
# Static & Media
# -------------------------
STATIC_URL = '/static/'

# Where collectstatic will place files (used by nginx or static server)
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Extra places to look for static (dev)
STATICFILES_DIRS = [ BASE_DIR / 'main' / 'static' ]

# Media (if you have uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# If you choose to use whitenoise in middleware, uncomment:
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# -------------------------
# Default primary key field type
# -------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -------------------------
# SECURITY (turn on when DEBUG=False)
# -------------------------
if not DEBUG:
    # production hardening
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = int(getenv('SECURE_HSTS_SECONDS', 31536000))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = getenv_bool('SECURE_HSTS_INCLUDE_SUBDOMAINS', True)
    SECURE_HSTS_PRELOAD = getenv_bool('SECURE_HSTS_PRELOAD', True)
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
else:
    # dev-friendly defaults
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False

# -------------------------
# Logging (basic, extend as needed)
# -------------------------
LOG_LEVEL = 'DEBUG' if DEBUG else 'INFO'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {'format': '[%(asctime)s] %(levelname)s %(name)s: %(message)s'}
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'formatter': 'standard'},
    },
    'root': {
        'handlers': ['console'],
        'level': LOG_LEVEL,
    },
}

# -------------------------
# Additional notes: DB client
# -------------------------
# Make sure you have mysqlclient installed in your environment (requirements.txt).
# For Alpine/slim images, you may need system libs: libmariadb-dev-compat, build-essential, etc.
