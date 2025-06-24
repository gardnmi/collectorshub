from pathlib import Path
from decouple import config
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")
OPENAI_API_KEY = config("OPENAI_API_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=True, cast=bool)
CSRF_TRUSTED_ORIGINS = [f"https://{config('HOST')}"]

ALLOWED_HOSTS = ["localhost", "127.0.0.1", config("HOST")]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Application definition

INSTALLED_APPS = [
    # 3rd Party apps
    "unfold",  # before django.contrib.admin
    # Default Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # My apps
    "a_collectibles",
    "a_accounts",
    "a_wishlist",
    "a_core",
    "a_messaging",
    # 3rd Party apps
    "django_extensions",  # For additional management commands and features
    "django_cotton",
    "django_vite",
    "allauth_ui",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "widget_tweaks",
    "slippers",
    "django.contrib.humanize",  # For human-friendly template filters
    "django_cleanup.apps.CleanupConfig", # Should be last in INSTALLED_APPS 
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # 3rd Party apps
    "django_htmx.middleware.HtmxMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",    
]

ROOT_URLCONF = "a_core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],  # new
        "APP_DIRS": True,  # removed per requirement of django_components
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # `allauth` needs this from django
                "django.template.context_processors.request",
                "a_messaging.context_processors.unread_message_count",
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by email
    "allauth.account.auth_backends.AuthenticationBackend",
]


WSGI_APPLICATION = "a_core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases


if config("DATABASE", default='neon', cast=str) == 'neon':
    DATABASES = {
        "default": dj_database_url.parse(
            config("NEON_CONNECTION_STRING", cast=str, ) # type: ignore
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "assets",  # Directory for static files
    BASE_DIR / "static",  # Ensure the 'static' directory is included
]

STATIC_ROOT = BASE_DIR / "staticfiles"  # Directory where static files will be collected

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": config("AWS_ACCESS_KEY_ID"),
            "secret_key": config("AWS_SECRET_ACCESS_KEY"),
            "bucket_name": config("AWS_STORAGE_BUCKET_NAME"),
            "custom_domain": config("AWS_S3_CUSTOM_DOMAIN"),
            "cloudfront_key_id": config("AWS_CLOUDFRONT_KEY_ID"),
            "cloudfront_key": config("AWS_CLOUDFRONT_KEY", cast=str).replace("\\n", "\n").encode("ascii").strip(), # type: ignore
            }
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },  
}
# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django AllAuth Settings
LOGIN_REDIRECT_URL = "profile"
# ACCOUNT_EMAIL_REQUIRED = True  # Deprecated, replaced below
ACCOUNT_EMAIL_VERIFICATION = "none"  # Can be 'mandatory', 'optional', or 'none'
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']

# 3rd Party Apps Settings
DJANGO_VITE = {"default": {"dev_mode": DEBUG}}

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        "APP": {"client_id": "123", "secret": "456", "key": ""}
    }
}

# settings.py
ALLAUTH_UI_THEME = "light"
