# 운영과 통합

## 로컬 테스트

명령은 문서 저장소가 아니라 비공개 프로그램 저장소에서 실행합니다. Qt, ICU, libxml2 등 의존성이 설정된 macOS 프리셋과 Node.js 22.12 이상의 22 버전이 필요합니다. 새 테스트 데이터베이스에서 `--init admin`을 한 번만 실행하고 암호를 입력합니다. 첫 터미널의 서버를 유지하고 프로젝트 루트에서 새 터미널을 열어 두 번째 명령 블록을 실행합니다. 각 프로세스는 Ctrl+C로 종료합니다. 테스트 데이터는 기존 데스크톱 데이터와 분리됩니다.

```bash
cmake --preset user-macos-vscode-debug
cmake --build --preset user-macos-vscode-debug --parallel
mkdir -p build/portal-test
./build/user-macos-vscode-debug/apps/server/clubplatform-server \
  --sqlite build/portal-test/data.sqlite --init admin
./build/user-macos-vscode-debug/apps/server/clubplatform-server \
  --sqlite build/portal-test/data.sqlite \
  --extensions "$PWD/build/user-macos-vscode-debug/runtime-extensions" \
  --port 8080 --portal-origin http://127.0.0.1:5173
```

```bash
cd apps/portal
npm ci
npm run dev -- --port 5173 --strictPort
```

http://127.0.0.1:5173

## 인증과 배포

`POST /api/v1/auth/login`에 `{"login":"…","password":"…"}`를 보내면 `token`, `user_id`, `login`, `expires_at`을 받습니다. 이후 `Authorization: Bearer <token>`을 사용하고 토큰은 메모리에만 보관합니다. `GET /api/v1/auth/me`는 세션을 확인하고 `POST /api/v1/auth/logout`은 취소합니다. 기본 제한은 최대 8시간, 미사용 30분이며 로그인 5회 실패 후 30초 잠금입니다. 서버는 권한과 모듈 상태를 검사합니다.

운영에서는 HTTPS 역방향 프록시가 포털을 제공하고 `/api/v1`을 루프백 서버로 전달합니다. `--portal-origin`은 브라우저 출처와 정확히 일치해야 합니다. Origin은 유지하고 백엔드 Host는 localhost/127.0.0.1로 지정합니다. CORS는 포털의 암호학적 인증이 아니며 일반 클라이언트는 Origin을 생략할 수 있습니다. mTLS/BFF는 아직 구현되지 않았습니다. JavaScript에 비밀 키를 넣지 마세요.

## 라이선스와 모듈

1. 게시자와 활성화 키 쌍을 저장소 밖에서 생성하고 개인 키를 보호합니다.
2. HTTPS 뒤에 활성화 서비스를 배포합니다. [운영자 안내](../../tools/activation/README.md).
3. 모듈, 사용자 제한, 유효 기간과 활성화 정책을 지정합니다. Banking에는 `finance`, `banking`이 모두 필요합니다.
4. 게시자 키로 서명하고 서비스에 등록합니다. 공개 키와 서명 파일만 배포합니다.
5. 운영 패키지에는 저장소 변수 `CLUBPLATFORM_PINNED_LICENSE_KEY`를 설정합니다. 개발용 기존 라이선스는 운영 복사 방지가 아닙니다.
6. 라이선스를 가져와 활성화하고 모듈을 설치 및 활성화합니다. 포털에서는 브라우저별이 아니라 서버 설치가 연결됩니다.
7. 이전 설치를 해제하고 새 호스트에서 다시 활성화합니다. 오프라인 발급은 정책에서 허용해야 합니다. 오프라인 취소는 임대 만료까지 지연될 수 있습니다.

스키마 18은 은행, 17은 활성화, 16은 통화, 15는 사용자/개인 연결, 14는 일정/행사입니다. 업그레이드 전에 서버를 중지하고 백업을 검증한 후 호환 버전을 배포합니다. 다른 호스트 복원은 활성화를 대신하지 않습니다.

## API와 SDK

[API 목록](../api/overview.md)을 참고하세요. 금액은 최소 통화 단위의 정수 문자열입니다. 리비전과 원본 ID는 변경 및 재시도를 보호합니다. 은행 가져오기는 미리보기와 승인이 필요합니다. [계약](../banking.md).

ABI V3는 C 인터페이스와 매니페스트를 사용합니다. 네이티브 확장은 프로세스 안의 신뢰 코드이며 샌드박스가 아닙니다. 저장과 권한 검사는 호스트가 담당합니다. [V3](../extension-v3.md), [자리표시자](placeholders.md), [검증 상태](../status.md)를 참고하세요.

