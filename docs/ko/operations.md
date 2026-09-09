# 운영, 백업과 업데이트

> 목표 버전 0.6.0의 준비 작업 G0입니다. HTTP API는 `/api/v1`이며 공통 `Client` 계약을 `LocalClient`와 `RestClient`가 구현합니다. 데이터베이스 스키마 8과 확장 ABI 2는 그대로입니다. 기존 `/api/...` 경로는 404를 반환합니다. 서버, 데스크톱, 포털 및 프록시를 함께 업데이트하십시오. 아래 기능 설명은 0.5.0 기준에서 작성되었으며 이 안내로 변경된 부분 외에는 계속 적용됩니다. ABI V3 및 일곱 UI 언어를 포함한 Core Foundation II는 아직 완료되지 않았습니다.


[시작 페이지](README.md) · [설치](installation.md)

서비스 계정, 프로그램, 모듈과 데이터 폴더를 분리합니다. 포털 사용자가 모듈
폴더에 쓰지 못하게 합니다. 백업에는 개인 데이터, 파일과 비밀번호 해시가
있으므로 접근과 저장 위치를 보호합니다. `scripts/pilot-*.py`는 구현 패키지의
도구이며 이 공개 저장소에는 포함되지 않습니다. Python 3.11 이상이 필요합니다.

> Windows 빌드와 PostgreSQL 복구에는 추가로 수정 커밋 `6ebb363ec28ab8631fb82a88051351f87659b523`가 필요합니다. Windows SDK 심볼을 `LOAD_LIBRARY_SEARCH_DEFAULT_DIRS`로 수정하고 `pg_restore`의 SQL 출력에 `--file=-`를 추가합니다. 이 수정은 스키마나 API를 변경하지 않습니다. 덤프 출력이 검색 경로를 비우므로 세션을 취소하기 전에 설정된 검색 경로도 복원합니다. 회귀 테스트는 세션 취소 실패 시 복원된 테이블도 함께 롤백되는지 확인합니다.

## SQLite

```sh
python3 scripts/pilot-data.py backup data.sqlite backup-2026-09-09
python3 scripts/pilot-data.py diagnose backup-2026-09-09/database.sqlite
python3 scripts/pilot-data.py restore backup-2026-09-09 restored.sqlite
```

온라인 백업은 확정된 WAL 데이터도 포함합니다. 대상 폴더는 없어야 합니다.
무결성, 외래 키, 마이그레이션 순서와 SHA-256을 검사합니다. 실패 시 불완전한
폴더가 남을 수 있으며 유효한 매니페스트 없이 복구 가능한 백업으로 보아서는 안 됩니다.

복원은 **새** 데이터베이스 파일을 요구하고 내용을 확인한 뒤 이전 세션을
무효화합니다. 호스트를 멈춘 다음 검증된 파일로 경로를 변경합니다. 업무 확인이
끝날 때까지 이전 파일을 보관합니다. 첨부파일은 포함되지만 프로그램, 모듈,
인증서와 설정은 별도로 복구할 수 있어야 합니다.

## PostgreSQL

서버와 호환되는 `pg_dump`, `pg_restore`, `psql`을 사용합니다. `pg_service.conf`,
`.pgpass` 또는 보호된 libpq 설정을 준비합니다. 별도 서비스 설정과 새 빈 복원
대상 데이터베이스를 만들고 복원 중 다른 호스트를 연결하지 않습니다.

```sh
python3 scripts/pilot-postgres.py backup --service club-production --directory pg-backup
python3 scripts/pilot-postgres.py restore --service club-restore --directory pg-backup
```

Custom 형식 아카이브와 체크섬 매니페스트를 사용합니다. 사용자 테이블이 이미
있으면 복원을 거부합니다. 복원과 세션 폐기는 한 트랜잭션이며 기존 소유자·ACL은
옮기지 않습니다. 운영용 데이터베이스 역할을 별도로 준비하십시오. 사용 중인
운영 테이블 위에 복원하지 않습니다.

## 업데이트 절차

1. 사용자에게 알리고 작업을 마친 뒤 백업합니다.
2. 새 실행 파일과 호환 모듈을 별도 버전 폴더에 둡니다.
3. 새 테스트 데이터베이스에 복원하고 새 호스트로 마이그레이션을 검사·적용합니다.
4. 로그인, 수정, 회원 소속, 승급, 파일, CSV, PDF를 제한 계정까지 포함해 확인합니다.
5. 운영 호스트를 멈추고 인수 완료 후 프로그램·설정과 대응하는 포털 파일을 전환합니다.
6. 브라우저를 새로 고치고 로그인하여 업무 데이터를 확인합니다.
7. 롤백 시 이전 프로그램과 **해당 마이그레이션 전의 호환 백업**을 함께 사용합니다.

마이그레이션된 데이터베이스를 이전 실행 파일로 열면 안 됩니다. 백업 이후
변경이 롤백으로 사라질 수 있으므로 먼저 처리 방침을 정합니다. 업데이트 검색은
설치를 수행하지 않습니다. 서명, 공증, 전체 배포는 별도 출시 단계입니다.

## 진단과 문제 대응

`clubplatform-server --sqlite TESTFILE --diagnose`는 개인 정보 없이 연결과
스키마를 표시합니다. 호스트를 열면 마이그레이션을 검사할 뿐 아니라 **적용**합니다.
마이그레이션 없이 SQLite만 검사하려면 `pilot-data.py diagnose`를 사용합니다.
지원 요청에는 버전, 방식, 시간과 오류를 기록하되 비밀번호·토큰은 넣지 않습니다.

Git 추적 정보가 없으면 올바른 브랜치를 선택하고 한 번
`git branch --set-upstream-to=origin/feature/core-foundation feature/core-foundation`을
실행한 뒤 `git pull --ff-only`를 사용합니다. 강제 reset으로 로컬 변경을 지우지
않습니다. `403`은 역할과 프록시·출처를 함께 확인합니다. 모듈 누락은 경로,
CPU, ABI, 저장된 매니페스트와 활성화를 확인하고 마이그레이션 테이블이나
매니페스트를 직접 고쳐 검사를 우회하지 마십시오.
