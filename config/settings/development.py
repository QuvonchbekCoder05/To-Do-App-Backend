from .base import * # noqa

from datetime import timedelta
import environ


env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

ALLOWED_HOSTS = ["*"]

DEBUG = env('DEBUG')

INTERNAL_IPS = ["127.0.0.1"]

INSTALLED_APPS += ["debug_toolbar"]  # noqa: F405

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa: F405

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",
    }
}

AUTH_USER_MODEL = env('AUTH_USER_MODEL')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')



SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=10),
    'AUTH_TOKEN_CLASSES':('rest_framework_simplejwt.tokens.AccessToken')
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny'
    )
}

# The line `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'` in the Django settings
# file is configuring the email backend to use the console backend.
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


