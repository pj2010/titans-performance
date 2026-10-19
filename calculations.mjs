/** Pure calculations shared by the browser and Node's validation tests. */
export const PIVOT = '2022-11-18';
export const END = '2026-10-19';
export const CALENDAR_START = '2018-12-18';
export function splitGames(games,mode='calendar') {
  const sorted=[...games].sort((a,b)=>a.date.localeCompare(b.date)||a.id.localeCompare(b.id));
  let before=sorted.filter(g=>g.date>=CALENDAR_START && g.date<PIVOT);
  let after=sorted.filter(g=>g.date>=PIVOT && g.date<=END);
  if(mode==='games') {const count=Math.min(before.length,after.length);before=before.slice(-count);after=after.slice(0,count)}
  return {before,after};
}
export const rate=(wins,losses,ties=0)=>{const n=wins+losses+ties;return n?(wins+ties/2)/n*100:null};
export const round=(n,d=1)=>Number(n.toFixed(d));
export function runs(games) {
  const out=[];let curr=null;
  for(const g of games){if(!curr||curr.result!==g.result){curr={result:g.result,count:0,first:g,last:g,games:[]};out.push(curr)}curr.count++;curr.last=g;curr.games.push(g)}
  return out;
}
export function summarize(games){
 const n=games.length;const wins=games.filter(g=>g.result==='W').length,losses=games.filter(g=>g.result==='L').length,ties=n-wins-losses;
 const pf=games.reduce((s,g)=>s+g.pointsFor,0),pa=games.reduce((s,g)=>s+g.pointsAgainst,0);
 const division=games.filter(g=>g.division),close=games.filter(g=>g.oneScore),home=games.filter(g=>g.location==='Home'),away=games.filter(g=>g.location==='Away');
 const rec=a=>{const w=a.filter(g=>g.result==='W').length,l=a.filter(g=>g.result==='L').length;return {wins:w,losses:l,ties:a.length-w-l,total:a.length,pct:rate(w,l,a.length-w-l)}};
 const streaks=runs(games);const losing=streaks.filter(s=>s.result==='L');const winning=streaks.filter(s=>s.result==='W');
 const plays=games.filter(g=>g.playDataAvailable);
 return {games:n,wins,losses,ties,pct:rate(wins,losses,ties),per17:n?(wins+ties/2)*17/n:null,pf,pa,pointsFor:n?pf/n:null,pointsAgainst:n?pa/n:null,margin:n?(pf-pa)/n:null,division:rec(division),close:rec(close),home:rec(home),away:rec(away),blowouts:games.filter(g=>g.result==='L'&&g.margin<=-9).length,scored20:games.filter(g=>g.pointsFor>=20).length,streakLoss:Math.max(0,...losing.map(s=>s.count)),streakWin:Math.max(0,...winning.map(s=>s.count)),streaks,playCoverage:plays.length,taggedRuns:plays.reduce((s,g)=>s+(g.taggedRuns||0),0),taggedPasses:plays.reduce((s,g)=>s+(g.taggedPasses||0),0),taggedSacksAllowed:plays.reduce((s,g)=>s+(g.taggedSacksAllowed||0),0),taggedSacksMade:plays.reduce((s,g)=>s+(g.taggedSacksMade||0),0)};
}
export function seasonsFor(a,b){const all=[...a,...b], map=new Map();for(const g of all){const key=g.season+'-'+g.period;if(!map.has(key))map.set(key,{key,season:g.season,period:g.period,games:[]});map.get(key).games.push(g)}return [...map.values()].sort((a,b)=>a.games[0].date.localeCompare(b.games[0].date));}
export function comparisonRows(left,right){return [
 {label:'Wins per 17 games',key:'per17',unit:'',values:[left.per17,right.per17],desc:'Wins normalized to 17 regular-season games; not actual season records.'},
 {label:'Points scored / game',key:'pointsFor',unit:'',values:[left.pointsFor,right.pointsFor],desc:'Titans final points divided by games in the selected sample.'},
 {label:'Points allowed / game',key:'pointsAgainst',unit:'',values:[left.pointsAgainst,right.pointsAgainst],desc:'Opponent final points divided by games in the selected sample.'},
 {label:'Scoring margin / game',key:'margin',unit:'',values:[left.margin,right.margin],desc:'(Points scored − points allowed) / games.'},
 {label:'AFC South win rate',key:'division',unit:'%',values:[left.division.pct,right.division.pct],desc:'Regular-season games versus Houston, Indianapolis, and Jacksonville.'},
 {label:'One-score win rate',key:'close',unit:'%',values:[left.close.pct,right.close.pct],desc:'Games decided by eight points or fewer.'},
 {label:'Longest losing streak',key:'streakLoss',unit:' games',values:[left.streakLoss,right.streakLoss],desc:'Maximum consecutive defeats within each comparison sample.'},
 {label:'Losses by 9+ points',key:'blowouts',unit:' games',values:[left.blowouts,right.blowouts],desc:'Count of losses by at least nine points; sample lengths differ in calendar mode.'}
]}
export function chartPoints(games){let wins=0;return games.map((g,i)=>{if(g.result==='W')wins++;return {game:g,x:i+1,y:wins,pct:wins/(i+1)*100}})}
