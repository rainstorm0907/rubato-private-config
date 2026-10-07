---
description: A Maplog map pin is a Place, not a per-date photo bundle. Screen collision must not recompute membership. Number badges are not the default pin language.
---

## Conclusion

- A single photo is evidence inside a memory, not a map pin and not a Journey node.
- The map pin is one Place: one representative photo at that place's coordinate. Same place first, same capture-local day second. Inside one place, morning and evening of the same capture-local day are one Visit. Woojin: “한 방문으로 보자”
- Screen collision, zoom, and which photo is on the front must not change Place or Visit identity, membership, or photo count. A cluster only tidies the screen.
- How "many photos" reads on the pin is the current pin contract in `/Users/wooojin/App/maplog/record/PRODUCT.md`. Do not put a `+n` badge back because an older contract required one.
- Saved Journey linking is outside 1.0. Do not use a Journey-node reading to merge different places into one map pin.

## Rationale

- Chose a stable identity over regrouping by what overlaps on screen. Recomputing membership on zoom changed counts like `+519 → +1229 → +781/+416 → +603 → +75/+24`. “우수수” only became “팟 팟 팟”. The thing to fix was identity, not a pixel threshold.
- Rejected: one map pin per date bundle, and `+n` as the count of photos left in that bundle. That was the 2026-09-01 reading of the quotes below. The user later set place first and day second, and rejected number badges as the default pin (“숫자도 깨알같이 쓴다고 나아지는것도 아니야”).
- Rejected as a map rule: “같은 날 강북과 강남을 모두 갔어도 하루 묶음 하나로”. That sentence was about linking a Journey, not about drawing one pin for two places. Two places on one day are two Visits. Gallery inside one place still splits photos by day.
- The fixed values, when a date bundle is still the unit being stored, are its id, its photo membership, and that day's path. A missing location stays in membership and drops out of the path only.

## Symptom

> “전체 사진 다 보여주지 말고, 날짜별로 묶어서 보여주기”

> “이것도 장면을 원하는게 아니라 날짜별로 묶은거를 잇고싶어. 예를 들어 서울 여행이면 : 첫날 강북 논 사진 묶음 > 다음 유저의 선택은 다음날 강남을 간 사진 묶음. 이렇게 이틀치의 이동 동선을 묶고 싶어할거야. 단 한개씩 사진을 연결하는게 아니라.”

> “이거 너가 완벽히 이해해야돼. 핵심 문장에 이어지는 감성이야 이거”

> “어 그게 맞아. 같은 날 강북과 강남을 모두 갔어도 하루 묶음 하나로 보는게 맞아. 그리고 '날짜 묶음의 ID와 그 안에 들어 있는 사진들' 이걸 고정하는게 맞아.”
