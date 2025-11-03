from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers

# 예시용 Serializer
# class ExampleSerializer(serializers.ModelSerializer):
#     """
#     예시용 Serializer - 실제 사용시 주석 해제하고 수정
#     """
#     class Meta:
#         # model = ExampleModel
#         # fields = '__all__'
#         pass


# 기본 응답 Serializer
@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "정상 응답 예시",
            summary="서버가 정상적으로 작동 중",
            description="API 서버가 정상적으로 작동하고 있을 때의 응답",
            value={"status": "ok", "message": "Django API server is running!"},
            response_only=True,
        ),
    ]
)
class HealthCheckSerializer(serializers.Serializer):
    """
    헬스 체크 응답용 Serializer
    """

    status = serializers.CharField(help_text="서버 상태 (ok/error)")
    message = serializers.CharField(help_text="상태 메시지")


# ViewSet 예시용 Serializer (주석 처리)
# @extend_schema_serializer(
#     examples=[
#         OpenApiExample(
#             "생성 예시",
#             summary="새 항목 생성",
#             description="새로운 항목을 생성하는 예시",
#             value={
#                 "title": "예시 제목",
#                 "content": "예시 내용",
#             },
#             request_only=True,
#         ),
#         OpenApiExample(
#             "응답 예시",
#             summary="생성된 항목",
#             description="생성된 항목의 응답 예시",
#             value={
#                 "id": 1,
#                 "title": "예시 제목",
#                 "content": "예시 내용",
#                 "created_at": "2024-01-01T00:00:00Z",
#             },
#             response_only=True,
#         ),
#     ]
# )
# class ExampleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ExampleModel
#         fields = '__all__'
