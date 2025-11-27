from pathlib import Path
import os
import dj_database_url  # Thư viện parse DATABASE_URL

# --- ĐƯỜNG DẪN CƠ BẢN ---
BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================================
# --- BẢO MẬT & MÔI TRƯỜNG CHẠY ---
# ==========================================================

# SECRET_KEY: lấy từ biến môi trường nếu có, nếu không dùng key local (dev)
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-change-me-please-before-deployment'
)

# DEBUG: True nếu chạy local, False khi deploy Production
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# ALLOWED_HOSTS
ALLOWED_HOSTS = os.environ.get('WEB_HOST', '127.0.0.1,localhost').split(',')

# --- CÁC APP ĐÃ CÀI ĐẶT ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',  # App của bạn
]

# --- MIDDLEWARE ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # cho static files production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

# --- TEMPLATES ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Thư mục templates
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

WSGI_APPLICATION = 'mysite.wsgi.application'

# ==========================================================
# --- CẤU HÌNH DATABASE ---
# ==========================================================

DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Production: PostgreSQL
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            conn_health_check=True
        )
    }
else:
    # Local: SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# --- MẬT KHẨU ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- QUỐC TẾ HÓA ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ==========================================================
# --- STATIC FILES ---
# ==========================================================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise: nén và cache static files (production)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ==========================================================
# --- CẤU HÌNH RIÊNG CHO GAME ---
# ==========================================================
X_FRAME_OPTIONS = 'SAMEORIGIN'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- LOGIN ---
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/game/'
LOGOUT_REDIRECT_URL = '/login/'
