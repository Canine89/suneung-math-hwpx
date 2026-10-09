"""검토용: 쪽 PNG 여러 장을 한 장으로 이어 붙인다.  python contact.py 1 2 3 4"""
import os, sys
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ims = [Image.open(os.path.join(ROOT, "build", "png", f"p{int(a):02d}.png")) for a in sys.argv[1:]]
w, h = ims[0].size
sheet = Image.new("RGB", (w * len(ims), h), "white")
for i, im in enumerate(ims):
    sheet.paste(im, (i * w, 0))
sheet.save(os.path.join(ROOT, "build", "png", "sheet.png"))
