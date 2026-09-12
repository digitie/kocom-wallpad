[![HACS Custom](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://my.home-assistant.io/redirect/hacs_repository/?owner=digitie&repository=kocom-wallpad&category=Integration)

# Kocom Wallpad for Home Assistant

코콤 월패드를 Home Assistant에 연결하는 커스텀 통합구성요소입니다. 월패드에서 수신한 상태 패킷으로 기기를 찾아 `light`, `switch`, `climate`, `fan`, `sensor`, `binary_sensor` 엔티티로 제공합니다.

이 저장소는 [lunDreame/kocom-wallpad](https://github.com/lunDreame/kocom-wallpad)를 기반으로 한 포크입니다. 원본 프로젝트의 기기 통신·엔티티 구현을 바탕으로 AI 도구를 활용해 코드 분석, 오류 수정, 유지보수와 문서화를 개선합니다. AI가 제안한 변경도 저장소 검증과 실제 월패드 동작 확인이 필요합니다.

## 지원 기능

| 월패드 기능 | Home Assistant 엔티티 | 현재 구현 |
|---|---|---|
| 조명 | `light` | 켜기/끄기. 밝기 조절은 지원하지 않습니다. |
| 일괄 소등 | `light` | 전체 조명 끄기 명령과 상태 표시 |
| 콘센트 | `switch` | 켜기/끄기 |
| 난방 | `climate` | 난방/꺼짐, 목표·현재 온도, 외출 프리셋 |
| 에어컨 | `climate` | 냉방·송풍·제습·자동·꺼짐, 목표·현재 온도, 팬 모드 |
| 환기 | `fan` | 켜기/끄기, 3단 속도, 월패드가 보고하는 프리셋 |
| 실내 공기질 | `sensor` | PM10, PM2.5, CO₂, VOC, 온도, 습도 |
| 환기 상태 | `sensor`, `binary_sensor` | CO₂와 오류 상태 |
| 보일러 상태 | `sensor`, `binary_sensor` | 난방수·온수 온도와 오류 상태 |
| 가스밸브 | `switch` | 상태 표시와 명령 엔티티. 아래 제한사항을 확인하세요. |
| 현관 움직임 감지 | `binary_sensor` | 움직임 감지 상태 |
| 엘리베이터 | `switch`, `sensor` | 호출 요청, 방향 및 층수 상태. 층수는 월패드가 층 정보를 보낼 때 제공됩니다. |

기기별 지원 여부와 보고되는 센서는 월패드 모델, 세대 설정, EW11 연결 방식에 따라 달라질 수 있습니다. 인터폰 음성·영상 제어는 지원하지 않습니다. 조명의 디밍/밝기 조절도 현재 구현되어 있지 않습니다.

### 알려진 제한사항

- 조명과 콘센트는 통합이 켜짐 상태 패킷을 받아야 새 엔티티로 등록될 수 있습니다. 기기가 보이지 않으면 월패드에서 한 번 켠 뒤 상태 패킷을 기다려 보세요. 엔티티가 생성된 다음에는 끌 수 있습니다.
- 가스밸브의 현재 명령 생성 코드는 Home Assistant의 켜기와 끄기 요청에 같은 프로토콜 명령을 보냅니다. 잠금/해제가 모델별로 올바르게 동작한다고 가정하지 마세요.
- 엘리베이터 엔티티의 현재 명령 생성 코드는 켜기와 끄기 요청에 같은 호출 프레임을 보냅니다. 끄기 동작을 호출 취소로 사용하지 마세요.
- 상태는 월패드에서 오는 패킷으로 갱신됩니다. 모델별 프로토콜 차이와 실제 하드웨어에서 확인되지 않은 동작은 보장하지 않습니다.

## 준비물과 연결 방식

- Home Assistant에서 연결할 수 있는 코콤 월패드 통신 경로가 필요합니다. 기존 설치에서 많이 사용하는 연결 방식은 RS-485와 EW11 시리얼-Wi-Fi/Ethernet 변환기입니다.
- EW11을 TCP로 연결하려면 Home Assistant에서 접근 가능한 호스트 주소와 EW11 포트를 준비하세요. 포트 기본값은 `8899`입니다.
- Home Assistant 호스트에 접근 가능한 시리얼 장치를 직접 연결할 수도 있습니다. 호스트 입력란에 `/dev/ttyUSB0` 또는 `/dev/serial/by-id/...`처럼 `/`로 시작하는 장치 경로를 입력하면 시리얼로 열고 포트 입력값은 무시합니다. 시리얼 통신 속도는 현재 코드에서 9600 baud입니다.
- 시리얼 장치를 사용하는 경우 Home Assistant 실행 환경에서 해당 장치 파일에 접근할 수 있어야 합니다.

## 설치

### HACS

1. HACS에서 **Custom repositories**를 열고 `https://github.com/digitie/kocom-wallpad`를 카테고리 **Integration**으로 추가합니다.
2. **Kocom Wallpad (Digitie)**를 설치한 뒤 Home Assistant를 재시작합니다.
3. **설정 → 기기 및 서비스 → 통합구성요소 추가**에서 **코콤 월패드 (Digitie)**를 검색해 추가합니다.

이 포크는 원본과 같은 Home Assistant 통합 도메인(`kocom_wallpad`)과 설치 경로를 유지합니다. 따라서 원본과 이 포크를 동시에 설치하거나 HACS에서 두 저장소를 함께 관리할 수 없습니다. 기존 원본을 사용 중이면 HACS에서 원본 저장소를 제거한 뒤 이 저장소를 설치하고 Home Assistant를 재시작하세요. Home Assistant의 기존 통합 항목은 삭제하지 마세요. 도메인을 유지해 기존 설정 항목과 엔티티 식별자의 호환성을 보존합니다.

### 연결 설정

통합 설정 화면에서 다음 값을 입력합니다.

| 입력값 | 설명 |
|---|---|
| 호스트 | EW11의 IP 주소 또는 시리얼 장치 경로 |
| 포트 | TCP 연결 포트. 기본값은 `8899`이며, 시리얼 장치 경로를 입력한 경우 무시됩니다. |

설정 단계에서 연결을 확인합니다. 첫 연결에 실패하면 Home Assistant가 설정을 다시 시도할 수 있습니다. 연결을 사용 중에 잃으면 통합이 재연결을 시도합니다. `manifest.json`은 `pyserial-asyncio`를 의존성으로 선언하며 Home Assistant가 통합을 설치할 때 함께 설치합니다. 저장소의 HACS 메타데이터에는 Home Assistant `2025.2.2`가 최소 버전으로 지정되어 있습니다.

## 문제 해결

### 기기가 나타나지 않는 경우

1. 호스트 주소와 포트가 맞는지, Home Assistant에서 해당 주소로 연결할 수 있는지 확인합니다.
2. EW11 또는 시리얼 장치가 월패드의 올바른 통신선에 연결되어 있는지 확인합니다.
3. 조명과 콘센트는 한 번 켜서 상태 패킷이 오도록 한 다음 엔티티가 생성되는지 확인합니다.
4. 엘리베이터 층수 센서는 월패드가 층 정보를 보낸 뒤 나타날 수 있습니다.

### 디버그 로그

문제를 확인할 때 `configuration.yaml`에 아래 설정을 추가하고 Home Assistant를 재시작하세요. 확인이 끝나면 디버그 로깅을 끄세요.

```yaml
logger:
  default: info
  logs:
    custom_components.kocom_wallpad: debug
```

디버그 로그에는 호스트 주소와 원시 통신 패킷이 포함될 수 있습니다. 이슈에 로그를 첨부하기 전에 IP 주소, 시리얼 장치 경로 등 개인 환경을 드러내는 정보를 가리세요.

## 구조와 동작

1. `config_flow.py`가 호스트와 포트 입력을 받고 연결 가능 여부를 확인합니다.
2. `transport.py`가 TCP 또는 시리얼 스트림을 비동기로 열고 연결 복구를 담당합니다.
3. `gateway.py`가 수신·송신 작업, 명령 대기열, 상태 확인과 Home Assistant 엔티티 등록을 관리합니다.
4. `controller.py`가 Kocom 패킷을 분리·검증하고 기기 상태를 해석하거나 제어 프레임을 생성합니다.
5. `models.py`의 기기 상태가 각 플랫폼 파일을 통해 Home Assistant 엔티티로 노출됩니다. 상태 변경은 월패드에서 수신한 패킷으로 전달됩니다.

주요 파일은 다음과 같습니다.

| 경로 | 역할 |
|---|---|
| `custom_components/kocom_wallpad/manifest.json` | 통합 메타데이터와 의존성 |
| `custom_components/kocom_wallpad/config_flow.py` | UI 설정 및 연결 확인 |
| `custom_components/kocom_wallpad/transport.py` | TCP·시리얼 비동기 통신 |
| `custom_components/kocom_wallpad/gateway.py` | 수신·송신 루프, 명령 대기열, 기기 등록 |
| `custom_components/kocom_wallpad/controller.py` | 패킷 파싱 및 제어 프레임 생성 |
| `custom_components/kocom_wallpad/models.py` | 기기·상태 모델과 프로토콜 매핑 |
| `custom_components/kocom_wallpad/{light,switch,climate,fan,sensor,binary_sensor}.py` | Home Assistant 플랫폼 엔티티 |
| `custom_components/kocom_wallpad/translations/` | 한국어·영어 설정 및 엔티티 이름 |
| `.github/workflows/` | hassfest 및 HACS 검증 |

## 개발 및 검증

로컬에서 파이썬 문법을 확인할 수 있습니다.

```sh
python -m compileall -q custom_components/kocom_wallpad
```

GitHub Actions는 `hassfest`와 HACS 검증을 수행합니다. 현재 저장소에는 별도의 단위 테스트나 하드웨어 통합 테스트가 없습니다. 월패드 제어 동작을 바꾼 경우에는 지원 모델에서 실제 통신과 상태 반영을 확인해야 합니다.

## 기여 및 이슈 제보

버그 제보와 개선 제안은 [이 저장소의 Issues](https://github.com/digitie/kocom-wallpad/issues) 또는 [Pull requests](https://github.com/digitie/kocom-wallpad/pulls)에 남겨 주세요. 재현을 돕기 위해 Home Assistant 버전, 월패드/통신 어댑터 구성, 기대 동작과 실제 동작, 민감한 값을 가린 관련 로그를 함께 적어 주세요.

## 원본 프로젝트와 권리 표기

이 프로젝트는 [lunDreame/kocom-wallpad](https://github.com/lunDreame/kocom-wallpad)에서 시작한 포크입니다. 기존 코드와 원작자 표기를 존중하며, 이 저장소에는 별도의 `LICENSE` 파일이 포함되어 있지 않습니다. 원본 프로젝트 및 관련 저작권 표기를 확인해 주세요.
