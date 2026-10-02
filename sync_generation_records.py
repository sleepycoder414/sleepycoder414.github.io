from pathlib import Path
import json
r=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
jobs=read(r/'next20_jobs_revised.json')
for s in read(r/'styles_next20.json'):
 p=r/s['folder']/'prompt.json'
 spec=read(p)
 spec['planned_jobs']=[j for j in jobs if j['folder']==s['folder']]
 p.write_text(json.dumps(spec,indent=2))
records=[]
for p in sorted(r.glob('style_*/*_v*.png.generation.json')):
 if int(p.parent.name.split('_')[1])<=20:continue
 records.append({'folder':p.parent.name,'file':p.name.removesuffix('.generation.json'),'generation_record':str(p.relative_to(r)).replace('\\','/')})
(r/'next20_corrections.json').write_text(json.dumps({'state':'completed','pending':[],'revisions':records,'note':'Highest numeric revision is selected by build_style_pages.py. Earlier attempts remain for provenance; see per-style review.json for accepted results.'},indent=2))
print(str(len(records))+' correction revisions indexed')
