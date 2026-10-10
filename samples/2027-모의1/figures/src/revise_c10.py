"""Package selected image_gen revision only; no mathematical drawing."""
import json
import shutil
from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parent
out = root.parent
source = Path(r'C:\Users\canine89\.codex\generated_images\01a120d6-ef13-7ce3-b231-e1b921932542\exec-d894b5f1-ab79-40dd-8aff-37958d0ac051.png')
raw = root / 'raw/fig_c10_revision.png'
if not (root / 'raw/fig_c10_before_revision.png').exists():
    shutil.copy2(out / 'fig_c10.png', root / 'raw/fig_c10_before_revision.png')
shutil.copy2(source, raw)
with Image.open(raw) as image:
    image = image.convert('RGB')
    bounds = image.convert('L').point(lambda v: 255 if v < 200 else 0).getbbox()
    if bounds:
        image = image.crop(bounds)
    width, margin = round(70 * 600 / 25.4), round(600 / 25.4)
    inner_width = width - 2 * margin
    inner_height = round(image.height * inner_width / image.width)
    image = image.resize((inner_width, inner_height), Image.Resampling.LANCZOS)
    result = Image.new('RGB', (width, inner_height + 2 * margin), 'white')
    result.paste(image, (margin, margin))
    result.save(out / 'fig_c10.png', dpi=(600, 600))
with Image.open(out / 'fig_c10.png') as check:
    assert check.mode == 'RGB' and check.width == width
    assert all(abs(v - 600) < .1 for v in check.info['dpi'])
    print(check.size, check.info['dpi'])
manifest_path = root / 'manifest.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
for record in manifest:
    if record['id'] == 'fig_c10':
        record['source'] = str(source)
        record['raw_file'] = 'raw/fig_c10_revision.png'
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
with (out / 'DONE.txt').open('a', encoding='utf-8') as log:
    log.write(f'fig_c10.png revision: image_gen; 600dpi; {width * 25.4 / 600:.3f} x {(inner_height + 2 * margin) * 25.4 / 600:.3f} mm; BC/curve separated and curve ends on x-axis; A-B horizontal gap ~392px vs B-C ~430px in generated original (~10% residual mismatch), exact sine spacing not achieved.\n')
