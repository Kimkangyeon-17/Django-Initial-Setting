# API 문서화 가이드 (drf-spectacular)

이 프로젝트는 `drf-spectacular`를 사용하여 API 문서를 자동으로 생성합니다.

## 📚 API 문서 접속하기

서버를 실행한 후 아래 주소로 접속하세요:

```bash
# 서버 실행
uv run python manage.py runserver
```

### Swagger UI (추천!)
```
http://localhost:8000/api/docs/
```
- 웹 브라우저에서 **직접 API 테스트** 가능
- 요청/응답 예시 확인
- 인증 토큰 설정 가능

### ReDoc UI
```
http://localhost:8000/api/redoc/
```
- 깔끔한 문서 형태
- 읽기 전용 (테스트 불가)

### OpenAPI Schema (JSON)
```
http://localhost:8000/api/schema/
```
- 프로그래밍 방식으로 스키마 가져오기
- API 클라이언트 자동 생성에 사용

---

## 🎯 API 문서화하는 방법

### 1. 기본 API 뷰 문서화

```python
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.decorators import api_view

@extend_schema(
    summary="사용자 목록 조회",
    description="모든 사용자의 목록을 반환합니다.",
    responses={
        200: UserSerializer(many=True),
        401: OpenApiResponse(description="인증 실패"),
    },
    tags=["Users"],  # API를 그룹화
)
@api_view(['GET'])
def user_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
```

### 2. ViewSet 문서화

```python
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

@extend_schema_view(
    list=extend_schema(
        summary="게시글 목록",
        description="모든 게시글을 페이지네이션하여 반환",
        tags=["Posts"],
    ),
    retrieve=extend_schema(
        summary="게시글 상세",
        description="특정 게시글의 상세 정보를 반환",
        tags=["Posts"],
    ),
    create=extend_schema(
        summary="게시글 생성",
        description="새로운 게시글을 생성",
        tags=["Posts"],
    ),
)
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
```

### 3. Serializer에 예시 추가

```python
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "생성 예시",
            summary="새 게시글 작성",
            description="게시글을 생성할 때 보내는 데이터",
            value={
                "title": "Django 시작하기",
                "content": "Django는 파이썬 웹 프레임워크입니다.",
                "author": 1,
            },
            request_only=True,  # 요청 예시
        ),
        OpenApiExample(
            "응답 예시",
            summary="생성된 게시글",
            description="게시글이 생성된 후 반환되는 데이터",
            value={
                "id": 1,
                "title": "Django 시작하기",
                "content": "Django는 파이썬 웹 프레임워크입니다.",
                "author": 1,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
            },
            response_only=True,  # 응답 예시
        ),
    ]
)
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
```

### 4. 커스텀 응답 문서화

```python
from drf_spectacular.utils import OpenApiResponse, OpenApiTypes

@extend_schema(
    summary="파일 업로드",
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'file': {
                    'type': 'string',
                    'format': 'binary',
                }
            }
        }
    },
    responses={
        200: OpenApiResponse(
            description="업로드 성공",
            response={
                "type": "object",
                "properties": {
                    "url": {"type": "string"},
                    "filename": {"type": "string"},
                },
            }
        ),
        400: OpenApiResponse(description="잘못된 파일 형식"),
    },
)
@api_view(['POST'])
def upload_file(request):
    # file upload logic
    pass
```

### 5. 파라미터 문서화

```python
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes

@extend_schema(
    summary="게시글 검색",
    parameters=[
        OpenApiParameter(
            name='search',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='검색어',
            required=False,
        ),
        OpenApiParameter(
            name='page',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description='페이지 번호',
            required=False,
        ),
    ],
)
@api_view(['GET'])
def search_posts(request):
    search = request.GET.get('search', '')
    # search logic
    pass
```

---

## 🎨 태그로 API 그룹화하기

API를 카테고리별로 묶어서 문서를 보기 쉽게 만들 수 있습니다:

```python
# 사용자 관련 API
@extend_schema(tags=["Users"])

# 게시글 관련 API
@extend_schema(tags=["Posts"])

# 댓글 관련 API
@extend_schema(tags=["Comments"])

# 시스템 API
@extend_schema(tags=["System"])
```

---

## 🔒 인증 문서화

인증이 필요한 API는 자동으로 문서에 표시됩니다:

```python
# settings.py에서 설정
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

# 인증 필요
@api_view(['GET'])
def protected_view(request):
    pass

# 인증 불필요
@api_view(['GET'])
@permission_classes([AllowAny])
def public_view(request):
    pass
```

---

## ⚙️ 추가 설정

### OpenAPI 스키마 다운로드
```bash
# schema.yaml 파일로 저장
uv run python manage.py spectacular --file schema.yaml --format yaml

# schema.json 파일로 저장
uv run python manage.py spectacular --file schema.json --format openapi-json
```

### 설정 커스터마이징 (settings.py)
```python
SPECTACULAR_SETTINGS = {
    'TITLE': 'My API',
    'DESCRIPTION': 'API 상세 설명',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,

    # Swagger UI 커스터마이징
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': True,
        'filter': True,  # 검색 기능
    },

    # 컴포넌트 분리
    'COMPONENT_SPLIT_REQUEST': True,

    # 태그 정렬
    'TAGS': [
        {'name': 'Users', 'description': '사용자 관련 API'},
        {'name': 'Posts', 'description': '게시글 관련 API'},
        {'name': 'System', 'description': '시스템 API'},
    ],
}
```

---

## 📖 더 알아보기

- [drf-spectacular 공식 문서](https://drf-spectacular.readthedocs.io/)
- [OpenAPI 3.0 스펙](https://swagger.io/specification/)
- [Swagger UI 데모](https://petstore.swagger.io/)

---

## 💡 팁

1. **문서부터 작성**: API를 만들 때 `@extend_schema` 데코레이터부터 작성하면 API 설계가 명확해집니다.

2. **예시 추가**: `OpenApiExample`로 요청/응답 예시를 추가하면 프론트엔드 개발자가 이해하기 쉽습니다.

3. **태그 활용**: API가 많아지면 태그로 그룹화해서 문서를 정리하세요.

4. **자동 테스트**: Swagger UI에서 직접 API를 테스트할 수 있어서 디버깅이 편합니다.

5. **팀 협업**: API 문서 URL을 팀원들과 공유하세요!
