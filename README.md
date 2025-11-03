# Django + DRF Template

Django와 Django REST Framework를 사용한 백엔드 개발을 위한 템플릿 프로젝트입니다.

## 🛠️ 기술 스택

- **Python**: 3.13
- **Django**: 최신 버전
- **Django REST Framework**: REST API 개발
- **UV**: 패키지 관리 및 가상환경
- **SQLite**: 기본 데이터베이스 (변경 가능)

## 📦 포함된 패키지

### 메인 패키지
- `django`: Django 웹 프레임워크
- `djangorestframework`: REST API 구축
- `django-cors-headers`: CORS 처리
- `python-decouple`: 환경변수 관리
- `pillow`: 이미지 처리
- `drf-spectacular`: API 자동 문서화 (Swagger/ReDoc)

### 개발용 패키지
- `black`: 코드 포맷터
- `flake8`: 코드 린터
- `isort`: import 정렬
- `pytest`: 테스트 프레임워크
- `pytest-django`: Django용 pytest 플러그인
- `pre-commit`: Git 커밋 전 자동 코드 검사

## 🚀 빠른 시작

### 1. 레포지토리 복제
```bash
git clone <your-template-repo-url> my-new-project
cd my-new-project
```

### 2. 환경변수 설정
```bash
# .env.example을 복사하여 .env 파일 생성
cp .env.example .env

# .env 파일을 열어서 필요한 값들을 수정하세요
# 최소한 SECRET_KEY는 새로운 키로 변경해야 합니다
```

**.env 파일 예시:**
```env
DEBUG=True
SECRET_KEY=your-new-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

**SECRET_KEY 생성 방법:**
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 3. 의존성 설치 및 서버 실행
```bash
# 패키지 설치
uv sync

# Pre-commit 설치 (최초 1회만)
uv run pre-commit install

# 마이그레이션
uv run python manage.py migrate

# 슈퍼유저 생성 (선택사항)
uv run python manage.py createsuperuser

# 개발 서버 실행
uv run python manage.py runserver
```

## 🎯 Pre-commit 설정

### Pre-commit이란?
Git 커밋하기 전에 자동으로 코드를 검사하고 포맷팅하는 도구입니다.

### 설치 방법
```bash
# 1. pre-commit 설치 (최초 1회)
uv run pre-commit install

# 2. 모든 파일에 대해 한 번 실행해보기 (선택사항)
uv run pre-commit run --all-files
```

### 동작 방식
Git 커밋할 때 자동으로 다음 작업들을 수행합니다:
- ✅ **Black**: 코드 자동 포맷팅
- ✅ **isort**: import 문 자동 정렬
- ✅ **Flake8**: 코드 스타일 체크
- ✅ **기본 체크**: 파일 끝 공백, 큰 파일, YAML/JSON 문법 등

### 사용 예시
```bash
# 일반적인 커밋 (자동으로 pre-commit 실행됨)
git add .
git commit -m "feat: 새 기능 추가"

# 특정 파일만 체크
uv run pre-commit run --files api/views.py

# 모든 파일 체크 (커밋 없이)
uv run pre-commit run --all-files

# Pre-commit 훅 업데이트
uv run pre-commit autoupdate
```

### Pre-commit 건너뛰기 (비추천)
```bash
# 특별한 경우에만 사용
git commit -m "메시지" --no-verify
```

## 📁 프로젝트 구조

```
project/
├── config/             # Django 설정
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── api/                # API 관련 파일들
│   ├── urls.py
│   ├── views.py
│   └── serializers.py
├── apps/               # Django 앱들을 여기에 생성
├── static/             # 정적 파일
├── media/              # 업로드된 미디어 파일
├── templates/          # Django 템플릿
├── .env                # 환경변수 (Git에 포함되지 않음)
├── .env.example        # 환경변수 템플릿 (Git에 포함)
├── .pre-commit-config.yaml  # Pre-commit 설정
├── .flake8             # Flake8 설정
├── pyproject.toml      # UV 프로젝트 설정
├── README.md
└── API_DOCUMENTATION_GUIDE.md  # API 문서화 가이드
```

## 🔧 개발 도구

### 코드 포맷팅
```bash
# Black으로 자동 포맷팅
uv run black .

# isort로 import 정렬
uv run isort .
```

### 코드 린팅
```bash
# Flake8으로 코드 스타일 체크
uv run flake8
```

### 테스트 실행
```bash
# 모든 테스트 실행
uv run pytest

# 특정 테스트 파일만 실행
uv run pytest tests/test_api.py

# 커버리지와 함께 실행
uv run pytest --cov
```

## 📝 새 앱 추가하기

```bash
# 새 Django 앱 생성
uv run python manage.py startapp myapp apps/myapp

# settings.py의 LOCAL_APPS에 추가
LOCAL_APPS = [
    'apps.myapp',
]
```

## 🌐 API 엔드포인트

### 기본 엔드포인트
- `/api/` - API 루트
- `/api/health/` - 헬스 체크
- `/admin/` - Django 관리자

### API 문서 (drf-spectacular)
- `/api/docs/` - **Swagger UI** (추천! 웹에서 API 테스트 가능)
- `/api/redoc/` - **ReDoc UI** (깔끔한 문서 뷰)
- `/api/schema/` - OpenAPI 3.0 스키마 (JSON)

#### API 문서 사용법
1. 서버 실행: `uv run python manage.py runserver`
2. 브라우저에서 접속: `http://localhost:8000/api/docs/`
3. Swagger UI에서 바로 API 테스트 가능!

#### API 문서화 방법
```python
from drf_spectacular.utils import extend_schema, OpenApiResponse

@extend_schema(
    summary="API 요약",
    description="API 상세 설명",
    responses={200: YourSerializer},
    tags=["카테고리"],
)
@api_view(['GET'])
def your_api(request):
    # your code
    pass
```

## 🔒 보안 설정

프로덕션 환경에서는 다음 사항들을 확인하세요:

1. `DEBUG=False`로 설정
2. `SECRET_KEY` 새로 생성
3. `ALLOWED_HOSTS` 적절히 설정
4. 데이터베이스 설정 변경
5. HTTPS 설정

## 💡 개발 팁

### VS Code 추천 익스텐션
- Python
- Pylance
- Django
- GitLens
- Better Comments

### VS Code 설정 (.vscode/settings.json)
```json
{
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  }
}
```

## 📚 추가 리소스

- [Django 공식 문서](https://docs.djangoproject.com/)
- [Django REST Framework 문서](https://www.django-rest-framework.org/)
- [UV 공식 문서](https://docs.astral.sh/uv/)
- [Pre-commit 공식 문서](https://pre-commit.com/)

## 🤝 기여하기

버그 리포트나 기능 제안은 이슈로 등록해주세요.

## 📄 라이센스

MIT License
