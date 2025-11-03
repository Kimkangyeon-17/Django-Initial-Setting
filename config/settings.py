from pathlib import Path

from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", default="django-insecure-change-me-in-production")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,127.0.0.1").split(",")

# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "corsheaders",
    "drf_spectacular",  # API 문서화
]

# 개발 환경에서만 추가되는 앱
if DEBUG:
    THIRD_PARTY_APPS += [
        "debug_toolbar",  # Django Debug Toolbar (개발용)
    ]

LOCAL_APPS = [
    # 여기에 앱들을 추가하세요
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# 개발 환경에서만 Debug Toolbar 미들웨어 추가
if DEBUG:
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
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
LANGUAGE_CODE = "ko-kr"
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    # drf-spectacular 설정
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# drf-spectacular 설정
SPECTACULAR_SETTINGS = {
    "TITLE": "Django API",
    "DESCRIPTION": "Django REST Framework API 문서",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    # Swagger UI 설정
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
        "displayOperationId": True,
    },
    # 인증 관련
    "COMPONENT_SPLIT_REQUEST": True,
}

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True

# Django Debug Toolbar 설정 (개발 환경에서만)
if DEBUG:
    INTERNAL_IPS = [
        "127.0.0.1",
        "localhost",
    ]

    # Debug Toolbar 패널 설정
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG,
        "SHOW_COLLAPSED": False,  # 기본적으로 펼쳐진 상태
    }

    # 표시할 패널 커스터마이징 (선택사항)
    DEBUG_TOOLBAR_PANELS = [
        "debug_toolbar.panels.history.HistoryPanel",  # 요청 히스토리
        "debug_toolbar.panels.versions.VersionsPanel",  # 버전 정보
        "debug_toolbar.panels.timer.TimerPanel",  # 타이머
        "debug_toolbar.panels.settings.SettingsPanel",  # 설정
        "debug_toolbar.panels.headers.HeadersPanel",  # 헤더
        "debug_toolbar.panels.request.RequestPanel",  # 요청
        "debug_toolbar.panels.sql.SQLPanel",  # SQL 쿼리 (가장 중요!)
        "debug_toolbar.panels.staticfiles.StaticFilesPanel",  # 정적 파일
        "debug_toolbar.panels.templates.TemplatesPanel",  # 템플릿
        "debug_toolbar.panels.cache.CachePanel",  # 캐시
        "debug_toolbar.panels.signals.SignalsPanel",  # 시그널
        "debug_toolbar.panels.redirects.RedirectsPanel",  # 리다이렉트
        "debug_toolbar.panels.profiling.ProfilingPanel",  # 프로파일링
    ]
