import json
import shutil
from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parent.parent
revisions = json.loads((root / 'src/revision_20261010.json').read_text(encoding='utf-8'))
manifest_path = root / 'src/prompts.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
manifest.setdefault('revisions', []).append({'date': '2026-10-10', 'edits': revisions})
notes = {
 'c08': 'image gen 편집: 포물선 식을 가파른 상단 가지 옆, 직선 식을 그 아래 오른쪽으로 이동. 기하·음영 유지 확인. 생성 편집상 미세 위치 변화.',
 'c10': 'image gen 3회 편집: 회색 사각형의 BD가 D, CA가 C에 연결되는 수정본 저장. 검수 미통과: C가 B 거의 바로 아래, D는 곡선에서 벗어남; x 등간격(1,3,5,7) 불충족. 확정본 사용 불가.',
}
for key, entry in revisions.items():
    ident = 'fig_' + key
    target = root / (ident + '.png')
    shutil.copy2(target, root / 'src/raw' / (ident + '_before_revision_20261010.png'))
    raw = root / 'src/raw' / (ident + '_revision_20261010.png')
    shutil.copy2(entry['source'], raw)
    im = Image.open(raw).convert('RGB')
    bbox = im.convert('L').point(lambda p: 255 if p < 200 else 0).getbbox()
    if bbox:
        im = im.crop(bbox)
    width = round(entry['width'] * 600 / 25.4)
    margin = round(600 / 25.4)
    inner = width - 2 * margin
    height = round(im.height * inner / im.width)
    im = im.resize((inner, height), Image.Resampling.LANCZOS)
    canvas = Image.new('RGB', (width, height + 2 * margin), 'white')
    canvas.paste(im, (margin, margin))
    canvas.save(target, dpi=(600,600))
    check = Image.open(target)
    assert check.mode == 'RGB' and check.width == width
    assert all(abs(d-600)<.01 for d in check.info['dpi'])
    manifest['selected_sources'][ident] = entry['source']
    with (root / 'DONE.txt').open('a', encoding='utf-8') as done:
        done.write(f'2026-10-10 수정 {ident}.png: {width*25.4/600:.2f} × {check.height*25.4/600:.2f} mm, {width} × {check.height} px, 600dpi, RGB 흰 배경; {notes[key]}\n')
    print(ident, check.size, check.info['dpi'])
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
