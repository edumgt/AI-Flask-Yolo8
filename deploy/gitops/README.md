# GitOps Environment Profiles

이 디렉터리는 배포 목표 상태를 Git으로 관리하기 위한 GitOps 선언 파일입니다.

- `environments/local.json`: 로컬 검증용 수동 실행 프로파일
- `environments/dev.json`: `develop` 브랜치 배포 대상
- `environments/prod.json`: `main` 브랜치 배포 대상

각 파일의 핵심 필드:
- `environment`: 환경명 (`local`/`dev`/`prod`)
- `branch`: 해당 환경에서 허용하는 Git 브랜치
- `aws_region`: 배포 대상 AWS 리전
- `codepipeline_name`: 실행할 CodePipeline 이름
- `wait_for_completion`: 파이프라인 완료 대기 여부

권장 변경 흐름:
1. 환경 파일 수정 후 Pull Request 생성
2. 리뷰/승인 후 머지
3. GitHub Actions가 GitOps 목표 상태를 읽어 CodePipeline 실행
