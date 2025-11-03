from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


# 헬스 체크용 뷰 (서버가 잘 돌아가는지 확인)
@extend_schema(
    summary="헬스 체크",
    description="API 서버의 상태를 확인하는 엔드포인트입니다.",
    responses={
        200: OpenApiResponse(
            description="서버 정상 작동",
            response={
                "type": "object",
                "properties": {
                    "status": {"type": "string", "example": "ok"},
                    "message": {
                        "type": "string",
                        "example": "Django API server is running!",
                    },
                },
            },
        )
    },
    tags=["System"],
)
@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    """
    API 서버 상태 확인용 엔드포인트
    """
    return Response(
        {"status": "ok", "message": "Django API server is running!"},
        status=status.HTTP_200_OK,
    )


# 예시용 ViewSet (나중에 실제 모델로 교체)
# ViewSet을 사용하려면 아래 주석을 해제하고 필요한 import를 추가하세요:
# from rest_framework import viewsets
# from .serializers import ExampleSerializer
# from .models import ExampleModel
#
# class ExampleViewSet(viewsets.ModelViewSet):
#     """
#     예시용 ViewSet - 실제 사용시 주석 해제하고 수정
#     """
#     queryset = ExampleModel.objects.all()
#     serializer_class = ExampleSerializer
