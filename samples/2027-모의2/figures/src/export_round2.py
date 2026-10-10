"""Package image-gen originals; no mathematical drawing or creative editing."""
import json
import shutil
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
manifest = json.loads((ROOT / 'src/prompts.json').read_text(encoding='utf-8'))
raw = ROOT / 'src/raw'
raw.mkdir(parents=True, exist_ok=True)
notes = {
 'fig_c08': '교점·음영·라벨 확인. 곡선 수치와 선 굵기는 생성 이미지의 근사값.',
 'fig_c10': '검수 미통과: A-B/B-C/C-D 수평 간격 불일치, BD 끝이 D에 연결되지 않음, AC 일부가 곡선과 겹침. 반복 재생성·편집 후에도 큰 오차 잔존. 문제지 삽입용 확정본 아님.',
 'fig_c14': '6개 선분과 라벨 확인. AD=CD 길이와 좌표에 약 10% 수준 시각 오차, BD 하단에 미세 굽음.',
 'fig_c21': '두 곡선의 점 연결, AD/BC 수직, AB 수평 확인. 세로 높이는 개략도 압축; D가 k/8보다 높고 C가 8k보다 낮음.',
 'fig_m27': '반주기·음영·라벨 확인. 교점은 약 1/6 및 5/6, y=1 높이는 최대 높이의 약 0.53로 근사.',
 'fig_m29': '선분·라벨·두 음영 확인. 반원 세로/가로 비율 및 P,H 위치 오차: H는 AB의 약 75%(사양 약 82%), 각도 약 27도(사양 25도). 두 음영 대비가 약함.',
 'fig_g26': '두 가지·초점·연결선·라벨 확인. P 좌표는 사양 대비 근사: 초점 간격 기준 x 약 3.7(사양 4.2), y 위치도 수치 불일치. 정확한 좌표 도해로는 미통과.',
 'fig_g28': '평면·정사각형 투시·PBD 음영·PA와 AB 직각 표시·라벨 확인. 투시 길이는 개략도.',
}
lines = ['2회 그림 생성 및 검수 기록', '상태: 8개 PNG 저장. 전체 사양 충족 완료 아님; 특히 fig_c10, fig_g26은 검수 미통과.', '모든 원본은 image gen으로 생성. Pillow는 자르기·크기·RGB·DPI 포장에만 사용.', '공통 잔여 오차: 글꼴 10pt/선 굵기 0.5~0.6pt 및 균일 회색은 생성 결과에서 정확히 보장되지 않음.']
for ident, mm, *_ in manifest['jobs']:
    source = Path(manifest['selected_sources'][ident])
    original = raw / (ident + '.png')
    shutil.copy2(source, original)
    im = Image.open(original).convert('RGB')
    bbox = im.convert('L').point(lambda p: 255 if p < 200 else 0).getbbox()
    if bbox:
        im = im.crop(bbox)
    width = round(mm * 600 / 25.4)
    margin = round(600 / 25.4)
    inside = width - 2 * margin
    height = round(im.height * inside / im.width)
    im = im.resize((inside, height), Image.Resampling.LANCZOS)
    canvas = Image.new('RGB', (width, height + 2 * margin), 'white')
    canvas.paste(im, (margin, margin))
    target = ROOT / (ident + '.png')
    canvas.save(target, dpi=(600, 600))
    check = Image.open(target)
    assert check.mode == 'RGB' and check.width == width
    assert all(abs(d - 600) < .01 for d in check.info['dpi'])
    size = f'{check.width * 25.4 / 600:.2f} × {check.height * 25.4 / 600:.2f} mm ({check.width} × {check.height} px), 600dpi, 흰 배경'
    lines.append(f'{ident}.png: {size}; {notes[ident]}')
    print(ident, check.size, check.info['dpi'])
(ROOT / 'DONE.txt').write_text('\n'.join(lines) + '\n', encoding='utf-8')
