# Flask-YOLO8 영상 분석 시스템

Flask와 YOLOv8을 사용해 이미지/영상 속 객체를 탐지하고, 결과를 저장·조회할 수 있는 웹 애플리케이션입니다.

## ✨ 한눈에 보는 핵심 기능

| 기능 | 설명 | 사용자 이점 |
|---|---|---|
| 사용자 인증 | 회원가입, 로그인, 로그아웃, 세션 기반 접근 제어 | 내 분석 이력과 결과를 계정 단위로 안전하게 관리 |
| 파일 업로드 | 이미지(`jpg`, `jpeg`, `png`) 및 영상(`mp4`, `avi`, `mov`) 업로드 | 다양한 입력 포맷을 바로 분석 가능 |
| 샘플 데이터 | 기본 샘플 이미지/영상 제공 | 테스트 파일 없이 즉시 데모 가능 |
| AI 분석 | YOLOv8 기반 객체 탐지 수행 | 객체 종류/탐지 결과를 자동으로 확인 |
| 결과 관리 | 분석 이력 조회 및 결과 다운로드 | 반복 분석/비교 및 결과 보관이 쉬움 |
| 실시간 상태 확인 | Ajax 기반 처리 상태 폴링 | 긴 영상 분석도 진행 상황을 즉시 확인 |

## 🧱 기술 스택

- **백엔드**: Flask, SQLAlchemy, Flask-Migrate
- **AI/ML**: Ultralytics (YOLOv8)
- **프론트엔드**: Jinja2, Bootstrap, JavaScript
- **데이터베이스**: SQLite
- **보안**: Werkzeug(비밀번호 해시), Flask-Session
- **스토리지**: S3 연동 유틸리티 기반 파일 관리

## 🗂️ 프로젝트 구조

```text
flask-yolo8/
├── app.py                 # Flask 앱 진입점
├── config.py              # 환경설정
├── models.py              # 데이터베이스 모델
├── requirements.txt       # 의존성 목록
├── yolov8n.pt             # YOLOv8 모델 파일
├── routes/                # 라우트 (블루프린트)
├── templates/             # Jinja2 템플릿
├── static/                # 정적 파일 (CSS, 업로드, 결과)
├── samples/               # 샘플 이미지/비디오
├── utils/                 # 유틸리티 함수
├── migrations/            # 데이터베이스 마이그레이션
└── docs/                  # 프로젝트 문서
```

## 📘 문서

프로젝트 상세 문서는 아래를 참고하세요.

- **[프로젝트 구조](./docs/project-structure.md)**: 폴더/파일 구성과 책임
- **[코드 흐름](./docs/code-flow.md)**: 앱 초기화부터 분석 완료까지 실행 흐름
- **[데이터 흐름](./docs/data-flow.md)**: 업로드 → 분석 → 저장/조회 데이터 경로
- **[API 명세서](./docs/api-spec.md)**: 주요 API 엔드포인트 및 요청/응답

## ⚙️ 설정

주요 설정은 `config.py`에서 관리됩니다.

- `SECRET_KEY`: 세션 보안 키
- `SQLALCHEMY_DATABASE_URI`: 데이터베이스 연결 문자열
- `UPLOAD_FOLDER`: S3 업로드 경로(prefix)
- `RESULT_FOLDER`: S3 결과 경로(prefix)
- `SAMPLE_FOLDER`: 샘플 파일 경로

### 🔒 민감정보 마스킹 가이드

README/문서/로그에 아래 항목이 노출되지 않도록 마스킹하세요.

- `SECRET_KEY`
- DB 계정 정보(아이디/비밀번호/호스트)
- AWS Access Key / Secret Key / Session Token
- 외부 API Key, OAuth Client Secret

예시(마스킹):

```env
SECRET_KEY=********
SQLALCHEMY_DATABASE_URI=postgresql://db_user:********@db-host:5432/db_name
AWS_ACCESS_KEY_ID=AKIA************
AWS_SECRET_ACCESS_KEY=********************************
```

> 권장: 민감정보는 `.env` 또는 배포 환경 변수로만 주입하고, 저장소에는 커밋하지 않습니다.

## 🚀 사용법

1. **회원가입/로그인**: 계정을 생성하고 로그인합니다.
2. **파일 선택**: 새 파일 업로드 또는 샘플 파일을 선택합니다.
3. **분석 실행**: "분석 시작" 버튼으로 YOLO 분석을 실행합니다.
4. **결과 확인**: 결과 페이지에서 탐지 결과를 조회/다운로드합니다.

## 🛡️ 보안

- 비밀번호는 Werkzeug 기반 해시로 저장
- 업로드 파일 확장자 화이트리스트 검증
- 세션 기반 인증으로 사용자 접근 제어
- 파일명 정규화(보안 처리) 적용
