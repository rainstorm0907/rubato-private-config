---
description: The cause of Moonlight cutting out every 1 second on Woojin's Mac, and the verified temporary AWDL/LLW fix.
---
## 2026-08-29 Moonlight cutting out on a 1-second cycle

**Status: verified by what the user felt and by measurement.**

On Woojin's macOS 26.5.2 Mac, Moonlight cut out about every 1 second. Buffered services such as YouTube were normal. Windows Sunshine host processing, and Mac decoding and rendering, were each about 2~4ms, which was normal.

### Cause verdict

The cause was periodic channel occupancy that Apple's peer-to-peer wireless path created by sharing the physical wireless chip with ordinary Wi-Fi. At first `awdl0` and `llw0` were brought down together. After that macOS automatically brought `awdl0` back up, but `llw0` stayed down, and the latency and the drops had stayed gone. So the core state that kept the fix is `llw0` disabled, and `awdl0 down` is not required. The reverse test of bringing `llw0` back up to make it recur was not done, so it is described as an Apple P2P wireless path that LLW was involved in, rather than as LLW being the sole cause.

The kernel log just before turning it off recorded that AWDL was active for 1,040ms of 3.062 seconds (about 34%). At the same time `sharingd` queried the `awdl0` role, and resident services related to AirPlay sink capability, `rapportd`, and Sidecar·Continuity Camera were also confirmed. This is the ground for macOS automatically activating the interface for AirDrop·Handoff·AirPlay·Continuity. Which service first triggered the problem state today was not identified.

- Before the measure, Mac→router: median about 4ms, p95 72~92ms, max 96~177ms, 27~53 of 300 over 50ms
- Ping on the Mac itself: max under 0.7ms
- Reproduced on both 2.4GHz and 5GHz
- Lowering the Moonlight bitrate and FPS reduced the average frame drop, but the 1-second-cycle drop remained
- Mac→router, 300 times, right after disabling `awdl0`/`llw0`: median 2.936ms, p95 3.474ms, max 6.012ms, 0 over 50ms
- Remeasured with `awdl0` auto-reactivated and `llw0` inactive: median 2.961ms, p95 4.456ms, max 6.872ms, 0 over 50ms
- Woojin confirmed: "헐 미친 고쳐졌어. 이게 뭔데?????????"

### Verified temporary fix

```bash
sudo ifconfig awdl0 down
sudo ifconfig llw0 down
```

Ordinary Wi-Fi and the internet stay up, but Continuity features such as AirDrop, Handoff, Sidecar, and Universal Control can stop. After a reboot, sleep/wake, a Wi-Fi toggle, or a Continuity request, macOS can bring the interface back up. Run the same commands again then.

Restore:

```bash
sudo ifconfig awdl0 up
sudo ifconfig llw0 up
```

Reference: https://gyorgy.sh/blog/macos-awdl-network-jitter
