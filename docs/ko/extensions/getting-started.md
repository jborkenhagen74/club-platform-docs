# 네이티브 확장 개발

> 목표 버전 0.6.0의 준비 작업 G0입니다. HTTP API는 `/api/v1`이며 공통 `Client` 계약을 `LocalClient`와 `RestClient`가 구현합니다. 데이터베이스 스키마 8과 확장 ABI 2는 그대로입니다. 기존 `/api/...` 경로는 404를 반환합니다. 서버, 데스크톱, 포털 및 프록시를 함께 업데이트하십시오. 아래 기능 설명은 0.5.0 기준에서 작성되었으며 이 안내로 변경된 부분 외에는 계속 적용됩니다. ABI V3 및 일곱 UI 언어를 포함한 Core Foundation II는 아직 완료되지 않았습니다.


[시작 페이지](../README.md) · [화면 계약](ui.md) · [예제](../../../examples/extensions/hello-extension/README.md)

0.5.0 호스트는 **ABI 2**를 요구합니다. `sdk/extension_api.h`는 과거 ABI 1
초안이며 수명주기·메뉴·REST 콜백은 현재 호스트에서 사용할 수 없습니다.
새 모듈은 `sdk/extension_v2.h`를 사용합니다. C 경계로 STL과 모듈 간 메모리
해제를 피하지만 OS와 CPU 아키텍처는 일치해야 합니다.

모듈은 호스트 프로세스의 권한으로 실행되는 신뢰된 코드입니다. 샌드박스는
없습니다. 관리자가 폴더를 보호하고 배포할 라이브러리를 검토해야 하며,
일반 업로드 폴더에서 실행 모듈을 찾으면 안 됩니다. 시작 시 로드하며
실행 중 교체는 지원하지 않습니다.

## 진입점과 매니페스트

`clubplatform_extension_v2`를 내보내며 ABI 번호, UTF-8 매니페스트, 검증 함수를
가진 유효 수명이 유지되는 구조체를 반환합니다. 문자열은 모듈이 소유합니다.
검증 함수는 자료형 키와 JSON 문자열을 받고 성공 시 정확히 `1`을 반환합니다.
예외가 C 경계를 넘어가면 안 되며 데이터베이스 핸들은 제공하지 않습니다.

매니페스트는 `id`, `name`, `version`, `types`를 포함합니다. 버전은 세 숫자
구성요소이며 모듈 ID에는 점이 없습니다. 자료형 키는 `module.`로 시작합니다.
자료형에는 `key`, `label`, `fields`, 필드에는 `key`, `label`, `type` 및 선택적
`required:false`가 있습니다. 지원 형식은 `text`, `integer`, `decimal`, `boolean`,
`date`입니다. 키는 영문 소문자로 시작하고 소문자, 숫자, 밑줄, 네임스페이스의
점을 사용합니다. 중복과 다른 모듈의 네임스페이스는 거부합니다.

선택 필드도 빈 문자열로 보내는 등 선언한 모든 필드를 전송합니다. 알 수 없는
필드는 거부됩니다. 호스트는 모듈 검증 전에 자료형과 필수 값을 검사하며
현재 값당 512 UTF-8 바이트 제한을 적용합니다. 예제는 공개 헤더만으로
훈련 출석 레코드를 추가합니다.

```sh
cmake -S examples/extensions/hello-extension -B build/hello-extension -DCMAKE_BUILD_TYPE=Release
cmake --build build/hello-extension --config Release
```

결과 라이브러리를 전용 폴더에 복사합니다. Visual Studio의 `Release`/`Debug`
하위 폴더를 확인하십시오. `--extensions /absolute/path` 또는
`CLUBPLATFORM_EXTENSIONS`로 호스트에 전달합니다. 서버 모듈을 원격 데스크톱
PC에서 다시 로드하지 않습니다.

## 활성화와 데이터

로그인한 관리자가 `Erweiterungen aktivieren`을 선택하거나
`POST /api/v1/extensions/install`에 `{}`를 보냅니다. `schema.manage`가 필요하며
자료형 등록과 매니페스트 저장은 트랜잭션 및 감사 대상입니다.
`GET /api/v1/extensions`는 로드된 매니페스트와 `installed`를 표시합니다.
동일 매니페스트의 재설치는 허용됩니다.

현재 네이티브 레코드는 사람에게 속합니다. 예제 경로는
`/api/v1/management/ext:attendance.session`입니다. 관리 값에는 `person_id`도
포함하며 호스트가 업무 검증 함수 호출 전에 이를 분리합니다.
`records.read/write` 외에 `attendance.read/write`를 역할에 부여합니다.
화면이 보인다고 서버 권한 검사를 대신하지 않습니다.

이미 설치된 것과 다른 매니페스트는 로드 시 거부합니다. 버전만 올려도 데이터가
마이그레이션되지는 않습니다. 명시적 마이그레이션과 검증된 백업이 필요합니다.
임의 REST 경로, 백그라운드 작업, 동봉 QML/JavaScript 실행과 핫 리로드는
ABI 2 범위 밖입니다.
