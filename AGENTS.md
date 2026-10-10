# AGENTS.md — 수능형 문제지(hwpx) 제작

이 프로젝트는 **대학수학능력시험 문제지와 같은 양식**의 문제지를 한글(hwpx)로 만든다.
두 에이전트가 Herdr 작업 공간에서 나란히 실행되며 역할을 나눈다. 이 문서를 읽는 에이전트는 자기 역할만 수행한다.

| 역할 | 담당 | 하는 일 | 쓰는 위치 |
|---|---|---|---|
| 출제·조판·검수 | **Claude Code** (왼쪽 탭) | 문항 출제와 정답 검증, hwpx 조판, 그림 사양서 작성·요청·검수, 최종 결과물 | `problems/`, `tools/`, `build/`, `output/`, `figures/FIGURE_SPEC.md` |
| 그림 | **Codex 앱** (오른쪽 탭) | 문제 그림(그래프·도형)을 **반드시 image gen(이미지 생성 도구)으로** 제작 | `figures/` (`fig_*.png`, `src/`, `DONE.txt`) |

## 폴더
```
problems/exam.py      문항 데이터 (META, COMMON, SUBJECTS, 쪽 배치)
problems/verify.py    정답 계산 검증 (sympy·전수 계산)
figures/              그림 사양서와 Codex가 만든 PNG
tools/build.py        hwpx 생성 → 한글 COM 수식 재계산 → hwpx/pdf 저장 → 위치 보정
tools/hwpx.py         HWPX XML 빌더       tools/hwp_com.ps1  한글 COM 처리
tools/render.py       PDF → 쪽 PNG        tools/contact.py   쪽 PNG 이어 붙이기
tools/gaps.py         양쪽 정렬로 벌어진 줄 찾기 (문항 넘침 검사는 build.py 가 자동으로 함)
tools/answers.py      정답표             tools/secmod/      한글 자동화 보안 모듈
output/               결과 (hwpx, pdf, 정답표.txt)
samples/<회차>/       끝난 회차 보관본 = 참고용 샘플 (problems, figures, output). 그림 요청 방식은 각 회차 FIGURE_SPEC.md·DONE.txt 참고
.claude/skills/suneung-exam-hwpx/   Claude용 절차·실측값·수식 문법·Codex 협업 문서
```
Python: `C:\Users\canine89\AppData\Local\Programs\Python\Python312-arm64\python.exe` (pymupdf, pillow, sympy 설치됨)

---

## Codex(그림 담당)

1. 요청이 오면 `figures/FIGURE_SPEC.md` 를 읽는다. 그림마다 파일 이름, 인쇄 폭(mm), 수치, 라벨이 적혀 있다.
2. **그림은 image gen(이미지 생성 도구)으로 만든다.** matplotlib 같은 코드 플로팅으로 대신하지 않는다. 수정 요청도 image gen 편집으로 처리한다. (사용자 지시)
3. 생성한 그림이 사양과 맞는지 직접 확인한다: 곡선 모양, 교점·극점 위치와 간격 비율, 음영 영역, 점 이름, 식 라벨.
4. 저장 규칙
   - `figures/<파일이름>.png`, **600 dpi, 흰 배경**(투명 금지), 여백 1 mm 안팎으로 잘라냄
   - 가로 픽셀 = 인쇄 폭(mm) ÷ 25.4 × 600
   - 프롬프트는 `figures/src/prompts.json`, 원본 이미지는 `figures/src/raw/` 에 보관
5. 수능 그림 스타일: 흑백 선화, 선 0.5~0.6 pt, 색칠은 연회색(#D9D9D9), 눈금·격자·제목·범례 없음, 축은 양의 방향 화살표만, 원점 `O`, 변수·식은 이탤릭, 점 이름(A, B, P…)은 정체.
6. 끝나면 `figures/DONE.txt` 에 그림별 실제 크기(mm)와 남은 오차를 적는다. 수정본은 같은 파일 이름으로 덮어쓰고 DONE.txt 에 한 줄 추가한다.
7. `problems/`, `tools/`, `output/`, `build/` 는 수정하지 않는다.

## Claude Code(출제·조판 담당)

`suneung-exam-hwpx` 스킬(`.claude/skills/suneung-exam-hwpx/SKILL.md`)의 절차를 따른다. 핵심:

1. `problems/exam.py` 에 문항을 쓰고, 모든 정답을 `problems/verify.py` 로 계산 검증한다.
2. 그림이 필요하면 `figures/FIGURE_SPEC.md` 를 쓰고 Herdr로 Codex에게 전달한다. 요청문에 **"image gen으로 만들 것"** 을 반드시 넣는다. 그림을 직접 그리지 않는다.
3. `python tools/build.py` → `tools/render.py`·`tools/contact.py` 로 쪽 이미지를 보며 검수 → Codex 그림도 사양과 대조해 틀리면 수정 요청.
4. `python tools/answers.py` 로 정답표를 만든다.

## 공통 규칙

- 결과물이 실제 평가원 문제지로 오인되지 않게 한다. 상단 문구에 "모의", 하단에 "학습용으로 제작된 모의 문제지" 문구를 쓰고, 평가원 저작권 문구는 쓰지 않는다.
- 사용자가 한글에서 `output/*.hwpx` 를 열어 두면 저장이 실패한다. 닫아 달라고 하거나 다른 이름으로 저장한다.
- 한글 자동화 권한 팝업이 뜨면 보안 모듈 등록을 확인한다: 레지스트리 `HKCU\SOFTWARE\HNC\HwpAutomation\Modules` 의 `FilePathCheckerModuleExample` = `tools\secmod\FilePathCheckerModuleExample.dll`.
