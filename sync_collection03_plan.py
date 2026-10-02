from pathlib import Path
import json
r=Path(__file__).resolve().parent
jobs=json.loads((r/'collection03_jobs_full.json').read_text())
for s in json.loads((r/'styles_collection03.json').read_text()):
 p=r/s['folder']/'prompt.json';v=json.loads(p.read_text());v['planned_jobs']=[j for j in jobs if j['folder']==s['folder']];p.write_text(json.dumps(v,indent=2)+'\n')
