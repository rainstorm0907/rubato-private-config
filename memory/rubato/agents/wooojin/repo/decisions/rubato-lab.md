---
description: The confirmed roles and boundary of the public Rubato repository and the private Rubato Lab research repository.
---
## 2026-08-30 — repository role split

- Status: user confirmed.
- Context: Setting up a repository to separate Rubato's public product code from internal research and documents.
- Woojin, original wording: “여기는 rubato-lab/rubato/ 이 구조로 가고”
- Woojin, original wording: “루바토는 공개용 레포, 루바토 랩은 그거 문서정리나 이런것들 적어두는 연구실.”
- Decision:
  - The public Rubato repository is the source of truth for product code and public documents.
  - The private `rubato-lab/rubato` repository is the lab that supports Rubato, and handles internal documents, experiments, and knowledge structure.
  - Memory structure is Lab's first candidate, but the final directory and PR order are confirmed after a separate design.
