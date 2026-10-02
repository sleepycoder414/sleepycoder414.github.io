from pathlib import Path
import json, hashlib
root=Path(__file__).resolve().parent
styles=json.loads((root/'styles.json').read_text(encoding='utf-8-sig'))
jobs=json.loads((root/'rework_jobs.json').read_text(encoding='utf-8-sig'))
base=['01_moodboard.png','02_palette.png','03_example_living.png','04_example_bedroom.png','05_example_dining.png']
report=[]
for s in styles:
 folder=root/s['folder']
 expected=[j['file'] for j in jobs if j['folder']==s['folder']]
 saved=[f for f in expected if (folder/f).is_file()]
 reviewfile=folder/'review.json'
 review=json.loads(reviewfile.read_text()) if reviewfile.exists() else {}
 status={'revision':'empty-shell-v2','style':s['name'],'expected_condo_edits':5,'saved_condo_edits':saved,'missing_condo_edits':[f for f in expected if f not in saved],'base_assets_present':[f for f in base if (folder/f).exists()],'review':review,'state':'reviewed' if len(saved)==5 and review.get('approved') else 'generated_pending_review' if len(saved)==5 else 'in_progress'}
 (folder/'status.json').write_text(json.dumps(status,indent=2),encoding='utf-8')
 report.append(status)
(root/'progress.json').write_text(json.dumps({'revision':'empty-shell-v2','expected_condo_edits':100,'saved_condo_edits':sum(len(s['saved_condo_edits']) for s in report),'styles':report},indent=2),encoding='utf-8')
print('Condo edits:',sum(len(s['saved_condo_edits']) for s in report),'/100')
