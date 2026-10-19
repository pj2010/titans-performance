#!/usr/bin/env python3
"""Embeds site assets, normalized game data, and downloadable sources into one HTML."""
import re,json
from pathlib import Path
root=Path(__file__).resolve().parent.parent
html=(root/'index.html').read_text()
styles='\n'.join((root/'styles'/name).read_text() for name in ['base.css','layout.css','print.css'])
# Print CSS in bundled build must remain print-only.
styles=styles.replace('/*PRINT_ONLY_BEGIN*/','')
base='\n'.join((root/'styles'/name).read_text() for name in ['base.css','layout.css'])
pr=(root/'styles/print.css').read_text()
html=re.sub(r'<link rel="stylesheet" href="styles/base.css">\s*<link rel="stylesheet" href="styles/layout.css">\s*<link rel="stylesheet" href="styles/print.css" media="print">',f'<style>\n{base}\n</style>\n<style media="print">\n{pr}\n</style>',html)
data=(root/'scripts/data.js').read_text().replace('export const ','const ')
calc=(root/'scripts/calculations.mjs').read_text().replace('export const ','const ').replace('export function ','function ')
app=(root/'scripts/app.js').read_text()
app=re.sub(r'^import .*?;\s*','',app,flags=re.M)
# In standalone edition, download CSV and audit JSON without file dependencies.
extra='''\nfor(const [path,name,content,mime] of [
['data/games.csv','titans_games.csv',null,'text/csv'],
['data/games.json','titans_games.json',JSON.stringify(GAMES,null,2),'application/json'],
['data/validation.json','titans_validation.json',JSON.stringify(AUDIT,null,2),'application/json']]){
 const a=document.querySelector('a[href="'+path+'"]');if(!a)continue;
 a.href='#';a.setAttribute('download',name);
 a.addEventListener('click',event=>{
 event.preventDefault();let data=content;
 if(data===null){const fields=Object.keys(GAMES[0]);const csvEsc=t=>'"'+String(t??'').replace(/"/g,'""')+'"';data=[fields.map(csvEsc).join(','),...GAMES.map(g=>fields.map(k=>csvEsc(g[k])).join(','))].join('\\n')}
 const blob=new Blob([data],{type:mime+';charset=utf-8'});const url=URL.createObjectURL(blob);const link=document.createElement('a');link.href=url;link.download=name;document.body.append(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(url),10000);
 });
}'''
js=data+'\n'+calc+'\n'+app+'\n'+extra
html=html.replace('<script type="module" src="scripts/app.js"></script>','<script>\n'+js.replace('</script','<\\/script')+'\n</script>')
(root.parent/'titans_performance_standalone.html').write_text(html,encoding='utf-8')
print(root.parent/'titans_performance_standalone.html',len(html.encode()))
