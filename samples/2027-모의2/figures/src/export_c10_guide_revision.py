"""Package final image-gen output without drawing edits."""
from pathlib import Path
import json
import shutil
from PIL import Image

root=Path(__file__).resolve().parent.parent
revision=json.loads((root/'src/c10_guide_revision.json').read_text(encoding='utf-8'))
target=root/'fig_c10.png'
shutil.copy2(target,root/'src/raw/fig_c10_before_guide_revision.png')
raw=root/'src/raw/fig_c10_imagegen_from_guide.png'
shutil.copy2(revision['source'],raw)
im=Image.open(raw).convert('RGB')
bbox=im.convert('L').point(lambda p:255 if p<200 else 0).getbbox()
im=im.crop(bbox)
width=round(65*600/25.4)
margin=round(600/25.4)
inner=width-2*margin
height=round(im.height*inner/im.width)
im=im.resize((inner,height),Image.Resampling.LANCZOS)
canvas=Image.new('RGB',(width,height+2*margin),'white')
canvas.paste(im,(margin,margin))
canvas.save(target,dpi=(600,600))
check=Image.open(target)
assert check.mode=='RGB' and check.width==1535
assert all(abs(v-600)<.01 for v in check.info['dpi'])
manifest_path=root/'src/prompts.json'
manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
manifest.setdefault('revisions',[]).append({'date':'2026-10-10','fig_c10_guide_revision':revision})
manifest['selected_sources']['fig_c10']=revision['source']
manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (root/'DONE.txt').open('a',encoding='utf-8') as f:
    f.write(f'2026-10-10 fig_c10 가이드 참조 재수정: {check.width*25.4/600:.2f} × {check.height*25.4/600:.2f} mm ({check.width} × {check.height} px), 600dpi, RGB 흰 배경. 정확 좌표 가이드는 참고용이며 최종본은 image gen 결과. A/B는 y=k, C/D는 y=-k 위 곡선 교점; AB/BD/DC/CA 연결 및 곡선의 0·4·8 절편, 2·6 극점 확인. 원본 점 중심 x≈259,570,873,1183; 간격≈311,303,310px(평균 대비 최대 약1.6% 오차). 이전 C/B 중첩 및 D 곡선 이탈 문제 해결. 잔여: 미세 간격·곡선 근사, 회색 농도와 인쇄 선 굵기의 생성 오차.\n')
print(check.size,check.info['dpi'])
