"""수능 수학 영역 문제지 hwpx 생성기.

사용법:  python tools/build.py
 1) problems/exam.py 를 읽어 hwpx XML 을 만든다.
 2) 한글 COM 으로 열어 수식 크기를 다시 계산하고 hwpx/pdf 로 저장한다.
 3) pdf 에서 문항 번호 위치를 재서, 한 단의 두 번째 문항이 원본 수능과 같은 높이에 오도록
    간격을 보정한 뒤 한 번 더 만든다.
"""
import os
import re
import sys
import json
import shutil
import subprocess
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, os.path.join(ROOT, "problems"))

import hwpx as X  # noqa: E402
from hwpx import PT, MM  # noqa: E402
import exam  # noqa: E402

BUILD = os.path.join(ROOT, "build")
OUT = os.path.join(ROOT, "output")
FIG = os.path.join(ROOT, "figures")
COM = os.path.join(ROOT, "tools", "hwp_com.ps1")
OUT_NAME = exam.META.get("out_name", "수학영역_문제지")

# ---------------------------------------------------------------- 쪽 치수 (원본 PDF 실측, pt)
PAGE_W, PAGE_H = 841.89, 1190.55
HDR_LINE = 147.4                                           # 머리말 아래 굵은 선의 y
MARGIN = dict(left=87.8, right=87.8, top=107.8, header=39.6 + 12.0, footer=56.0)
MARGIN["bottom"] = PAGE_H - 1067.2 - MARGIN["footer"]
BODY_W = PAGE_W - MARGIN["left"] - MARGIN["right"]       # 666.3
COL_GAP = 31.2
COL_W = (BODY_W - COL_GAP) / 2                             # 317.6
HANG = 11.3                                                # 문항 내어쓰기
SIDE_W = 120.0

H = X.Header()

# ---------------------------------------------------------------- 글자 모양
BODY_FONT, LATIN_FONT = "신명 중명조", "한양신명조"
C_BODY = H.char_pr(BODY_FONT, LATIN_FONT, 11.2)
C_NUM = H.char_pr("한양견명조", "한양견명조", 12.7)
C_LABEL = H.char_pr("신명 태고딕", "신명 태고딕", 14.5, spacing=12)
C_PAGENO = H.char_pr("신명 견명조", "신명 견명조", 31.3)
C_TITLE = H.char_pr("한양견고딕", "한양견고딕", 29.0, ratio=90)
C_TITLE_SUB = H.char_pr("한양견고딕", "한양견고딕", 24.0, ratio=90)
C_TITLE_BIG = H.char_pr("한양견고딕", "한양견고딕", 41.0, ratio=92, spacing=-6)
C_TITLE_BIG_SUB = H.char_pr("한양견고딕", "한양견고딕", 33.0, ratio=92, spacing=-6)
C_HOLSU = H.char_pr("한양견고딕", "한양견고딕", 18.9)
C_HOLSU_BIG = H.char_pr("한양견고딕", "한양견고딕", 25.8)
C_GYOSI = H.char_pr("한양견명조", "한양견명조", 19.7, ratio=92, spacing=-8)
C_YEAR = H.char_pr("신명 디나루", "신명 디나루", 19.4)
C_FOOTNO = H.char_pr("신명 견명조", "신명 견명조", 11.7)
C_COPY = H.char_pr("굴림체", "굴림체", 10.0, color="#0000FF")
C_CHK = H.char_pr("신명 중고딕", "신명 중고딕", 10.7, symbol="한양신명조")
C_CHK_B = H.char_pr("신명 태고딕", "신명 태고딕", 10.7)
C_CHK_SYM = H.char_pr("한양신명조", "한양신명조", 10.7)
C_TINY = H.char_pr(BODY_FONT, LATIN_FONT, 1.0)

# ---------------------------------------------------------------- 문단 모양
LS = 165  # 줄 간격(%)
P_FIRST = H.para_pr("JUSTIFY", left=0, indent=-HANG*PT, line=LS)
P_CONT = H.para_pr("JUSTIFY", left=HANG*PT, line=LS)
P_EQ = H.para_pr("LEFT", left=41.0*PT, prev=5*PT, next=5*PT, line=LS)
TABS = [(HANG + 61.25*i)*PT for i in range(1, 5)]
P_CH = H.para_pr("LEFT", left=HANG*PT, prev=11*PT, line=LS, tabs=TABS)
P_CH2 = H.para_pr("LEFT", left=HANG*PT, prev=4*PT, line=LS, tabs=TABS)
P_CH3 = H.para_pr("LEFT", left=HANG*PT, prev=11*PT, line=LS, tabs=[(HANG + 61.25*2)*PT])
P_CH3B = H.para_pr("LEFT", left=HANG*PT, prev=4*PT, line=LS, tabs=[(HANG + 61.25*2)*PT])
P_BOX = H.para_pr("LEFT", left=HANG*PT, prev=7*PT, next=7*PT, line=LS)
P_FIG = H.para_pr("CENTER", left=HANG*PT, prev=10*PT, next=4*PT, line=100)
P_INBOX = H.para_pr("LEFT", left=0, indent=-25*PT, line=LS)
P_SIDE = H.para_pr("LEFT", line=LS)
P_CELLC = H.para_pr("CENTER", line=130)
P_LABEL = H.para_pr("LEFT", next=18*PT, line=100)
P_LEFT0 = H.para_pr("LEFT", line=100)
P_GYOSI = H.para_pr("LEFT", prev=11*PT, line=100)
P_CENTER0 = H.para_pr("CENTER", line=100)
P_RIGHT0 = H.para_pr("RIGHT", line=100)
P_HDR_L = H.para_pr("LEFT", line_type="FIXED", line=36*PT)
P_HDR_C = H.para_pr("CENTER", line_type="FIXED", line=36*PT)
P_HDR_R = H.para_pr("RIGHT", line_type="FIXED", line=36*PT)
P_FOOT1 = H.para_pr("CENTER", prev=14.9*PT, line=100)
P_FOOT2 = H.para_pr("RIGHT", right=-15.7*PT, line=100)
P_FNO_L = H.para_pr("LEFT", line_type="FIXED", line=10.5*PT)
P_FNO_R = H.para_pr("RIGHT", line_type="FIXED", line=10.5*PT)
P_CHK = H.para_pr("LEFT", left=0, indent=-12*PT, prev=2.5*PT, line=150)

# ---------------------------------------------------------------- 테두리
BF_NONE = 1
BF_BOX = H.box("0.12 mm")
BF_HDR = H.border_fill(bottom="SOLID", widths={"bottom": "0.4 mm"})
BF_BIG = H.border_fill(bottom="SOLID", widths={"bottom": "0.4 mm"}, fill="#FFFFFF")
BF_WHITE = H.border_fill(fill="#FFFFFF")
BF_FOOT = H.border_fill("SOLID", "SOLID", "SOLID", "SOLID", width="0.12 mm", slash=True)


# ================================================================ 조각 함수
def eq_size(script):
    n = len(re.sub(r"\s+", "", script))
    tall = any(k in script for k in ("over", "sum", "int", "cases", "lim"))
    return max(600, n * 330), (2600 if tall else 1300)


def eq(script):
    script = re.sub(r"cases\{(.*?)#(.*)\}", lambda m: "cases{" + m.group(1) + "#` & `#" + m.group(2) + "}", script)
    # 한글 수식의 rm 은 중괄호로 범위가 끝나지 않으므로, 정체로 쓸 낱말 뒤에 it 를 붙여 기울임으로 되돌린다.
    script = re.sub(r"rm ([A-Za-z']+)(?! it\b)", r"rm \1 it", script)
    w, hh = eq_size(script)
    return X.equation(script, 1100, w, hh)


def rich(text, char=None):
    """'$수식$' 이 섞인 문장을 run 목록으로."""
    char = C_BODY if char is None else char
    runs = []
    for i, seg in enumerate(text.split("$")):
        if not seg:
            continue
        if i % 2 == 1:
            runs.append(X.run(char, eq(seg)))
        else:
            runs.append(X.run(char, X.t(seg)))
    return runs


def label_table(kind):
    text, w = ("5지선다형", 110.5) if kind == "MC" else ("단답형", 78.5)
    cell = [X.para(P_CENTER0, [X.run(C_LABEL, X.t(text))])]
    return X.table([[cell]], [w*PT], [23.4*PT], BF_BOX, in_margin=(0, 0, 0, 0))


def choice_paras(items, rows):
    marks = "①②③④⑤"
    if rows == 1:
        groups = [list(range(5))]
    elif rows == 2:
        groups = [[0, 1, 2], [3, 4]]
    else:  # 아주 긴 보기: 한 줄에 둘씩 (①② / ③④ / ⑤)
        groups = [[0, 1], [2, 3], [4]]
    out = []
    for gi, g in enumerate(groups):
        runs = []
        for j, k in enumerate(g):
            sep = "" if j == 0 else ("\t" if rows in (1, 3) else "\t\t")
            runs.append(X.run(C_BODY, X.t(f"{sep}{marks[k]} ")))
            runs.append(X.run(C_BODY, eq(items[k])))
        if rows == 3:  # 둘씩 놓을 때는 단 가운데 근처 탭 하나만 쓴다 (긴 보기가 탭을 건너뛰지 않게)
            out.append(X.para(P_CH3 if gi == 0 else P_CH3B, runs))
        else:
            out.append(X.para(P_CH if gi == 0 else P_CH2, runs))
    return out


def box_table(lines):
    cell = [X.para(P_INBOX, rich(s)) for s in lines]
    w = COL_W - HANG
    return X.table([[cell]], [w*PT], [10*PT*len(lines)], BF_BOX, in_margin=(1100, 1100, 650, 650))


def side_block(lines, ztable):
    left = [X.para(P_SIDE, rich(s)) for s in lines]
    rows = [[[X.para(P_CELLC, [X.run(C_BODY, eq("z"))])],
             [X.para(P_CELLC, [X.run(C_BODY, eq("{rm P} left ( 0 <= Z <= z right )"))])]]]
    for z, p in ztable:
        rows.append([[X.para(P_CELLC, [X.run(C_BODY, eq(z))])], [X.para(P_CELLC, [X.run(C_BODY, eq(p))])]])
    zt = X.table(rows, [38*PT, 74*PT], [17*PT]*len(rows), BF_BOX, in_margin=(200, 200, 100, 100))
    right = [X.para(P_RIGHT0, [X.run(C_BODY, zt)])]
    w = COL_W - HANG
    return X.table([[left, right]], [(w-114)*PT, 114*PT], [100*PT], BF_NONE, in_margin=(0, 0, 0, 0),
                   valign="TOP")


FIG_CACHE = {}


def figure(name, width_mm, images):
    from PIL import Image, ImageDraw
    path = os.path.join(FIG, name + ".png")
    if not os.path.exists(path):
        # 코덱스 그림이 오기 전까지 같은 크기의 자리표시 그림
        path = os.path.join(BUILD, name + "_placeholder.png")
        if not os.path.exists(path):
            w, hh = int(width_mm / 25.4 * 300), int(width_mm * 0.75 / 25.4 * 300)
            im = Image.new("RGB", (w, hh), "white")
            d = ImageDraw.Draw(im)
            for x0 in range(0, w, 40):
                d.line((x0, 2, x0 + 20, 2), fill="#999999", width=3)
                d.line((x0, hh - 3, x0 + 20, hh - 3), fill="#999999", width=3)
            for y0 in range(0, hh, 40):
                d.line((2, y0, 2, y0 + 20), fill="#999999", width=3)
                d.line((w - 3, y0, w - 3, y0 + 20), fill="#999999", width=3)
            im.save(path)
    im = Image.open(path)
    pw, ph = im.size
    iid = f"image{len(images) + 1}"
    images.append((iid, path))
    W = width_mm * MM
    return X.picture(iid, W, W * ph / pw, pw, ph)


def problem_paras(p):
    """문항 하나의 문단 목록 (영역 칸 안에 들어간다)."""
    blocks = p["blocks"]
    pts_tag = f" [{p['pts']}점]"
    last_t = max(i for i, b in enumerate(blocks) if b[0] in ("t",))
    out = []
    first = True
    for i, b in enumerate(blocks):
        kind = b[0]
        if kind == "t":
            text = b[1] + (pts_tag if (i == last_t and not p.get("manual_pts")) else "")
            if first:
                runs = [X.run(C_NUM, X.t(f"{p['no']}.")), X.run(C_BODY, X.t(" "))] + rich(text)
                out.append(X.para(P_FIRST, runs))
                first = False
            else:
                out.append(X.para(P_CONT, rich(text)))
        elif kind == "eq":
            out.append(X.para(P_EQ, [X.run(C_BODY, eq(b[1]))]))
        elif kind == "box":
            out.append(X.para(P_BOX, [X.run(C_BODY, box_table(b[1]))]))
        elif kind == "side":
            out.append(X.para(P_BOX, [X.run(C_BODY, side_block(b[1], b[2]))]))
        elif kind == "fig":
            out.append(X.para(P_FIG, [X.run(C_BODY, figure(b[1], b[2], STATE["images"]))]))
        elif kind == "ch":
            rows = b[2] if len(b) > 2 else (2 if any(len(c) > 22 for c in b[1]) else 1)
            out.extend(choice_paras(b[1], rows))
    return out


# ---------------------------------------------------------------- 머리말 / 꼬리말
def holsu_box(big=False):
    w, hh = (80.7, 44.0) if big else (59.5, 29.7)
    inner = [X.para(P_CENTER0, [X.run(C_HOLSU_BIG if big else C_HOLSU, X.t(exam.META["type"]))])]
    return X.rounded_box(inner, w*PT, hh*PT, ratio=12)


def title_runs(subject, big):
    main, sub = (C_TITLE_BIG, C_TITLE_BIG_SUB) if big else (C_TITLE, C_TITLE_SUB)
    runs = [X.run(main, X.t("수학 영역"))]
    if subject:
        runs.append(X.run(sub, X.t(f"({subject})")))
    return runs


def page_header_ctrl(local_no, subject):
    odd = local_no % 2 == 1
    num = [X.run(C_PAGENO, X.t(str(local_no)))]
    box = [X.run(C_BODY, holsu_box())]
    left = [X.para(P_HDR_L, box if odd else num)]
    right = [X.para(P_HDR_R, num if odd else box)]
    center = [X.para(P_HDR_C, title_runs(subject, False))]
    tbl = X.table([[left, center, right]], [SIDE_W*PT, (BODY_W-2*SIDE_W)*PT, SIDE_W*PT], [(HDR_LINE - MARGIN["top"])*PT],
                  BF_HDR, in_margin=(0, 0, 0, 0), valign="TOP")
    p = X.para(P_LEFT0, [X.run(C_BODY, tbl)])
    return X.run(C_BODY, X.header_ctrl([p], BODY_W*PT, MARGIN["header"]*PT, "header"))


def empty_header_ctrl():
    p = X.para(P_LEFT0, [X.run(C_BODY, X.t(""))])
    return X.run(C_BODY, X.header_ctrl([p], BODY_W*PT, MARGIN["header"]*PT, "header"))


def footer_ctrl(global_no, total):
    cell = [X.para(P_FNO_L, [X.run(C_FOOTNO, X.t(str(global_no)))]),
            X.para(P_FNO_R, [X.run(C_FOOTNO, X.t(str(total)))])]
    tbl = X.table([[cell]], [51*PT], [22*PT], BF_FOOT, in_margin=(250, 250, 0, 0))
    p1 = X.para(P_FOOT1, [X.run(C_BODY, tbl)])
    p2 = X.para(P_FOOT2, [X.run(C_COPY, X.t(exam.META["copyright"]))])
    return X.run(C_BODY, X.header_ctrl([p1, p2], BODY_W*PT, MARGIN["footer"]*PT, "footer"))


def big_header(subject):
    """1쪽(및 선택과목 첫 쪽) 상단: 흰 바탕 표를 머리말 위에 덮는다 (원본과 같은 방식)."""
    r1 = [[X.para(P_LEFT0, [X.run(C_BODY, X.t(""))])],
          [X.para(P_HDR_C, [X.run(C_YEAR, X.t(exam.META["year_title"]))])],
          [X.para(P_HDR_R, [X.run(C_PAGENO, X.t("1"))])]]
    gyosi = X.rounded_box([X.para(P_CENTER0, [X.run(C_GYOSI, X.t(exam.META["period"]))])],
                          90.7*PT, 31.2*PT, ratio=50)
    r2 = [[X.para(P_GYOSI, [X.run(C_BODY, gyosi)])],
          [X.para(P_CENTER0, title_runs(subject, True))],
          [X.para(P_RIGHT0, [X.run(C_BODY, holsu_box(True))])]]
    pos = X.pos_xml(False, vrel="PAPER", hrel="PAPER", voff=107.8*PT, hoff=MARGIN["left"]*PT, flow=False)
    va = [["TOP", "CENTER", "TOP"], ["TOP", "CENTER", "CENTER"]]
    return X.table([r1, r2], [SIDE_W*PT, (BODY_W-2*SIDE_W)*PT, SIDE_W*PT], [39.6*PT, 70.9*PT],
                   BF_WHITE, cell_fills=[[BF_WHITE]*3, [BF_BIG]*3], pos=pos, in_margin=(0, 0, 0, 0),
                   out_margin=(0, 0, 0, 12.8*PT), valign=va, z=5)


def check_box(next_subject):
    sym = lambda s: X.run(C_CHK_SYM, X.t(s))
    paras = [X.para(P_LEFT0, [sym("＊"), X.run(C_CHK, X.t(" 확인 사항"))]),
             X.para(P_CHK, [sym("◦ "), X.run(C_CHK, X.t("답안지의 해당란에 필요한 내용을 정확히 기입(표기)했는지 확인하시오."))])]
    if next_subject:
        paras.append(X.para(P_CHK, [sym("◦ "), X.run(C_CHK, X.t("이어서, ")), sym("｢"),
                                    X.run(C_CHK_B, X.t(f"선택과목({next_subject})")), sym("｣"),
                                    X.run(C_CHK, X.t(" 문제가 제시되오니, 자신이 선택한 과목인지 확인하시오."))]))
    top, hgt = (964.6, 102.6) if next_subject else (1003.9, 63.3)
    pos = X.pos_xml(False, vrel="PAPER", hrel="COLUMN", voff=top*PT, hoff=0, flow=False)
    return X.table([[paras]], [COL_W*PT], [hgt*PT], BF_BOX, pos=pos, in_margin=(1000, 1000, 700, 500),
                   valign="TOP")


# ================================================================ 문서 조립
STATE = {"images": [], "markers": None}


# ---------------------------------------------------------------- 쪽 격자(영역) 배치
# 한 쪽 = 왼쪽·오른쪽 단, 한 단 = 문항 1개(1칸) 또는 2개(위/아래 2칸).
# 각 문항은 쪽 위치에 고정된 테두리 없는 영역(1칸 표) 안에 들어간다 → 앞 문항 길이와 무관하게 자리가 정해지고,
# 내용이 영역보다 길면 한글이 칸을 늘리므로 저장 후 칸 높이를 읽어 넘친 문항을 알려 준다.
BODY_TOP = HDR_LINE + 12.0      # 일반 쪽 영역 시작 (머리말 선 아래)
FIRST_TOP = 231.1               # 과목 첫 쪽 (큰 제목 아래, 원본 5지선다형 상자 위치)
BODY_BOTTOM = 1067.2
NUM_OFFSET = 6.6                # 영역 위쪽 → 문항 번호 글자 윗변 거리 (실측)
COL_X = (MARGIN["left"], MARGIN["left"] + COL_W + COL_GAP)
CHECK_TOP = {True: 964.6, False: 1003.9}   # 확인 사항 상자 위쪽 (다음 과목 있음/없음)


def column_regions(col, top, bottom, part):
    """단 항목 목록 → [(위, 아래, [항목...])]. 'MC'/'SA' 표시는 다음 문항 영역 맨 위에 붙는다."""
    groups, pending = [], []
    for item in col:
        if item in ("MC", "SA"):
            pending.append(item)
        else:
            groups.append(pending + [item])
            pending = []
    if len(groups) == 1:
        return [(top, bottom, groups[0])]
    second_no = groups[1][-1]
    split = exam.SECOND_TARGET.get(second_no) if part is None else None
    split = (split - NUM_OFFSET) if split else round((top + bottom) / 2)
    return [(top, split, groups[0]), (split, bottom, groups[1])]


C_MARK = H.char_pr(BODY_FONT, LATIN_FONT, 1.0, color="#FFFFFF")


def region_table(items, bynum, x, top, bottom, key):
    paras = []
    for item in items:
        if item in ("MC", "SA"):
            paras.append(X.para(P_LABEL, [X.run(C_BODY, label_table(item))]))
        else:
            paras.extend(problem_paras(bynum[item]))
    if STATE["markers"] is not None:
        # 넘침 검사용 빌드에서만: 영역 끝에 보이지 않는 표식 → PDF에서 위치를 읽어 실제 내용 끝을 안다
        idx = len(STATE["markers"])
        STATE["markers"].append((key, top, bottom))
        paras.append(X.para(P_LEFT0, [X.run(C_MARK, X.t(f"QEND{idx:03d}"))]))
    pos = X.pos_xml(False, vrel="PAPER", hrel="PAPER", voff=top*PT, hoff=x*PT, flow=False, overlap=True)
    return X.table([[paras]], [COL_W*PT], [(bottom - top)*PT], BF_NONE, pos=pos, in_margin=(0, 0, 0, 0),
                   valign="TOP", wrap="IN_FRONT_OF_TEXT")


def build_xml():
    STATE["images"] = []
    parts = [(None, exam.COMMON, exam.COMMON_LAYOUT)] + [(s, probs, exam.ELECTIVE_LAYOUT) for s, probs in exam.SUBJECTS]
    total = sum(len(lay) for _, _, lay in parts)
    paragraphs = []
    gno = 0
    for pi, (subject, probs, layout) in enumerate(parts):
        bynum = {p["no"]: p for p in probs}
        next_subject = exam.SUBJECTS[pi][0] if pi < len(exam.SUBJECTS) else None
        for li, (lcol, rcol) in enumerate(layout):
            gno += 1
            local = li + 1
            last = li == len(layout) - 1
            runs = []
            if gno == 1:
                runs.append(X.run(C_BODY, X.sec_pr(PAGE_W*PT, PAGE_H*PT,
                                                   {kk: v*PT for kk, v in MARGIN.items()}, COL_GAP*PT)))
            if local == 1:
                runs += [empty_header_ctrl(), X.run(C_BODY, big_header(subject))]
            else:
                runs.append(page_header_ctrl(local, subject))
            runs.append(footer_ctrl(gno, total))
            line_top = 218.3 if local == 1 else HDR_LINE
            runs.append(X.run(C_BODY, X.vline((PAGE_W/2 - 0.42)*PT, line_top*PT, (BODY_BOTTOM - line_top)*PT)))
            top = FIRST_TOP if local == 1 else BODY_TOP
            for ci, col in enumerate((lcol, rcol)):
                bottom = BODY_BOTTOM
                if ci == 1 and last:
                    pos = X.pos_xml(False, vrel="PAPER", hrel="PAPER", voff=CHECK_TOP[bool(next_subject)]*PT,
                                    hoff=COL_X[1]*PT, flow=False)
                    runs.append(X.run(C_BODY, check_box(next_subject).replace(
                        X.pos_xml(False, vrel="PAPER", hrel="COLUMN", voff=CHECK_TOP[bool(next_subject)]*PT,
                                  hoff=0, flow=False), pos)))
                    bottom = CHECK_TOP[bool(next_subject)] - 8
                for (t0, t1, items) in column_regions(col, top, bottom, subject):
                    key = f"{subject or '공통'} {items[-1]}번"
                    runs.append(X.run(C_BODY, region_table(items, bynum, COL_X[ci], t0, t1, key)))
            runs.append(X.run(C_BODY, X.t("")))
            p = X.para(P_LEFT0, runs)
            if gno > 1:
                p = p.replace('pageBreak="0"', 'pageBreak="1"', 1)
            paragraphs.append(p)
    return X.section_xml(paragraphs)


def write_hwpx(section, path):
    tmp = os.path.join(BUILD, "pkg")
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(os.path.join(tmp, "Contents"))
    os.makedirs(os.path.join(tmp, "META-INF"))
    os.makedirs(os.path.join(tmp, "BinData"))
    images = [(iid, f"{iid}.png") for iid, _ in STATE["images"]]
    for (iid, src) in STATE["images"]:
        shutil.copy(src, os.path.join(tmp, "BinData", f"{iid}.png"))
    files = {
        "mimetype": "application/hwp+zip",
        "version.xml": X.VERSION_XML,
        "settings.xml": X.SETTINGS_XML,
        "META-INF/container.xml": X.CONTAINER_XML,
        "META-INF/manifest.xml": X.MANIFEST_XML,
        "Contents/content.hpf": X.content_hpf("수학 영역 문제지", images),
        "Contents/header.xml": H.xml(),
        "Contents/section0.xml": section,
    }
    with zipfile.ZipFile(path, "w") as z:
        z.writestr(zipfile.ZipInfo("mimetype"), files.pop("mimetype"), compress_type=zipfile.ZIP_STORED)
        for name, data in files.items():
            z.writestr(name, data.encode("utf-8"), compress_type=zipfile.ZIP_DEFLATED)
        for iid, fn in images:
            z.write(os.path.join(tmp, "BinData", fn), f"BinData/{fn}", compress_type=zipfile.ZIP_STORED)


def com_finalize(raw, out_hwpx, out_pdf):
    cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", COM,
           "-In", raw, "-OutPdf", out_pdf, "-RefreshEquations"]
    if out_hwpx:
        cmd += ["-OutHwpx", out_hwpx]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="cp949", errors="replace")
    print(r.stdout.strip())
    if r.returncode != 0 or (out_hwpx and "hwpx: True" not in r.stdout) or "pdf: True" not in r.stdout:
        print(r.stderr)
        raise SystemExit("한글 COM 처리 실패 (결과 파일이 한글에서 열려 있으면 닫고 다시 실행하세요)")


def check_overflow(pdf, markers):
    """검사용 PDF에서 각 영역 끝 표식의 위치를 읽어, 정해진 영역 아래로 내려간 문항을 찾는다.
    (한글은 넘친 칸을 늘려 그리지만 파일의 칸 높이는 그대로 두므로 PDF로 잰다)"""
    import pymupdf
    found = {}
    for page in pymupdf.open(pdf):
        for w in page.get_text("words"):
            m = re.fullmatch(r"QEND(\d{3})", w[4])
            if m:
                found[int(m.group(1))] = w[1]
    over = []
    for idx, (key, top, bottom) in enumerate(markers):
        y = found.get(idx)
        if y is None:
            over.append(f"{key}: 끝 표식을 찾지 못함 (다음 쪽으로 밀렸을 수 있음)")
        elif y > bottom:
            over.append(f"{key}: 영역 {bottom - top:.0f}pt 를 {y - bottom:.0f}pt 넘침")
    return over


def main():
    os.makedirs(BUILD, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    raw = os.path.join(BUILD, "raw.hwpx")
    out_hwpx = os.path.join(OUT, OUT_NAME + ".hwpx")
    out_pdf = os.path.join(OUT, OUT_NAME + ".pdf")
    # 1) 넘침 검사용 빌드 (영역 끝 표식 포함, PDF만)
    STATE["markers"] = []
    raw_check = os.path.join(BUILD, "raw_check.hwpx")   # 한글이 늦게 놓아 줄 수 있어 최종본과 다른 파일 사용
    write_hwpx(build_xml(), raw_check)
    com_finalize(raw_check, "", os.path.join(BUILD, "check.pdf"))
    over = check_overflow(os.path.join(BUILD, "check.pdf"), STATE["markers"])
    if over:
        print("영역을 넘친 문항 (쪽 배치를 바꾸거나 그림·문장을 줄이세요):")
        print("\n".join("  " + o for o in over))
    else:
        print("넘친 문항 없음")
    # 2) 최종 빌드 (표식 없음)
    STATE["markers"] = None
    write_hwpx(build_xml(), raw)
    com_finalize(raw, out_hwpx, out_pdf)
    print("완료:", out_hwpx)
    if over and "--strict" in sys.argv:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
