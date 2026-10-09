"""검수용: 양쪽 정렬 때문에 글자 사이가 지나치게 벌어진 줄을 찾는다.

    python tools/gaps.py [기준pt=16]
본문 줄에서 이웃한 두 글자(수식 글자 포함) 사이 빈칸이 기준보다 넓은 곳이 2군데 이상이면 출력한다.
보기(①~⑤) 줄과 그림·표 안 글자는 제외. 문장을 고치거나 긴 수식을 가운데 수식(eq 블록)으로 빼서 해결한다.
"""
import os
import sys
import pymupdf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "problems"))
import exam  # noqa: E402

limit = float(sys.argv[1]) if len(sys.argv) > 1 else 16.0
pdf = os.path.join(ROOT, "output", exam.META.get("out_name", "수학영역_문제지") + ".pdf")
doc = pymupdf.open(pdf)
out = []
for pno, page in enumerate(doc, 1):
    chars = []
    for b in page.get_text("rawdict")["blocks"]:
        for line in b.get("lines", []):
            for s in line["spans"]:
                for c in s["chars"]:
                    x0, y0, x1, y1 = c["bbox"]
                    if c["c"].strip() and 150 < y0 and y1 < 1067:
                        chars.append((x0, x1, (y0 + y1) / 2, s["size"], c["c"]))
    # 본문 크기(11pt 안팎) 글자로 줄을 잡고, 그 줄 높이 ±7pt 안의 모든 글자(첨자 포함)를 같은 줄로 본다
    body = sorted({round(ch[2]) for ch in chars if 10.5 <= ch[3] <= 12})
    lines, used = [], set()
    for yc in body:
        if any(abs(yc - u) < 6 for u in used):
            continue
        used.add(yc)
        lines.append(yc)
    for yc in lines:
        for col, (lo, hi) in enumerate(((80, 421), (421, 760))):
            row = sorted(ch for ch in chars if lo <= ch[0] < hi and abs(ch[2] - yc) < 7)
            text = "".join(ch[4] for ch in row)
            if len(row) < 4 or any(m in text for m in "①②③④⑤"):
                continue
            gaps = [row[i + 1][0] - row[i][1] for i in range(len(row) - 1)]
            big = [g for g in gaps if g > limit]
            # 줄 끝까지 이어진 본문 줄만 (짧은 마지막 줄은 정렬로 벌어지지 않음)
            if len(big) >= 2 and row[-1][1] > hi - 25:
                out.append(f"p{pno} {'LR'[col]} y={yc}: 빈칸 {len(big)}곳, 최대 {max(big):.0f}pt")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
print("\n".join(out) if out else "벌어진 줄 없음")
