"""Build a local review gallery from files actually present; no image generation."""
from pathlib import Path
import json, html
root=Path(__file__).resolve().parent
styles=json.loads((root/'styles.json').read_text(encoding='utf-8-sig'))
jobs=[j for j in json.loads((root/'jobs.json').read_text(encoding='utf-8-sig')) if not j['file'].startswith('condo_')]+json.loads((root/'rework_jobs.json').read_text(encoding='utf-8-sig'))
cards=[]
total=0
for s in styles:
    folder=root/s['folder']
    expected=[j for j in jobs if j['folder']==s['folder']]
    present=[j for j in expected if (folder/j['file']).is_file()]
    total+=len(present)
    figs=[]
    for j in present:
        revisions=sorted(folder.glob(Path(j['file']).stem+'_v*.png'),key=lambda p:int(p.stem.rsplit('_v',1)[1]))
        selected=revisions[-1].name if revisions else j['file']
        link=s['folder']+'/'+selected
        figs.append(f'<figure><a href="{link}"><img loading="lazy" src="{link}" alt="{html.escape(j["file"])}"></a><figcaption>{html.escape(j["file"])}</figcaption></figure>')
    review=json.loads((folder/'review.json').read_text()) if (folder/'review.json').exists() else {}
    issues=review.get('pending_corrections',[])
    review_note=('<p><b>Review: corrections pending.</b> '+html.escape(' '.join(x['required_change'] for x in issues))+'</p>') if issues else '<p>Concept review passed; minor AI placement variations remain.</p>'
    swatches=''.join(f'<span style="background:{c}">{c}</span>' for c in s['colors'])
    cards.append(f'<section id="s{s["id"]}"><h2>{s["id"]}. {html.escape(s["name"])}</h2>{review_note}<p>{html.escape(s["definition"])}</p><p><b>Condo fit: {s["fit"]}.</b> {html.escape(s["implement"])}</p><div class="palette">{swatches}</div><p><a href="{s["folder"]}/GUIDE.md">Style guide</a> · <a href="{s["folder"]}/prompt.json">Prompts and provenance</a> · {len(present)}/10 images saved</p><div class="grid">'+''.join(figs)+'</div></section>')
nav=''.join(f'<a href="#s{s["id"]}">{s["id"]} {html.escape(s["name"])}</a>' for s in styles)
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Condo style ideation</title><style>body{font:16px/1.6 system-ui;margin:0;background:#f3f0e8;color:#28352e}header,main{max-width:1440px;margin:auto;padding:32px}h1{font:48px Georgia}h2{font:32px Georgia}nav{display:flex;flex-wrap:wrap;gap:8px}nav a{padding:5px 12px;background:white;border-radius:20px}a{color:#345746}section{padding:30px 0;border-top:1px solid #ccc}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:18px}figure{margin:0;background:white;padding:10px;border-radius:8px}img{width:100%;height:280px;object-fit:contain}figcaption{font-size:12px;overflow-wrap:anywhere}.palette{display:flex;gap:8px}.palette span{padding:20px 10px;color:white;text-shadow:0 1px 4px black;flex:1}p{max-width:900px}</style><header><h1>20 ways to feel at home</h1><p>Interior style ideation for the Burnaby Lake condo. Curated current and enduring styles; this is not a statistical popularity ranking.</p><p>Generated concepts preserve the intended shell but are not dimensionally verified construction renders. Generic examples depict other interiors. Exact digital palette swatches appear below each introduction.</p>'''+f'<p><b>{total}/200 images saved.</b> <a href="README.md">Research and project notes</a> · <a href="REFERENCE_MAP.md">Reference view map</a></p><nav>{nav}</nav></header><main>'+''.join(cards)+'</main></html>'
(root/'index.html').write_text(page,encoding='utf-8')
(root/'gallery-progress.json').write_text(json.dumps({'expected':200,'saved':total,'missing':[j['folder']+'/'+j['file'] for j in jobs if not (root/j['folder']/j['file']).is_file()]},indent=2),encoding='utf-8')
print(f'{total}/200 images saved; gallery rebuilt')

