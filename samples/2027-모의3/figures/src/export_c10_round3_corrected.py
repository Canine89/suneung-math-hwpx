from pathlib import Path
import json, shutil
from PIL import Image
root=Path(__file__).resolve().parent.parent
revision=json.loads((root/'src/c10_round3_corrected.json').read_text(encoding='utf-8'))
target=root/'fig_c10.png'
shutil.copy2(target,root/'src/raw/fig_c10_round3_before_m_correction.png')
raw=root/'src/raw/fig_c10_round3_corrected_imagegen.png'
shutil.copy2(revision['source'],raw)
im=Image.open(raw).convert('RGB')
bbox=im.convert('L').point(lambda p:255 if p<200 else 0).getbbox()
im=im.crop(bbox)
width=round(55*600/25.4);margin=round(600/25.4);inner=width-2*margin
height=round(im.height*inner/im.width)
im=im.resize((inner,height),Image.Resampling.LANCZOS)
canvas=Image.new('RGB',(width,height+2*margin),'white');canvas.paste(im,(margin,margin));canvas.save(target,dpi=(600,600))
check=Image.open(target)
assert check.mode=='RGB' and check.width==1299 and all(abs(d-600)<.01 for d in check.info['dpi'])
path=root/'src/prompts.json';manifest=json.loads(path.read_text(encoding='utf-8'))
job=next(j for j in manifest['jobs'] if j['id']=='fig_c10')
job.setdefault('revisions',[]).append(revision)
job['source']=revision['source'];job['guide']=revision['guide']
job['inspection']='修正 m=4−∛32≈0.825198, 교점(3.174802,2.619840). 가이드와 기울기·교점·음영·라벨 대조 완료. 약한 음영 농도 변화 잔존.'
path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (root/'DONE.txt').open('a',encoding='utf-8') as f:
    f.write(f'2026-10-10 fig_c10 수치 수정: m=4−∛32≈0.825198, 교점(3.174802,2.619840), 직선 x≈3.8까지 연장. 정확 좌표 가이드 참조 image gen 결과로 덮어씀. {width*25.4/600:.2f} × {check.height*25.4/600:.2f} mm ({width} × {check.height}px), 600dpi, RGB 흰 배경. 원본 기준 O≈(150,942), 4≈(1109,942), 꼭짓점≈(630,248), 교점≈(912,487): 좌표 환산≈(3.18,2.62), 수정 사양과 근접. 두 음영 영역·식 라벨 확인. 잔여: 미세 곡선/좌표 근사, 약한 음영 농도 변화. 다른 7개 최종 그림 수정 없음.\n')
print(check.size,check.info['dpi'])
