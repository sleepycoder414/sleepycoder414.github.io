from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote,urlsplit
import json
r=Path(__file__).resolve().parent
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):
  for k,v in attrs:
   if k in ('href','src','data-enlarge') and v:self.links.append(v)
errors=[];n=0
for p in [r/'index.html',*r.glob('style_*/index.html')]:
 parser=Links();txt=p.read_text(encoding='utf-8');parser.feed(txt)
 for link in parser.links:
  u=urlsplit(link)
  if u.scheme or not u.path:continue
  n+=1
  if not (p.parent/unquote(u.path)).exists():errors.append(str(p.relative_to(r))+': '+link)
 if p.parent!=r:
  import re
  views=json.loads(re.search(r'<script id="view-data" type="application/json">(.*?)</script>',txt).group(1))
  for v in views:
   for k in ('image','original'):
    if v[k] and not (p.parent/v[k]).exists():errors.append(str(p)+': '+str(v[k]))
status=json.loads((r/'collection-status.json').read_text())
report={'html_pages':1+len(list(r.glob('style_*/index.html'))),'local_links_checked':n,'saved':status['saved'],'expected':status['expected'],'reviewed_styles':sum(s['state']=='reviewed' for s in status['styles']),'errors':errors}
(r/'review/integrity.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))
if errors:raise SystemExit(1)
