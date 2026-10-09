# kmath-test-maker

대학수학능력시험(수능) 문제지와 같은 양식의 문제지를 한글 **hwpx**로 만드는 작업 환경입니다.
Claude Code(출제·조판·검수)와 Codex 앱(그림, image gen)이 Herdr 작업 공간에서 나란히 일합니다.

- `AGENTS.md` — 두 에이전트의 역할 분담과 공통 규칙 (Claude, Codex 모두 읽음)
- `.claude/skills/suneung-exam-hwpx/` — Claude Code 스킬: 출제 → 정답 검증 → Codex 그림 요청·검수 → 조판 → 검수 절차,
  원본 수능지 실측값, 한글 수식 문법, 예시 문제지(46문항)
- `tools/` — 조판기
  - `build.py` 문항 데이터(`problems/exam.py`) → hwpx → 한글 COM 수식 재계산 → hwpx/pdf, 쪽 격자 배치와 문항 넘침 자동 검사
  - `hwpx.py` HWPX XML 빌더, `hwp_com.ps1` 한글 COM 처리
  - `render.py`·`contact.py` 쪽 이미지 검토, `gaps.py` 양쪽 정렬로 벌어진 줄 찾기, `answers.py` 정답표

## 필요 환경
- Windows + 한컴오피스 한글(2024에서 확인) — 신명·한양 HFT 글꼴과 HYhwpEQ 수식 글꼴이 함께 설치됨
- Python 3.12 (`pip install pymupdf pillow sympy`)
- [Herdr](https://herdr.dev) 작업 공간: 왼쪽 탭 Claude Code, 오른쪽 탭 Codex 앱
- **한글 자동화 보안 모듈** (저장소에는 포함하지 않음): 한컴 개발자 자료
  [hancom-io/devcenter-archive](https://github.com/hancom-io/devcenter-archive) 의 `hwp-automation/보안모듈(Automation).zip` 에서
  `FilePathCheckerModuleExample.dll` 을 `tools/secmod/` 에 두고 레지스트리에 등록
  (`HKCU\SOFTWARE\HNC\HwpAutomation\Modules` → 값 이름 `FilePathCheckerModuleExample`, 데이터 = DLL 전체 경로).
  등록하지 않으면 빌드할 때마다 한글 권한 확인 창이 뜹니다.

## 사용
Claude Code에서 "수능 수학 모의고사 만들어줘"처럼 요청하면 스킬이 적용됩니다.
직접 돌릴 때: `problems/exam.py` 작성(형식은 스킬의 `templates/exam_example.py`) → `python tools/build.py` → `output/`.

결과물은 학습용 모의 문제지로, 평가원 문제지로 오인되지 않도록 "모의" 문구와 학습용 안내 문구를 넣습니다.
