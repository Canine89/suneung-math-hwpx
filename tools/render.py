"""output pdf 를 쪽별 PNG 로 (검토용)."""
import os, sys, pymupdf
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "problems"))
import exam  # noqa: E402
pdf = os.path.join(ROOT, "output", exam.META.get("out_name", "수학영역_문제지") + ".pdf")
outdir = os.path.join(ROOT, "build", "png")
os.makedirs(outdir, exist_ok=True)
doc = pymupdf.open(pdf)
pages = [int(a) for a in sys.argv[1:]] or range(1, doc.page_count + 1)
dpi = int(os.environ.get("DPI", "80"))
for p in pages:
    doc[p - 1].get_pixmap(dpi=dpi).save(os.path.join(outdir, f"p{p:02d}.png"))
print(doc.page_count, "pages; fonts:", sorted({f[3] for i in range(min(3, doc.page_count)) for f in doc[i].get_fonts()}))
