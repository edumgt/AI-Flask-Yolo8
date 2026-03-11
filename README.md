# Flask YOLO8 Analyzer

Flask + YOLOv8 기반 이미지/영상 객체 탐지 웹 애플리케이션입니다.  
사용자는 로그인 후 파일을 업로드하거나 샘플 파일을 선택해 분석을 요청하고, 결과 상태를 조회/다운로드할 수 있습니다.

## 1) 레포 분석 요약

### 핵심 구성
- 웹 서버: `Flask` (`app.py`)
- 인증/세션: `routes/auth.py`, `Flask-Session`
- 분석 처리: `routes/main.py` + `Ultralytics YOLO`
- 데이터 저장: `SQLAlchemy` (`models.py`, 기본 SQLite)
- 파일 저장: `AWS S3` (`utils/s3_utils.py`)
- 상태 UI: `templates/results.html`에서 `/results/status` 폴링

### YOLO 처리 흐름
1. 로그인 사용자만 분석 요청 가능 (`login_required_view`)
2. 입력 파일 검증 (`jpg/jpeg/png/mp4/avi/mov`)
3. DB에 `processing` 상태 기록
4. 백그라운드 스레드에서 YOLO 실행
5. 결과 파일을 S3 업로드 후 DB 상태 갱신 (`done`/`error`)
6. 결과 화면에서 Ajax 폴링으로 상태 확인

## 2) 실행 검증 결과 (2026-03-11 기준)

### 검증 환경
- Python: `3.12.3`
- 의존성: `requirements.txt` 기준 `.venv` 설치 완료

### 실제 확인한 항목
- 의존성 import: 성공 (`flask`, `ultralytics`, `flask_sqlalchemy`, `flask_session`, `boto3`, `dotenv`)
- Flask test client 헬스체크:
  - `GET /api/health` -> `200`
  - 응답: `{"status":"ok","app_env":"local"}`
- 인증 플로우:
  - `POST /register` -> `302 /login`
  - `POST /login` -> `302 /`
- YOLO 샘플 추론:
  - 입력: `samples/highway-7213206_1280.jpg`
  - 실행 로그: `13 cars` 탐지
- 분석 요청 상태 전이:
  - 초기: `processing`
  - 이후: `error` (S3 업로드 단계에서 실패한 것으로 판단)

### 실행 가능성 결론
- 코드/의존성/YOLO 추론 자체는 동작 확인됨.
- 이 앱은 **S3 의존 구조**라서 AWS 설정 없이는 결과 완료(`done`)까지 가기 어렵고 `error`로 끝날 수 있음.
- 현재 샌드박스에서는 포트 바인딩 제한으로 실제 `0.0.0.0:8000` 리슨 검증은 제한됨.
  - Flask `test_client`로는 정상 라우팅 확인 완료.

## 3) YOLO 기반으로 할 수 있는 작업

### A. 이미지 객체 탐지
- 입력: `jpg/jpeg/png`
- 처리: `model(input_path)`로 단일 이미지 추론
- 결과: 바운딩 박스가 그려진 결과 이미지 생성 후 S3 업로드

### B. 영상 객체 탐지
- 입력: `mp4/avi/mov`
- 처리: `model.predict(source=..., save=True, ...)`로 프레임 단위 추론
- 결과: 추론 결과 영상 파일 생성 후 S3 업로드

### C. 비동기 분석 상태 관리
- 요청 직후 DB 상태를 `processing`으로 저장
- 백그라운드 완료 시 `done`/예외 시 `error` 갱신
- `/results/status`로 실시간 상태 폴링

### D. 사용자별 결과 이력 관리
- 사용자명 기준으로 결과 목록 정렬 조회
- 완료 건은 presigned URL 기반 다운로드 제공

## 4) YOLO 기반으로 확인 가능한 항목 (운영/QA 체크리스트)

### 기능 확인
- 파일 확장자 제한이 정상 동작하는지
- 파일명 정책(영문/숫자/`._-`) 위반 시 차단되는지
- 샘플 파일 선택 시 분석이 시작되는지
- 분석 상태가 `processing -> done/error`로 전이되는지

### 추론 품질 확인
- 샘플 이미지/영상에서 기대 객체가 탐지되는지
- 탐지 개수/신뢰도(confidence)가 상식적으로 타당한지
- 다양한 해상도/조명/밀집도 데이터에서 오탐/미탐 비율 추세

### 성능 확인
- 이미지 1건당 추론 시간
- 영상 길이 대비 총 처리 시간
- 동시 요청 시 스레드 기반 처리 안정성

### 저장/다운로드 확인
- S3 업로드 성공 여부
- presigned URL 다운로드 가능 여부
- 만료 시간 이후 URL 접근 차단 여부

## 5) 실행 방법

### 로컬 Python 실행
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
cp .env.local.example .env.local

# 중요: Ultralytics 설정 폴더 권한 문제가 있으면 아래 변수 지정
export XDG_CONFIG_HOME=$(pwd)/.config

APP_ENV=local FLASK_DEBUG=false python app.py
```

### Docker 실행
```bash
cp .env.local.example .env.local
docker compose --env-file .env.local up -d --build
```

중지:
```bash
docker compose down
```

## 6) 환경 변수 핵심 항목
- `APP_ENV`: `local`/`dev`/`prod`
- `FLASK_SECRET_KEY`: Flask 세션/보안 키
- `FLASK_DEBUG`: 개발 디버그 여부
- `DATABASE_URL`: 기본 `sqlite:///users.db`
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`
- `S3_BUCKET`
- `UPLOAD_FOLDER`, `RESULT_FOLDER`, `SAMPLE_FOLDER`

`.env` + `.env.{APP_ENV}` 순서로 로딩됩니다.

## 7) 현재 코드 기준 제약사항
- 결과 저장이 S3에 강하게 결합되어 있음 (로컬 fallback 없음)
- YOLO/업로드 예외가 광범위하게 `except Exception` 처리되어 원인 로그가 부족함
- 업로드 단계 일부 예외는 사용자에게 500으로 보일 수 있음
- 파일명 정책이 엄격하여 한글/공백/특수문자 파일명 업로드 불가

## 8) 권장 개선사항
- S3 실패 시 로컬 저장 fallback 추가
- 예외 로깅 강화(오류 원인/스택 추적)
- 백그라운드 작업 큐(Celery/RQ)로 전환
- `/api/health`에 DB/S3 readiness 분리 (`/api/ready`) 추가

## 9) 문서/배포 템플릿
- GitOps 프로파일: `deploy/gitops/environments/*.json`
- CI: `.github/workflows/python-app.yml`
- CD: `.github/workflows/codepipeline-full.yml`
