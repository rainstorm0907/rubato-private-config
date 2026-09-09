---
description: 우진 맥에서 Moonlight가 1초마다 끊긴 원인과 검증된 AWDL/LLW 임시 해결법.
---
## 2026-08-29 Moonlight 1초 주기 끊김

**상태: 사용자 체감·계측 검증됨.**

우진의 macOS 26.5.2 맥에서 Moonlight가 약 1초마다 툭 끊겼다. 유튜브 등 버퍼형 서비스는 정상이었다. Windows Sunshine 호스트 처리와 맥 디코딩·렌더링은 각각 약 2~4ms로 정상이었다.

### 원인 판정

Apple peer-to-peer 무선 경로가 일반 Wi-Fi와 물리 무선칩을 공유하며 만든 주기적 채널 점유가 원인이었다. 처음에는 `awdl0`와 `llw0`를 함께 내렸다. 이후 macOS가 `awdl0`를 자동으로 다시 올렸지만 `llw0`는 내려간 채였고, 지연과 끊김이 계속 사라져 있었다. 따라서 해결을 유지한 핵심 상태는 `llw0` 비활성화이며 `awdl0 down`은 필수가 아니다. 다만 `llw0`를 다시 올려 재발시키는 역방향 시험은 하지 않았으므로 LLW 단독 원인보다는 LLW가 관여한 Apple P2P 무선 경로로 표현한다.

끄기 직전 커널 로그는 AWDL이 3.062초 중 1,040ms(약 34%) 활성 상태였다고 기록했다. 같은 시각 `sharingd`가 `awdl0` 역할을 조회했고 AirPlay sink capability, `rapportd`, Sidecar·Continuity Camera 관련 상주 서비스도 확인됐다. 이는 macOS가 AirDrop·Handoff·AirPlay·Continuity를 위해 인터페이스를 자동으로 활성화한다는 근거다. 다만 오늘 어떤 서비스가 최초로 문제 상태를 촉발했는지는 특정하지 못했다.

- 조치 전 맥→공유기: 중앙 약 4ms, p95 72~92ms, 최대 96~177ms, 300회 중 50ms 초과 27~53회
- 맥 자체 핑: 최대 0.7ms 미만
- 2.4GHz와 5GHz 모두 재현
- Moonlight 비트레이트·FPS 감소로 평균 프레임 드롭은 줄어도 1초 주기 끊김은 유지
- `awdl0`/`llw0` 비활성화 직후 맥→공유기 300회: 중앙 2.936ms, p95 3.474ms, 최대 6.012ms, 50ms 초과 0회
- `awdl0` 자동 재활성·`llw0` 비활성 상태 재측정: 중앙 2.961ms, p95 4.456ms, 최대 6.872ms, 50ms 초과 0회
- 우진 확인: "헐 미친 고쳐졌어. 이게 뭔데?????????"

### 검증된 임시 해결법

```bash
sudo ifconfig awdl0 down
sudo ifconfig llw0 down
```

일반 Wi-Fi와 인터넷은 유지되지만 AirDrop, Handoff, Sidecar, Universal Control 등 Continuity 기능이 중단될 수 있다. 재부팅, 잠자기/깨우기, Wi-Fi 토글 또는 Continuity 요청 뒤 macOS가 인터페이스를 다시 올릴 수 있다. 그때 같은 명령을 다시 실행한다.

원복:

```bash
sudo ifconfig awdl0 up
sudo ifconfig llw0 up
```

참고: https://gyorgy.sh/blog/macos-awdl-network-jitter
