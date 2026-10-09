"""정답표(output/정답표.txt)를 만든다."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "problems"))
import exam  # noqa: E402

MARK = "①②③④⑤"


def fmt(p):
    has_choice = any(b[0] == "ch" for b in p["blocks"])
    a = MARK[p["ans"] - 1] if has_choice else str(p["ans"])
    return f"{p['no']:>2}번  {a:<4} [{p['pts']}점]"


lines = [exam.META["year_title"], "수학 영역 정답표", "", "[공통: 수학Ⅰ·수학Ⅱ]"]
lines += [fmt(p) for p in exam.COMMON]
for name, probs in exam.SUBJECTS:
    lines += ["", f"[선택: {name}]"] + [fmt(p) for p in probs]
suffix = exam.META.get("out_name", "").replace("수학영역_문제지", "")
out = os.path.join(ROOT, "output", f"정답표{suffix}.txt")
open(out, "w", encoding="utf-8").write("\n".join(lines) + "\n")
print("written", out)
