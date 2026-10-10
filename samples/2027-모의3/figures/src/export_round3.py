"""Package image_gen outputs only; does not draw/alter mathematical content."""
import json
import shutil
from pathlib import Path
from PIL import Image

root=Path(__file__).resolve().parent.parent
manifest=json.loads((root/'src/prompts.json').read_text(encoding='utf-8'))
lines=['수능 수학 모의 문제지 3회 — 8개 그림 생성·검수 기록',
       '최종본은 모두 정확 좌표 가이드를 참조한 image gen 결과. 가이드만 matplotlib 사용. Pillow는 자르기·리사이즈·RGB·DPI 포장에만 사용.',
       '공통: 위치·간격·라벨·음영·선분 연결 직접 시각 대조. 생성 결과의 미세 좌표/곡선 근사 오차와 회색 농도 변화 잔존. 글꼴 약10pt·선굵기0.5~0.6pt·점지름1.2mm의 정확한 물리치 보장 불가.']
for job in manifest['jobs']:
    ident=job['id']
    raw=root/'src/raw'/f'{ident}_imagegen_round3.png'
    shutil.copy2(job['source'],raw)
    im=Image.open(raw).convert('RGB')
    bbox=im.convert('L').point(lambda p:255 if p<200 else 0).getbbox()
    if bbox:im=im.crop(bbox)
    width=round(job['width']*600/25.4)
    margin=round(600/25.4)
    inner=width-2*margin
    height=round(im.height*inner/im.width)
    im=im.resize((inner,height),Image.Resampling.LANCZOS)
    final=Image.new('RGB',(width,height+2*margin),'white')
    final.paste(im,(margin,margin))
    target=root/f'{ident}.png'
    final.save(target,dpi=(600,600))
    check=Image.open(target)
    assert check.mode=='RGB' and check.width==width
    assert all(abs(d-600)<.01 for d in check.info['dpi'])
    lines.append(f'{ident}.png: {width*25.4/600:.2f} × {check.height*25.4/600:.2f} mm ({width} × {check.height} px), 600dpi, RGB 흰 배경, 여백 약1mm; {job["inspection"]}')
    print(ident,check.size,check.info['dpi'])
(root/'DONE.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
