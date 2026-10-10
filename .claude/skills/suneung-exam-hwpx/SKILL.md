---
name: suneung-exam-hwpx
description: 대학수학능력시험(수능) 문제지와 같은 양식의 문제지를 한글 hwpx로 만드는 절차. 문항 출제·정답 검증, 수능 조판(2단, 머리말, 5지선다형/단답형, 확인 사항 상자), 그림은 오른쪽 탭 Codex 앱에 image gen으로 맡기고 검수까지. "수능 문제지 만들어줘", "모의고사 hwpx", "수능형 문제지", 새 회차/새 과목 문제지 요청 시 사용.
---

# 수능형 문제지(hwpx) 만들기

역할 분담과 공통 규칙은 프로젝트 루트 `AGENTS.md` 에 있다. 이 스킬은 Claude(출제·조판) 쪽 절차다.
**그림은 항상 오른쪽 탭 Codex 앱이 image gen으로 만든다. Claude는 그림을 직접 그리지 않는다.**

참고 문서 (필요할 때 읽기)
- `reference/layout-spec.md` — 원본 수능지 실측값(쪽 배치, 치수, 글꼴, 배점)
- `reference/hwp-equation.md` — 한글 수식 스크립트 문법과 수능식 표기 습관
- `reference/codex-figures.md` — Herdr로 Codex에 그림 맡기기, 사양서 쓰는 법, 검수 기준
- `templates/exam_example.py`, `verify_example.py`, `FIGURE_SPEC_example.md` — 완성된 2027 모의 수학 영역(46문항)
- 프로젝트 루트 `samples/2027-모의1~3/` — 실제로 만든 회차들의 문항·그림·결과 hwpx/pdf (참고용 샘플)

Python: `C:\Users\canine89\AppData\Local\Programs\Python\Python312-arm64\python.exe` (아래 `PY`)

## 0. 준비 확인
- 한글(한컴오피스) 설치, COM 등록(`HWPFrame.HwpObject`), 보안 모듈 레지스트리 등록 — AGENTS.md 공통 규칙 참고.
- Herdr 안에서 실행 중인지(`HERDR_ENV=1`)와 Codex 탭이 있는지 `herdr agent list` 로 확인. 없으면 사용자에게 오른쪽 탭에 Codex를 열어 달라고 한다.
- 새 문제지를 만들기 전에 이전 회차를 `samples/<회차>/` 로 옮긴다: `problems/`, `figures/`(src/raw 포함해도 됨 — 저장소에서는 자동 제외), `output/` 의 그 회차 결과(hwpx·pdf·정답표).
  `samples/README.md` 의 회차 표에 한 줄 추가. 그 뒤 작업 폴더의 `figures/fig_*.png`, `DONE.txt`, `src/` 를 비우고 시작.
- **참고 자료로 `samples/` 를 먼저 본다**: 이전 회차의 `exam.py`(문항 형식·난이도·배치), `FIGURE_SPEC.md`(그림 요청 방식), `DONE.txt`(Codex 검수 기록).
  같은 문항을 되풀이하지 않도록 이전 회차와 소재·수치를 겹치지 않게 출제한다.

## 1. 출제 — `problems/exam.py`
- 형식은 파일 상단 docstring과 `templates/exam_example.py` 그대로. 블록: `t` 문장, `eq` 가운데 수식, `box` (가)(나) 조건, `fig` 그림, `ch` 보기, `side` 본문+표준정규분포표.
  - `ch` 의 세 번째 값은 줄 수: 1(한 줄 다섯 개), 2(3+2), 3(2+2+1, 아주 긴 보기). 생략하면 길이로 1/2 자동. 긴 보기가 줄을 넘기면 3으로.
- `META`: `year_title`(반드시 "모의" 포함), `period`, `type`, `copyright`(학습용 모의 문구), `out_name`.
- 수학 영역 기본 구성: 공통 22문항(1–15 5지선다, 16–22 단답) + 선택 3과목 각 8문항(23–28 5지선다, 29–30 단답). 배점·쪽 배치는 `layout-spec.md`.
- **쪽 배치는 격자로 먼저 정한다** (`COMMON_LAYOUT`, `ELECTIVE_LAYOUT`): 쪽마다 `(왼쪽 단, 오른쪽 단)`, 한 단에 문항 1개(세로 1칸) 또는 2개(위·아래 2칸).
  즉 쪽 하나가 2×2(네 문항), 1×2(두 문항), 2+1 등. 'MC'/'SA' 표시는 다음 문항 칸 맨 위에 붙는다.
  - 각 문항은 쪽 위치에 고정된 테두리 없는 칸(영역)에 들어가므로 앞 문항 길이가 뒤 문항 위치에 영향을 주지 않는다.
  - 2칸 단의 나눔 위치: `SECOND_TARGET`(두 번째 문항 번호의 y, 원본 실측) 있으면 그 값, 없으면 단 가운데.
  - 짧은 문항(2·3점)은 2칸, 그림·조건 상자가 있는 긴 문항(4점)은 1칸에 배치하는 것이 원칙(원본 수능과 같음).
  - 다른 과목/분량이면 이 배치와 `SUBJECTS`, `SECOND_TARGET` 을 바꾼다.
- 출제 기준: 교육과정 범위, 수능 문체("~의 값은?", "~의 값을 구하시오.", "(단, ~)"), 단답 정답은 0~999 자연수.
- 5지선다 보기는 오름차순, 정답 번호가 ①~⑤에 고르게(공통 15문항이면 각 3개).
- 수식 문법은 `hwp-equation.md`. 숫자 하나도 `$...$` 수식으로, 여러 조건은 수식을 나눠 쓴다.

## 2. 정답 검증 — `problems/verify.py`
- 모든 문항을 sympy/전수 계산으로 풀어 `ans` 와 대조한다. 조건 문제는 해가 **유일한지**까지 확인(반례 조건 추가).
- `PY problems/verify.py` 출력과 exam.py의 보기·정답 번호를 한 번 더 맞춰 본다.

## 3. 그림 — Codex에게 image gen으로 맡기기
절차 상세는 `reference/codex-figures.md`.
1. `figures/FIGURE_SPEC.md` 작성(그림별 파일 이름·폭 mm·정확한 수치·라벨·음영·스타일).
2. `herdr agent list` 로 codex pane 찾기 → `herdr agent prompt <pane> "...image gen으로..."` 전달.
   출제 직후 바로 보내서 조판과 병렬로 진행시킨다.
3. 기다리는 동안 조판을 진행한다(그림이 없으면 자리표시가 들어감).
4. `herdr agent wait <pane> --until done --until idle --until blocked` 후 모든 PNG를 모아 보고 사양과 대조. 틀리면 수치를 짚어 수정 요청.
5. 사용자가 방식 변경을 지시하면(예: 특정 그림만 직접) 그 지시를 따른다.

## 4. 조판 — `PY tools/build.py`
- `exam.py` → HWPX XML(격자 칸 배치) → 한글 COM으로 열어 **수식 크기 재계산** → `output/<out_name>.hwpx/.pdf`.
- **넘침 검사**가 자동으로 먼저 돈다: 각 칸 끝에 보이지 않는 표식을 넣은 검사용 PDF(`build/check.pdf`)를 만들어 표식 위치로 실제 내용 끝을 재고,
  칸을 넘친 문항을 `영역을 넘친 문항: 공통 13번: 영역 450pt 를 20pt 넘침` 처럼 알려 준다. 그다음 표식 없는 최종본을 만든다.
  - 넘치면: 그 문항을 1칸 단으로 옮기거나(배치 변경), 그림 폭을 줄이거나, 문장·보기 줄 수를 줄인다. `--strict` 를 주면 넘칠 때 실패 코드로 끝난다.
  - (한글은 넘친 칸을 늘려 그리지만 파일의 칸 높이는 그대로 저장하므로 hwpx가 아니라 PDF로 잰다.)
- 실패 메시지가 "결과 파일이 열려 있으면…"이면 사용자에게 한글에서 결과 파일을 닫아 달라고 하거나 `out_name` 을 바꾼다.

## 5. 검수
- `PY tools/render.py` (전체 쪽 PNG, `DPI=` 환경변수로 해상도) → `PY tools/contact.py 1 2 3 4` 로 4쪽씩 이어 붙여 본다.
- 확인 항목: 머리말 홀짝 배치, 쪽 번호(과목별 머리말 / 전체 꼬리말), 단 구분선, 문항 위치, 보기 정렬, 조건 상자, 그림 크기·위치, 확인 사항 상자 문구(다음 선택과목 이름).
- `PY tools/gaps.py` — 양쪽 정렬 때문에 글자 사이가 크게 벌어진 줄을 찾는다(줄 끝에 긴 수식이 못 들어가서 생김).
  40pt 넘게 벌어진 줄은 고친다: 여러 조건을 `$..$, $..$` 로 나누기, 극한·적분 같은 긴 식은 `eq` 가운데 수식으로 빼기, 정의역은 `~(0 <= x <= 8)` 처럼 뒤로.
  조금 벌어진 줄은 원본 수능에도 있으므로 그대로 둬도 된다.
- 원본과 비교가 필요하면 평가원 기출 PDF를 받아 같은 영역을 잘라 나란히 본다(suneung.re.kr 기출문제 게시판 `fileDown.do?fileSeq=`).
- PDF 글꼴 확인: HFT 글꼴은 Type3(`T1`…)로 나온다. 본문이 `HCRBatang`으로만 나오면 글꼴 표가 비었다는 뜻(아래 함정 1).

## 6. 마무리
- `PY tools/answers.py` → `output/정답표.txt`.
- 사용자에게: 결과 파일 경로, 문항 구성·검증 방식, Codex 그림 검수 결과(남은 오차), 원본과 일부러 다르게 한 점("모의" 문구 등)을 보고.

## 알려진 함정 (이미 tools/ 에 반영됨 — 고칠 때 되살리지 말 것)
1. **글꼴 표 순서**: 글꼴은 `char_pr()` 등록 시점에 함께 등록해야 한다. XML 출력 중에 등록하면 첫 빌드의 fontfaces가 비어 전부 바탕체로 대체된다.
2. **수식 크기**: 한글은 hwpx를 열 때 `hp:sz` 를 다시 계산하지 않는다 → COM으로 각 수식 `Properties` 를 다시 넣는다(`-RefreshEquations`).
3. **`$hwp.Clear(3)` 금지**: "저장 후 닫기"라서 입력 파일을 덮어쓴다. 종료는 `Quit()` 만.
4. **권한 팝업**: `RegisterModule("FilePathCheckDLL", "FilePathCheckerModuleExample")` 가 True여야 한다. False면 레지스트리 등록을 확인.
5. **내어쓰기**: HWPX의 음수 `intent` 는 "첫 줄은 left, 둘째 줄부터 |intent| 들여씀". 탭 위치는 단 왼쪽 기준.
6. **단 구분선**: 다단 colLine은 내용 길이만큼만 그려진다 → 쪽마다 고정 위치 검은 막대(vline)로 그린다.
7. **`rm` 범위**: 중괄호로 끝나지 않는다 → 빌드가 `rm X` 뒤에 `it` 을 붙인다.
8. **수식 안 한글 공백**: 따옴표 안 공백은 사라진다 → `"이"~"홀수인"~"경우"`.
9. PowerShell 5.1은 BOM 없는 UTF-8 스크립트의 한글을 깨뜨린다 → `.ps1` 은 ASCII로만.
10. heredoc/셸로 정규식이 든 파이썬을 고치면 `\1` 같은 이스케이프가 깨진다 → Edit 도구나 별도 .py 파일로 수정.
