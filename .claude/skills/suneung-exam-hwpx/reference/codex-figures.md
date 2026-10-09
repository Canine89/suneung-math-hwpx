# Codex(오른쪽 탭)에게 그림 맡기기 — image gen 필수

사용자 방침: **문제지 그림은 항상 오른쪽 탭의 Codex 앱이 image gen(이미지 생성 도구)으로 만든다.**
Claude는 그림을 직접 그리지 않는다(matplotlib 대체 금지). 사양서를 쓰고, 전달하고, 검수한다.

## 1. Codex 찾기 (Herdr)
```bash
test "${HERDR_ENV:-}" = 1 || echo "Herdr 밖에서 실행 중 → 사용자에게 전달을 부탁"
HERDR=herdr   # PATH에 없으면: /c/Users/<user>/AppData/Local/Programs/Herdr/bin/herdr.exe
$HERDR agent list            # "agent":"codex" 인 항목의 pane_id (예: w1:p2)
```
pane_id는 매번 `agent list` 로 확인한다(고정값으로 가정하지 말 것).
Herdr 밖이거나 Codex가 없으면, 사용자에게 오른쪽 탭에 Codex를 열어 달라고 하거나 요청문을 직접 붙여 넣어 달라고 한다.

## 2. 사양서 쓰기 — `figures/FIGURE_SPEC.md`
`templates/FIGURE_SPEC_example.md` 형식을 따른다. 그림마다:
- 파일 이름 `fig_<과목><번호>` (공통 c, 확통 s, 미적분 m, 기하 g) 예: `fig_c07`, `fig_m26`
- 인쇄 가로 폭 mm (보통 50–70)
- 문제 원문 요지, **정확한 좌표/수치**(극점·교점 x값, 길이 비), 칠할 영역, 라벨 목록과 위치
- 공통 스타일 규칙(흑백, 0.6 pt, #D9D9D9, 눈금 없음, 600 dpi 흰 배경 PNG)

`problems/exam.py` 에는 `('fig', 'fig_c07', 60)` 블록으로 넣는다. 그림이 없으면 같은 크기 자리표시가 들어간다.

## 3. 요청 보내기
```bash
$HERDR agent prompt <codex-pane> "안녕하세요, 옆 탭의 Claude입니다. 수능형 문제지의 그림을 맡아 주세요.
<프로젝트>\figures\FIGURE_SPEC.md 를 읽고 그림 N개(fig_..., ...)를 같은 폴더에 PNG(600dpi, 흰 배경)로 만들어 주세요.
그림은 반드시 image gen(이미지 생성 도구)으로 만들고, 생성 후 사양의 수치·라벨과 맞는지 직접 확인해 주세요.
프롬프트는 figures/src/prompts.json 에 남기고, 끝나면 figures/DONE.txt 를 만들어 주세요.
problems/, tools/, output/ 은 건드리지 말아 주세요."
```
완료 대기: `$HERDR agent wait <codex-pane> --until done --until idle --until blocked --timeout 580000`
(blocked 면 Codex 쪽에서 승인이 필요한 상태 → 사용자에게 알린다.)

## 4. 검수 (Claude 책임)
- 모든 PNG를 한 장으로 모아(`PIL`) 직접 본다.
- 확인 항목: 극점·교점 위치와 **간격 비율**, 선분이 곡선과 겹치지 않는지, 음영 영역이 문제 정의와 같은지,
  점 이름·식 라벨, 직각 표시, 숨은 모서리 점선.
- 틀리면 구체적 수치로 수정 요청(같은 파일명 덮어쓰기, image gen 편집). 예: "B와 C의 가로 간격이 A–B 간격과 같아야 함(4:4)".
- image gen 특성상 미세 비율 오차(~10%)는 남을 수 있다. 문제에 필요한 수치가 모두 본문에 있으면 허용(수능 그림도 개략도).
- 그림 도착 후 `python tools/build.py` 를 다시 돌리면 자동 반영된다.
