#!/usr/bin/env python3
"""Build a reproducible Tennessee Titans game-level static dataset.
Run: python scripts/build_data.py --input /mnt/data --output data
Requires pandas. Does not alter the uploaded source files.
"""
import argparse, csv, json, re, math
from pathlib import Path
from datetime import datetime, date
from collections import defaultdict,Counter
import pandas as pd

TEAMS={'ARI':'Cardinals','ATL':'Falcons','BAL':'Ravens','BUF':'Bills','CAR':'Panthers','CHI':'Bears','CIN':'Bengals','CLE':'Browns','DAL':'Cowboys','DEN':'Broncos','DET':'Lions','GB':'Packers','HOU':'Texans','IND':'Colts','JAX':'Jaguars','KC':'Chiefs','LAC':'Chargers','LAR':'Rams','LV':'Raiders','MIA':'Dolphins','MIN':'Vikings','NE':'Patriots','NO':'Saints','NYG':'Giants','NYJ':'Jets','PHI':'Eagles','PIT':'Steelers','SEA':'Seahawks','SF':'49ers','TB':'Buccaneers','TEN':'Titans','WAS':'Commanders'}
FULL_TEAM={'Tennessee Titans':'TEN'}
DIV={'IND','HOU','JAX'}
CUTOFF=date(2026,10,19); PIVOT=date(2022,11,18); START=date(2018,12,18)
FIXES={('2026','WEEK 6','TEN','IND'):(26,20,'https://www.nfl.com/games/titans-at-colts-2026-reg-6')}
def as_date(s,season):
    m=re.match(r'([A-Za-z]+)\s+(\d+)',str(s))
    if not m:return None
    month=datetime.strptime(m.group(1),'%B').month
    year=int(season)+(1 if month<=3 else 0)
    return date(year,month,int(m.group(2)))
def dump(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
def main():
 p=argparse.ArgumentParser();p.add_argument('--input',default='/mnt/data');p.add_argument('--output',default='data');a=p.parse_args()
 input_dir=Path(a.input);output=Path(a.output);output.mkdir(parents=True,exist_ok=True)
 s=pd.read_csv(input_dir/'2010-2026_scores.csv',dtype={'Season':str},low_memory=False)
 rows=[];fixlog=[];bad=[];seen=set();excluded=Counter()
 for r in s.to_dict('records'):
    season=int(r['Season']);wk=str(r['Week']);status=str(r['GameStatus']);away=str(r['AwayTeam']);home=str(r['HomeTeam'])
    if season<2018 or season>2026 or (away!='TEN' and home!='TEN'):continue
    if not re.fullmatch(r'WEEK \d+',wk):excluded['preseason/postseason/bye']+=1;continue
    when=as_date(r['GameDate'],season)
    if not when or when<START or when>CUTOFF:excluded['outside date window']+=1;continue
    key=(season,wk,away,home)
    if key in seen:bad.append(f'duplicate {key}');continue
    seen.add(key)
    source='Uploaded 2010-2026_scores.csv';sourceUrl=None
    av,ho=r['AwayScore'],r['HomeScore']
    fixed=FIXES.get(tuple(map(str,(season,wk,away,home))))
    if fixed:
        av,ho,sourceUrl=fixed;source='NFL.com official game center (supplemental correction)'
        fixlog.append({'game':str(key),'originalStatus':status,'originalAwayScore':None if pd.isna(r['AwayScore']) else int(r['AwayScore']),'originalHomeScore':None if pd.isna(r['HomeScore']) else int(r['HomeScore']),'correctedAwayScore':av,'correctedHomeScore':ho,'url':sourceUrl})
    elif status!='FINAL' or pd.isna(av) or pd.isna(ho):excluded['unplayed/incomplete']+=1;continue
    av=int(av);ho=int(ho);usaway=(away=='TEN');opp=home if usaway else away
    pf=av if usaway else ho;pa=ho if usaway else av
    rid=f'{season}-{int(wk.split()[-1]):02}-{away}-{home}'
    rows.append({'id':rid,'season':season,'week':int(wk.split()[-1]),'date':when.isoformat(),'opponent':opp,'opponentName':TEAMS.get(opp,opp),'location':'Away' if usaway else 'Home','homeTeam':home,'awayTeam':away,'pointsFor':pf,'pointsAgainst':pa,'margin':pf-pa,'result':'W' if pf>pa else ('L' if pf<pa else 'T'),'division':opp in DIV,'oneScore':abs(pf-pa)<=8,'period':'before' if when<PIVOT else 'after','scoreSource':source,'scoreSourceUrl':sourceUrl,'playDataAvailable':False,'taggedPasses':None,'taggedRuns':None,'taggedSacksAllowed':None,'taggedSacksMade':None,'taggedPlayCoverage':'Missing'})
 rows.sort(key=lambda d:(d['date'],d['id']))
 idx={r['id']:r for r in rows};pbpstats=defaultdict(Counter);season_read={}; unmapped=[]
 for season in range(2018,2027):
    f=input_dir/f'{season}_plays.csv'
    if not f.exists():continue
    use=['Season','Week','AwayTeam','HomeTeam','TeamWithPossession','PlayOutcome','PlayDescription']
    d=pd.read_csv(f,usecols=use,low_memory=False)
    season_read[str(season)]={'inputRows':len(d),'tennesseeRows':0,'matchedGameCount':0}
    d=d[((d.AwayTeam=='TEN')|(d.HomeTeam=='TEN')) & (d.Week.astype(str).str.fullmatch('WEEK \\d+'))]
    season_read[str(season)]['tennesseeRows']=len(d)
    for (wk,away,home),group in d.groupby(['Week','AwayTeam','HomeTeam'],sort=False):
      rid=f'{season}-{int(wk.split()[-1]):02}-{away}-{home}'
      if rid not in idx:continue
      season_read[str(season)]['matchedGameCount']+=1
      g=idx[rid];g['playDataAvailable']=True;g['taggedPlayCoverage']='Play file present; outcome tags only'
      own=group.TeamWithPossession.eq('Tennessee Titans')
      out=group.PlayOutcome.fillna('').astype(str)
      g['taggedRuns']=int((own & out.str.match(r'^-?\d+ Yard Run$')).sum())
      g['taggedPasses']=int((own & (out.str.match(r'^-?\d+ Yard Pass$')|out.eq('Pass Incomplete')|out.eq('Interception'))).sum())
      g['taggedSacksAllowed']=int((own & (out.str.contains(r'Yard Sack')|out.eq('Sack'))).sum())
      g['taggedSacksMade']=int((~own & (out.str.contains(r'Yard Sack')|out.eq('Sack'))).sum())
      # Derived figures are explicitly outcome-tag counts, not official NFL box-score totals.
    del d
 # postseason separate via scores
 playoffs=[]
 for r in s.to_dict('records'):
    season=int(r['Season']);wk=str(r['Week']);
    if season<2018 or season>2026 or not any(x in wk for x in ('WILD CARD','DIVISIONAL PLAYOFF','CONFERENCE CHAMPIONSHIP','SUPER BOWL')):continue
    away=str(r['AwayTeam']);home=str(r['HomeTeam'])
    if away!='TEN' and home!='TEN':continue
    if str(r['GameStatus'])!='FINAL' or pd.isna(r['AwayScore']) or pd.isna(r['HomeScore']):continue
    av=int(r['AwayScore']);ho=int(r['HomeScore']);pf=av if away=='TEN' else ho;pa=ho if away=='TEN' else av
    playoffs.append({'season':season,'round':wk,'result':'W' if pf>pa else 'L','pf':pf,'pa':pa})
 # 2020 and 2021 division championships: fixed season-level reference from official results, documented in methodology
 title_seasons=[2020,2021]
 report={'asOf':CUTOFF.isoformat(),'pivot':PIVOT.isoformat(),'start':START.isoformat(),'gameCount':len(rows),'playFiles':season_read,'excludedRows':dict(excluded),'scoreCorrections':fixlog,'issues':bad,'playoffGames':playoffs,'divisionTitleSeasons':title_seasons,'notes':['Scores supplied by user; Week 6 2026 score supplemented from NFL.com official game center.','2026 Week 6 play-level data is not included in the uploaded 2026_plays.csv.','Play outcome tag counts are exploratory; do not treat as official team play totals.','Playoff appearances based on supplied postseason game rows.','Division title metadata (2020, 2021) maintained separately from game outcomes.']}
 dump(output/'games.json',rows);dump(output/'validation.json',report)
 with (output/'games.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 # derive comparison for audit independent of site JS
 def agg(records):
    n=len(records);w=sum(g['result']=='W' for g in records);l=sum(g['result']=='L' for g in records);t=n-w-l
    return {'games':n,'wins':w,'losses':l,'ties':t,'pct':round((w+t/2)/n*100,2) if n else None,'pointsFor':sum(g['pointsFor'] for g in records),'pointsAgainst':sum(g['pointsAgainst'] for g in records)}
 report['summary']={p:agg([r for r in rows if r['period']==p]) for p in ('before','after')}
 dump(output/'validation.json',report)
 module=output.parent/'scripts'/'data.js'
 if module.parent.is_dir():
    module.write_text('export const GAMES='+json.dumps(rows,ensure_ascii=False,separators=(',',':'))+';\nexport const AUDIT='+json.dumps(report,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
 print(json.dumps({'summary':report['summary'],'playFiles':season_read,'corrections':fixlog,'issues':bad,'playoffs':playoffs},indent=2))
if __name__=='__main__':main()
