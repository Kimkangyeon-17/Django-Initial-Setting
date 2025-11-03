# Django Debug Toolbar 사용 가이드

Django Debug Toolbar는 개발 중에 Django의 내부 동작을 시각적으로 확인할 수 있는 강력한 디버깅 도구입니다.

## 🎯 주요 기능

### 1. **SQL 쿼리 분석** ⭐ (가장 중요!)
- 페이지 로드 시 실행된 모든 SQL 쿼리 확인
- 각 쿼리의 실행 시간 측정
- **N+1 쿼리 문제** 발견
- 중복 쿼리 확인
- 느린 쿼리 식별

### 2. **성능 측정**
- 총 페이지 로드 시간
- SQL 쿼리 실행 시간
- 템플릿 렌더링 시간
- 캐시 히트/미스 비율

### 3. **요청/응답 정보**
- HTTP 헤더
- GET/POST 파라미터
- 세션 데이터
- 쿠키 정보

### 4. **템플릿 정보**
- 사용된 템플릿 파일
- 컨텍스트 변수
- 템플릿 상속 구조

---

## 🚀 시작하기

### 1. 패키지 설치
```bash
uv sync
```

### 2. 서버 실행
```bash
uv run python manage.py runserver
```

### 3. 웹 페이지 접속
브라우저에서 Django 페이지를 열면 **오른쪽에 Debug Toolbar**가 나타납니다!

```
http://localhost:8000/admin/
http://localhost:8000/api/health/
```

---

## 📊 패널 설명

### 🔍 SQL Panel (가장 많이 사용!)

**확인할 수 있는 것:**
- 총 쿼리 개수
- 중복된 쿼리
- 비슷한 쿼리 (N+1 문제 후보)
- 각 쿼리 실행 시간

**사용 예시:**
```python
# ❌ 나쁜 예: N+1 쿼리 문제
def bad_view(request):
    posts = Post.objects.all()  # 1개 쿼리
    for post in posts:
        author = post.author  # N개 쿼리 추가 발생!
    return render(request, 'posts.html', {'posts': posts})

# ✅ 좋은 예: select_related로 최적화
def good_view(request):
    posts = Post.objects.select_related('author').all()  # 1개 쿼리로 해결!
    return render(request, 'posts.html', {'posts': posts})
```

**Debug Toolbar에서 확인:**
- 나쁜 예: 101개 쿼리 (1 + 100)
- 좋은 예: 1개 쿼리

---

### ⏱️ Timer Panel

**페이지 로딩 시간 분석:**
- 총 실행 시간
- SQL 시간
- Python 시간
- 템플릿 렌더링 시간

**최적화 팁:**
- SQL 시간이 너무 많으면 → 쿼리 최적화 필요
- Python 시간이 많으면 → 로직 최적화 필요
- 템플릿 시간이 많으면 → 템플릿 간소화 필요

---

### 📋 Request Panel

**확인할 수 있는 것:**
- View 함수 정보
- GET/POST 파라미터
- 세션 데이터
- 현재 사용자 정보

---

### 🎨 Templates Panel

**확인할 수 있는 것:**
- 사용된 템플릿 파일들
- 템플릿 컨텍스트 변수
- 템플릿 상속 구조

---

### 💾 Cache Panel

**확인할 수 있는 것:**
- 캐시 히트/미스 횟수
- 캐시 키 목록
- 캐시 성능 지표

---

## 🔧 실전 활용 예시

### 예시 1: N+1 쿼리 문제 찾기

**상황:**
게시글 목록 페이지가 느려요!

**Debug Toolbar 확인:**
```
SQL Panel: 501 queries in 2.5s
Similar queries: 500
```

**문제 발견:**
```python
# views.py
def post_list(request):
    posts = Post.objects.all()  # 1 query
    # 템플릿에서 post.author.name 접근할 때마다 쿼리 발생!
```

**해결:**
```python
def post_list(request):
    posts = Post.objects.select_related('author').all()  # 1 query로 해결!
```

**결과:**
```
SQL Panel: 1 query in 0.05s
```

---

### 예시 2: 중복 쿼리 제거

**Debug Toolbar 확인:**
```
SQL Panel: 10 duplicate queries
SELECT * FROM posts WHERE id = 1  (실행 10번!)
```

**문제:**
같은 데이터를 여러 번 조회

**해결:**
```python
# 한 번만 조회하고 재사용
post = Post.objects.get(id=1)
# post를 여러 곳에서 사용
```

또는 캐싱 사용:
```python
from django.core.cache import cache

post = cache.get('post_1')
if not post:
    post = Post.objects.get(id=1)
    cache.set('post_1', post, 300)  # 5분 캐싱
```

---

### 예시 3: 느린 쿼리 최적화

**Debug Toolbar 확인:**
```
SQL Panel:
SELECT * FROM posts ORDER BY created_at DESC  (1.2s)
```

**해결:**
```python
# 1. 인덱스 추가
class Post(models.Model):
    created_at = models.DateTimeField(db_index=True)

# 2. 필요한 필드만 가져오기
posts = Post.objects.only('id', 'title', 'created_at').all()

# 3. 페이지네이션 추가
from rest_framework.pagination import PageNumberPagination
```

---

## ⚙️ 설정 커스터마이징

### 특정 페이지에서만 표시
```python
# settings.py
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: request.user.is_staff,
}
```

### 필요한 패널만 표시
```python
# settings.py
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.sql.SQLPanel',  # SQL만
    'debug_toolbar.panels.timer.TimerPanel',  # 타이머만
]
```

### 느린 쿼리 강조
```python
# settings.py
DEBUG_TOOLBAR_CONFIG = {
    'SQL_WARNING_THRESHOLD': 100,  # 100ms 이상 걸리는 쿼리 경고
}
```

---

## 🎓 최적화 체크리스트

### SQL 쿼리 최적화
- [ ] N+1 쿼리 문제 확인
- [ ] `select_related()` / `prefetch_related()` 사용
- [ ] 중복 쿼리 제거
- [ ] 인덱스 추가
- [ ] 필요한 필드만 조회 (`only()`, `values()`)

### 성능 최적화
- [ ] 페이지 로드 시간 < 1초
- [ ] SQL 쿼리 개수 < 50개
- [ ] 느린 쿼리 없음 (< 100ms)
- [ ] 캐싱 활용

---

## 💡 유용한 팁

### 1. API 개발 시 활용
REST API를 개발할 때도 Debug Toolbar를 사용할 수 있어요!

```python
# DRF ViewSet
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('author').prefetch_related('comments')
    serializer_class = PostSerializer
```

Swagger UI(`/api/docs/`)에서 API를 호출하면 Debug Toolbar로 쿼리를 확인할 수 있어요!

### 2. 쿼리 실행 계획 확인
```python
# SQL Panel에서 EXPLAIN을 볼 수 있어요
# 쿼리 최적화에 도움이 됩니다
```

### 3. 히스토리 패널 활용
여러 페이지를 이동하면서 쿼리 개수를 비교할 수 있어요.

---

## ⚠️ 주의사항

### 1. 프로덕션에서는 절대 사용 금지!
```python
# settings.py에서 자동으로 처리됨
if DEBUG:  # DEBUG=False면 자동으로 비활성화
    INSTALLED_APPS += ['debug_toolbar']
```

### 2. 성능 오버헤드
Debug Toolbar 자체가 약간의 성능 오버헤드를 발생시킵니다.
개발 중에만 사용하세요!

### 3. INTERNAL_IPS 설정
Docker를 사용하는 경우 추가 설정이 필요할 수 있어요:
```python
import socket
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]
```

---

## 📖 더 알아보기

- [Django Debug Toolbar 공식 문서](https://django-debug-toolbar.readthedocs.io/)
- [Django 쿼리 최적화 가이드](https://docs.djangoproject.com/en/stable/topics/db/optimization/)
- [select_related vs prefetch_related](https://docs.djangoproject.com/en/stable/ref/models/querysets/#select-related)

---

## 🎯 실전 연습

### 연습 1: 쿼리 개수 세기
1. 서버 실행
2. 페이지 접속
3. Debug Toolbar의 SQL Panel 확인
4. 쿼리 개수가 몇 개인가요?

### 연습 2: N+1 문제 찾기
1. "Similar queries" 항목 확인
2. 같은 패턴의 쿼리가 여러 번 실행되나요?
3. `select_related()` 또는 `prefetch_related()` 사용해서 최적화

### 연습 3: 느린 쿼리 찾기
1. 실행 시간이 100ms 이상인 쿼리 찾기
2. 왜 느린지 분석 (EXPLAIN 확인)
3. 인덱스 추가 또는 쿼리 개선

---

Debug Toolbar는 Django 개발자의 필수 도구입니다!
적극적으로 활용해서 빠르고 효율적인 API를 만드세요! 🚀
