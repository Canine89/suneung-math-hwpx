"""Export image_gen originals at requested print widths and 600 dpi.

This script does NOT draw or repair any mathematical artwork. Generation and
all creative corrections were performed with the built-in image_gen tool.
Original raster files and prompts are preserved beside this script.
Run: python figures/src/export_figures.py
"""
import json
import shutil
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent
DPI = 600


def main():
    records = json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))
    lines = ['Image generation exports; PNG, white background, 600 dpi.',
             'Dimensions below are actual raster dimensions at 600 dpi.', '']
    for record in records:
        raw = ROOT / record['raw_file']
        raw.parent.mkdir(parents=True, exist_ok=True)
        if not raw.exists():
            shutil.copy2(record['source'], raw)
        with Image.open(raw) as source:
            # Packaging only: no redrawing, text replacement, or shape correction.
            canvas = Image.new('RGB', source.size, 'white')
            if source.mode == 'RGBA':
                canvas.paste(source, mask=source.getchannel('A'))
            else:
                canvas.paste(source.convert('RGB'))
            # Trim exterior paper only; retain all mathematical marks and labels.
            ink = canvas.convert('L').point(lambda value: 255 if value < 200 else 0)
            bounds = ink.getbbox()
            if bounds:
                canvas = canvas.crop(bounds)
            width = round(record['width_mm'] * DPI / 25.4)
            margin = round(DPI / 25.4)  # 1 mm white paper on each side
            inner_width = width - 2 * margin
            inner_height = round(canvas.height * inner_width / canvas.width)
            content = canvas.resize((inner_width, inner_height), Image.Resampling.LANCZOS)
            height = inner_height + 2 * margin
            canvas = Image.new('RGB', (width, height), 'white')
            canvas.paste(content, (margin, margin))
            target = OUT / (record['id'] + '.png')
            canvas.save(target, dpi=(DPI, DPI))
        with Image.open(target) as check:
            assert check.mode == 'RGB'
            assert check.width == width
            assert all(abs(value - DPI) < .1 for value in check.info['dpi'])
        line = (f"{target.name}: {width * 25.4 / DPI:.3f} x "
                f"{height * 25.4 / DPI:.3f} mm; {width} x {height} px; "
                f"requested width {record['width_mm']} mm")
        lines.append(line)
        print(line)
    lines += ['', 'Visual review performed; see src/REVIEW.txt.',
              'IMPORTANT: these are AI-generated illustrations, not numerically exact plots.',
              'Strict FIGURE_SPEC numerical/style compliance has NOT been certified.',
              'Generation prompts: src/prompts.json; original rasters: src/raw/.']
    (OUT / 'DONE.txt').write_text('\n'.join(lines) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
