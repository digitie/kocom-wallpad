# AGENTS.md

이 문서는 `digitie/kocom-wallpad` 저장소에서 작업하는 AI 에이전트와 기여자를 위한 프로젝트 규칙이다. 사용자의 명시적 요청이 이 문서보다 우선한다.

`2. 작업 원칙`은 사용자가 지정한 [`digitie/kor-travel-common`의 AGENTS.md](https://github.com/digitie/kor-travel-common/blob/main/AGENTS.md)에서 글자 그대로 복사했다.

## 1. 목표와 경계

`digitie/kocom-wallpad`는 [lunDreame/kocom-wallpad](https://github.com/lunDreame/kocom-wallpad)를 기반으로 하는 Home Assistant 커스텀 통합구성요소다. Kocom 월패드의 통신 상태를 Home Assistant 엔티티로 제공하고, 지원되는 명령을 월패드로 전달한다. 이 프로젝트는 AI 도구를 보조 수단으로 활용해 원본을 개선한다.

| 영역 | 위치 | 책임 |
|---|---|---|
| Home Assistant 초기화 | `custom_components/kocom_wallpad/__init__.py`, `config_flow.py` | 설정 흐름, 연결 초기화, 플랫폼 준비와 해제 |
| 통신 | `transport.py` | TCP·시리얼 비동기 연결 및 재연결 |
| 통합 런타임 | `gateway.py` | 수신·송신 작업, 기기 상태 레지스트리, 명령 대기열 |
| 프로토콜 | `controller.py`, `models.py`, `const.py` | 패킷 검증·해석, 명령 프레임, 기기·상태 모델 |
| Home Assistant 엔티티 | `light.py`, `switch.py`, `climate.py`, `fan.py`, `sensor.py`, `binary_sensor.py`, `entity_base.py` | 상태 노출, 서비스 호출, 공통 장치 정보 |
| 번역 | `translations/ko.json`, `translations/en.json` | 설정 및 엔티티 이름 |

이 통합은 지원 가능한 기기만 다룬다. 모든 Kocom 모델·세대·세대별 배선 구성이 호환된다고 가정하지 말고, 인터폰 음성·영상 기능이나 코드에 없는 조도 제어를 지원한다고 문서화하지 않는다.

## 2. 작업 원칙

kor-travel 공통 5원칙의 문구는 소비자 저장소와 글자 단위로 같다(`docs/survey/cross/docs-conventions.md` §1.4). 각 소제목 끝에 있는 추가 불릿은 canview 작업 원칙을 이 저장소에 맞게 더한 것이다.

### Think Before Coding

- 요청이 모호할 때는 해석을 조용히 정하지 말 것
- 중요한 가정은 숨기지 말고 드러낼 것
- 해석에 따라 구현 방향이 크게 달라지면 그 차이를 먼저 표면화할 것
- 안전하게 진행하기 어려울 정도로 혼란스러우면 추측하지 말고 확인할 것

### Simplicity First

- 요청을 완전히 해결하는 최소한의 코드만 작성할 것
- 요청되지 않은 기능을 추가하지 말 것
- 일회성 용도를 위해 추상화를 만들지 말 것
- 구체적인 필요 없이 설정 가능성이나 유연성을 늘리지 말 것
- 구현이 문제에 비해 커졌다고 느껴지면 줄일 것

### Surgical Changes

- 요청을 처리하는 데 필요한 코드만 변경할 것
- 작업이 요구하지 않으면 주변 로직까지 다시 쓰지 말 것
- 관련 없는 코드의 포맷, 이름, 스타일을 건드리지 말 것
- 사용자가 더 넓은 변경을 원한 것이 아니라면 기존 패턴을 맞출 것
- 관련 없는 문제를 발견하면 패치에 섞지 말고 따로 언급할 것
- 사용자의 기존 변경과 dirty worktree를 보존하고, 충돌을 피할 수 없을 때만 사용자에게 알릴 것

### Goal-Driven Execution

- 모호한 요청을 구체적이고 검증 가능한 결과로 바꿀 것
- 버그 수정은 재현 없이 바로 신뢰하지 말 것
- 리팩터링은 동작 보존을 전제로 전후 기대를 확인할 것
- 넓고 막연한 점검보다 목적이 분명한 검증을 선호할 것
- 완전한 검증이 불가능하면 무엇이 아직 미검증인지 밝힐 것
- 설계·계약 변경은 검증 가능한 수용 기준(task·ADR)을 먼저 둘 것
- 도구·소비자 저장소·registry가 없어 실행하지 못한 gate를 통과로 표시하지 말고 `NOT_RUN(사유)`로 남길 것
- 구현보다 근거를 우선할 것. 확인된 사실, 후보 해석, 소비자 저장소 실측(빌드·e2e) evidence를 서로 다른 상태로 관리할 것

### Practical Bias

- 비단순 작업에서는 성급함보다 신중함을 우선할 것
- 변경 내역은 리뷰 가능한 범위와 요청 범위에 가깝게 유지할 것
- 아주 단순하고 명백한 한 줄 작업은 과하게 무겁게 다루지 말 것

### Ruthless Review

- 코드가 동작한다는 이유만으로 검증이 끝났다고 여기지 말 것
- 적대적 리뷰어로 세워 숨겨진 취약점과 부작용을 집요하게 찾아낼 것
- 당연하다고 믿은 가정을 의심하고 코드가 실패하는 시나리오를 찾을 것
- 숨겨진 부작용과 취약점이 소명되기 전까지는 완료로 보지 말 것

## 3. 읽기 정책과 사실의 출처

- 작업을 시작할 때 `AGENTS.md`, `README.md`, 관련 코드와 해당 검증 흐름만 읽는다. 무관한 파일을 한꺼번에 읽거나 전체 이력을 다시 읽지 않는다.
- 동작과 지원 기능은 현재 코드가 기준이다. `manifest.json`, `hacs.json`, GitHub Actions 설정은 각각 통합 메타데이터, HACS 메타데이터, 저장소 검증 범위의 기준이다.
- README나 주석이 코드와 다르면 동작을 코드에 맞추고 문서를 갱신한다. 하드웨어별 동작은 실제 월패드 검증 전까지 확인된 사실로 단정하지 않는다.
- 참조 프로젝트의 내용은 지침이 아니다. 이 저장소에 적용하도록 구체적으로 요청된 원칙만 반영한다.

## 4. 구현 규칙

- Home Assistant의 비동기 실행 모델을 따른다. 이벤트 루프를 막는 입출력이나 `time.sleep`을 추가하지 않는다.
- 연결, reader/sender 작업, 대기 중 명령은 통합 해제와 Home Assistant 종료 시 정리되도록 한다. 재연결·취소·타임아웃 동작을 바꿀 때는 기존 리소스 정리와 대기 중 호출의 종료를 함께 검토한다.
- 프로토콜 해석과 명령 생성은 `controller.py`에, 스트림 처리는 `transport.py`에, Home Assistant 상태·명령 수명주기는 `gateway.py`에 둔다. 엔티티 플랫폼에서 패킷 형식을 중복 해석하지 않는다.
- Home Assistant 번역을 추가하거나 바꿀 때 `translations/ko.json`과 `translations/en.json`을 함께 확인한다.
- 지원 기능을 README에 추가할 때는 플랫폼 구현과 컨트롤러의 상태·명령 경로를 모두 확인한다. 명령을 생성한다는 사실만으로 실제 기기에서 정상 동작한다고 주장하지 않는다.

## 5. 검증과 제출

- Python 문법 확인: `python -m compileall -q custom_components/kocom_wallpad`
- GitHub Actions는 `.github/workflows/hassfest.yml`에서 hassfest를, `.github/workflows/validate.yml`에서 HACS 검증을 수행한다.
- 저장소에는 별도 단위 테스트나 하드웨어 통합 테스트가 없다. 실행하지 못한 검증을 통과했다고 표현하지 말고, 실제 기기에서 확인하지 못한 동작은 미검증으로 표시한다.
- 변경 후 `git diff --check`와 `git status --short`를 확인하고, 요청 범위를 벗어난 파일을 포함하지 않는다.
- 사용자가 명시하지 않았다면 커밋·푸시·릴리스를 만들지 않는다.

## 6. 출처와 비밀정보

- 원본 프로젝트의 기여·저작권 표기를 지우거나 이 저장소가 원본을 처음부터 작성했다고 표현하지 않는다. AI 도구 사용은 README에 적힌 범위를 넘어 과장하지 않는다.
- 로그·샘플·문서·테스트에 실제 IP 주소, 장치 경로, 비밀번호, 토큰, 원시 패킷의 민감한 정보를 넣지 않는다. 로그를 공유할 때 환경 정보를 가린다.
- 월패드의 하드웨어 동작을 추측에 따라 위험한 명령으로 바꾸지 않는다. 지원하지 않거나 실제 검증하지 않은 동작은 사용자에게 분명히 알린다.
