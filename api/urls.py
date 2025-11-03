from django.urls import include, path

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter

from . import views

# DRF Router 설정
router = DefaultRouter()
# router.register(r'example', views.ExampleViewSet)  # 예시용 - 나중에 활성화

urlpatterns = [
    # API root
    path("", include(router.urls)),
    # 커스텀 API 엔드포인트들
    path("health/", views.health_check, name="health_check"),
    # API 문서화 (drf-spectacular)
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    # Swagger UI
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    # ReDoc UI
    path(
        "redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # 인증 관련 (필요시 추가)
    # path('auth/', include('rest_framework.urls')),
]
