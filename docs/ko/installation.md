# 설치와 초기 설정

[시작 페이지](README.md) · [운영과 복원](operations.md)

기존 설치를 변경하기 전에 검증된 백업을 만드십시오. 데이터, 설정, 프로그램은
분리하고 예제 경로를 실제 환경에 맞게 바꾸십시오. 운영 데이터베이스에서
스모크 테스트를 실행하면 안 됩니다.

압축 패키지는 범용 설치 프로그램이 아닙니다. 운영체제 라이브러리와 데스크톱용
Qt 런타임이 필요합니다. 제품의 배포 옵션으로 Qt를 포함할 수 있습니다.
애플리케이션 빌드 명령은 구현 저장소 접근 권한을 전제로 하며, 공개 문서
저장소에는 비공개 애플리케이션 코드가 없습니다.

## 개발 환경

| 시스템 | 프로젝트 기준 |
|---|---|
| Windows | Visual Studio 2026, Qt용 MSVC v143/14.44와 Qt 6.11.2 `msvc2022_64`, 선택적 IncrediBuild |
| macOS | 전체 Xcode, Apple Clang, VS Code, Ninja, ccache, Qt 6.11.2 `macos` |
| Linux | C++23 컴파일러, CMake/Ninja, SQLite, libsodium, cpp-httplib, nlohmann-json, 데스크톱용 Qt |
| 포털 | 지원되는 Node 22 버전 중 22.12 이상, npm |

이는 프로젝트의 기준이며 각각의 최신 출시 버전이라는 뜻은 아닙니다.
PostgreSQL 빌드에는 libpq도 필요합니다. `QT_ROOT`는 플랫폼 SDK를 가리킵니다.
개인 PC 설정인 `CMakeUserPresets.json`은 커밋하지 않습니다.

macOS가 Command Line Tools만 가리키면 설치된 전체 Xcode를 선택합니다.

```sh
sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
sudo xcodebuild -runFirstLaunch
xcodebuild -version
export QT_ROOT="$HOME/Qt/6.11.2/macos"
```

구현 저장소에서 다음을 실행합니다.

```sh
./scripts/init-dev-macos.sh
./scripts/verify-dev-macos.sh
cmake --preset user-macos-vscode-debug
cmake --build --preset user-macos-vscode-debug --parallel
ctest --preset user-macos-vscode-debug --output-on-failure
```

Windows에서는 `QT_ROOT`를 예를 들어 `C:\Qt\6.11.2\msvc2022_64`로 지정하고
새 터미널에서 `scripts\init-dev-windows.ps1`과 `scripts\verify-dev-windows.ps1`을
실행합니다. IncrediBuild 스크립트는 `-Configuration Debug -Desktop`을 지원합니다.
서로 다른 OS의 빌드 폴더를 공유하지 마십시오. Quick 3D/Shader Tools는 관련
그래픽 기능용이며 일반 관리 작업의 필수 조건은 아닙니다. 독립 웹 포털에는
WebEngine이 필요하지 않습니다.

## 단일 PC와 서버

```sh
clubplatform-desktop --database /path/club/data.sqlite \
  --extensions /path/club/extensions
```

새 데이터베이스는 최초 관리자 설정을 제공합니다. 12자 이상 비밀번호를 사용하고
로그인한 뒤 `Administration`에서 확장을 활성화합니다. 라이브러리는 미리 지정
폴더에 있어야 하며 활성화가 파일을 내려받는 것은 아닙니다.

서버는 로컬에서 초기화한 뒤 시작합니다.

```sh
clubplatform-server --sqlite /path/club/data.sqlite --init admin
clubplatform-server --sqlite /path/club/data.sqlite \
  --extensions /path/club/extensions \
  --portal-origin https://management.example
```

`--password-stdin`은 통제된 자동화용입니다. 비밀번호를 명령 인수, Git 또는
공개 로그에 넣지 마십시오. PostgreSQL은 `--postgres`와 보호된 설정의
`CLUBPLATFORM_POSTGRESQL`을 사용합니다. 저장소 제공자는 정확히 하나 선택합니다.

원격 데스크톱은 `--server https://management.example`로 연결합니다.
로컬 데이터베이스 경로는 서버의 오프라인 복제본이 아닙니다. 계정, 권한과 모듈은
서버에서 준비합니다. 원격 접속은 HTTPS 프록시를 이용하며 HTTP는 루프백용입니다.

## 포털 호스팅

```sh
cd apps/portal
npm ci
npm run build
```

`dist/`의 내용을 HTTPS 웹 루트에 복사합니다. 파일 제공에 Node 프로세스는
필요하지 않습니다. `/api/`를 `127.0.0.1:8080`으로 전달하고 업스트림 `Host`를
`127.0.0.1:8080`으로 설정하되 `Origin`과 `Authorization`은 보존합니다.
`--portal-origin`은 브라우저 출처와 정확히 같아야 하며 끝에 슬래시를 넣지
않습니다. 0.5.0의 포털 경로는 `/`이며 임의 하위 경로 배치는 완성된 설정 기능이 아닙니다.

개발용 Vite는 보통 `http://127.0.0.1:5173`을 사용하므로 해당 출처를 허용합니다.
`CLUB_API`로 개발 프록시 대상을 바꿀 수 있습니다. `npm run dev`는 운영 호스팅
명령이 아닙니다.

## 인수 확인

테스트 데이터로 로그인, 생성·저장·재조회, 조직, 회원 소속, 사진, 바이너리 파일
다운로드, 승급, CSV와 PDF를 확인합니다. 제한 계정의 무권한 쓰기는 거부되어야
합니다. 실제 백업을 새 데이터베이스에 복원하고 이전 세션이 무효인지 확인합니다.
모든 대상 OS에서 파일 대화상자와 PDF 뷰어를 점검하십시오. 빌드 성공만으로
기능 인수가 완료되지는 않습니다.

## HTTPS 리버스 프록시 예시

다음 Nginx 설정을 기존 TLS 가상 호스트에 추가합니다. 파일 루트를 수정하고 서버 환경에서 인증서와 HTTPS 수신 설정을 구성하십시오. 요청 크기는 최대 JSON 업로드를 허용하지만 디코딩된 파일 크기 제한은 애플리케이션이 계속 검사합니다. 서비스에는 정확히 같은 공개 Origin을 지정합니다.

```nginx
root /srv/club-platform/portal;
client_max_body_size 8m;

location / {
    try_files $uri $uri/ /index.html;
}

location /api/ {
    proxy_pass http://127.0.0.1:8080;
    proxy_set_header Host 127.0.0.1:8080;
    proxy_set_header Origin $http_origin;
    proxy_set_header Authorization $http_authorization;
}
```
