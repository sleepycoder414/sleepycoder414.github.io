const dialog=document.querySelector('dialog');
document.querySelectorAll('[data-enlarge]').forEach(b=>b.addEventListener('click',()=>{dialog.querySelector('img').src=b.dataset.enlarge;dialog.querySelector('img').alt=b.dataset.caption||'';dialog.showModal()}));
dialog?.querySelector('button').addEventListener('click',()=>dialog.close());
dialog?.addEventListener('click',ev=>{if(ev.target===dialog)dialog.close()});
let active=0,original=false;
const dataEl=document.querySelector('#view-data');
if(dataEl){const views=JSON.parse(dataEl.textContent),area=document.querySelector('.viewer'),label=document.querySelector('#view-label'),toggle=document.querySelector('.toggle'),zoom=document.querySelector('.zoom');
function paint(){const v=views[active],src=original?v.original:v.image;area.replaceChildren();if(src){const im=document.createElement('img');im.src=src;im.alt=(original?'Empty reference: ':'Style concept: ')+v.label;area.append(im)}else{const d=document.createElement('div');d.className='empty';d.textContent='This condo view is awaiting generation.';area.append(d)}label.textContent=(original?'Empty condo reference · ':'Furnished concept · ')+v.label;toggle.textContent=original?'Show styled view':'Show empty reference';toggle.setAttribute('aria-pressed',String(original));zoom.disabled=!src;document.querySelectorAll('[data-view]').forEach((b,i)=>b.setAttribute('aria-pressed',String(i===active)))}
document.querySelectorAll('[data-view]').forEach(b=>b.addEventListener('click',()=>{active=Number(b.dataset.view);paint()}));toggle.addEventListener('click',()=>{original=!original;paint()});zoom.addEventListener('click',()=>{const v=views[active];dialog.querySelector('img').src=original?v.original:v.image;dialog.querySelector('img').alt=v.label;dialog.showModal()});paint()}
const preferenceKeys={favorites:'condo-style-favorites',excluded:'condo-style-not-for-me'};
function readPreference(key){try{const values=JSON.parse(localStorage.getItem(key)||'[]');return new Set(Array.isArray(values)?values.filter(v=>typeof v==='string'):[])}catch{return new Set()}}
let saved=readPreference(preferenceKeys.favorites),excluded=readPreference(preferenceKeys.excluded);
function persistPreferences(){try{localStorage.setItem(preferenceKeys.favorites,JSON.stringify([...saved]));localStorage.setItem(preferenceKeys.excluded,JSON.stringify([...excluded]))}catch{}}
const search=document.querySelector('#search'),cards=[...document.querySelectorAll('.card')];
let only=false,collection=new URLSearchParams(location.search).get('collection')||'all';
if(!['all','favorites','jazz'].includes(collection))collection='all';
function paintPreferences(){
 document.querySelectorAll('.favorite').forEach(b=>{const on=saved.has(b.dataset.id)&&!excluded.has(b.dataset.id);b.setAttribute('aria-pressed',String(on));b.textContent=on?'Saved to shortlist':'Save to shortlist'});
 document.querySelectorAll('.not-for-me').forEach(b=>{const on=excluded.has(b.dataset.id);b.setAttribute('aria-pressed',String(on));b.textContent=on?'Restore to main list':'Not for me'});
 if(!search)return;
 const main=document.querySelector('#main-styles'),dismissed=document.querySelector('#excluded-styles'),q=search.value.toLowerCase().trim();
 let count=0,excludedCount=0;
 cards.forEach(c=>{
  const rejected=excluded.has(c.dataset.id),target=rejected?dismissed:main;
  if(c.parentElement!==target)target.append(c);
  const match=c.dataset.search.includes(q)&&(collection==='all'||c.dataset.collection===collection);
  const show=match&&(rejected||!only||saved.has(c.dataset.id));c.hidden=!show;
  if(show){if(rejected)excludedCount++;else count++}
 });
 // Restore the original collection order after moving cards between sections.
 [main,dismissed].forEach(container=>[...container.children].sort((a,b)=>Number(a.dataset.id)-Number(b.dataset.id)).forEach(c=>container.append(c)));
 document.querySelector('#result-count').textContent=count+(count===1?' style':' styles')+' shown in the main list';
 document.querySelector('#excluded-count').textContent=excludedCount+(excludedCount===1?' style':' styles')+' shown · '+excluded.size+' set aside';
 const empty=document.querySelector('#excluded-empty');empty.hidden=excludedCount>0;
 empty.textContent=excluded.size?'No excluded styles match this search or collection.':'Styles you mark “Not for me” will appear here. You can restore them whenever you like.';
}
document.querySelectorAll('.favorite,.not-for-me').forEach(b=>b.addEventListener('click',()=>{
 const id=b.dataset.id;
 if(b.classList.contains('favorite')){if(saved.has(id)&&!excluded.has(id))saved.delete(id);else{saved.add(id);excluded.delete(id)}}
 else if(excluded.has(id))excluded.delete(id);else{excluded.add(id);saved.delete(id)}
 persistPreferences();paintPreferences();
 const message=document.querySelector('#preference-feedback');if(message)message.textContent=b.classList.contains('favorite')?(saved.has(id)?'Style saved to your shortlist.':'Style removed from your shortlist.'):(excluded.has(id)?'Style moved to Not for me.':'Style restored to the main list.');
}));
if(search){
 document.querySelectorAll('[data-filter]').forEach(b=>{b.addEventListener('click',()=>{collection=b.dataset.filter;document.querySelectorAll('[data-filter]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));paintPreferences()});b.setAttribute('aria-pressed',String(b.dataset.filter===collection))});
 search.addEventListener('input',paintPreferences);
 document.querySelector('#shortlist').addEventListener('click',ev=>{only=!only;ev.currentTarget.textContent=only?'Show all styles':'Show my shortlist';ev.currentTarget.setAttribute('aria-pressed',String(only));paintPreferences()});
}
function refreshPreferences(){saved=readPreference(preferenceKeys.favorites);excluded=readPreference(preferenceKeys.excluded);paintPreferences()}
window.addEventListener('storage',refreshPreferences);window.addEventListener('pageshow',refreshPreferences);
paintPreferences();
