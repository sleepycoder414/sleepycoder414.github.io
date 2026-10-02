from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parent
styles=json.loads((root/'styles.json').read_text(encoding='utf-8-sig'))
jobs=json.loads((root/'rework_jobs.json').read_text(encoding='utf-8-sig'))
historical=json.loads((root/'jobs.json').read_text(encoding='utf-8-sig'))
corrections=json.loads((root/'corrections.json').read_text(encoding='utf-8-sig'))
first=json.loads((root/'resume_first.json').read_text()) if (root/'resume_first.json').exists() else None
for s in styles:
 d=root/s['folder']
 spec=json.loads((d/'prompt.json').read_text(encoding='utf-8-sig'))
 records=[json.loads(p.read_text()) for p in d.glob('*.generation.json')]
 if first and first['folder']==s['folder']:records.append(first)
 spec['tool']='built-in image_gen'
 spec['input_roles']=['Empty condo camera/architecture target','Generic style furnishing reference','Generic dining reference','Furnished living-wide consistency reference when applicable']
 spec['generation_records']=records
 spec['historical_corrections']=[x for x in corrections if x['folder']==s['folder']]
 spec['base_image_prompts']=[x for x in historical if x['folder']==s['folder'] and not x['file'].startswith('condo_')]
 spec['provenance_note']='Original base assets retained; missing interrupted-run base slots completed. Base prompts are the original specifications. Rework jobs hold initial condo prompts; generation_records hold exact resumed calls and corrections. Earlier calls may include supplemental constraints recorded in the conversation.'
 spec['selected_outputs']={}
 for j in jobs:
  if j['folder']!=s['folder']:continue
  vs=sorted(d.glob(Path(j['file']).stem+'_v*.png'),key=lambda p:int(p.stem.rsplit('_v',1)[1]))
  p=vs[-1] if vs else d/j['file']
  if p.exists():spec['selected_outputs'][j['ref']]={'file':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 for name in ['prompt.json','prompts.json']:(d/name).write_text(json.dumps(spec,indent=2),encoding='utf-8')
print('Prompt manifests consolidated')

