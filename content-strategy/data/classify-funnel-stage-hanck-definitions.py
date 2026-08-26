import json,re
def v2n(s):
    s=(s or '').replace(' views','').replace(',','').strip()
    m=re.match(r'^([\d.]+)([KM]?)$',s)
    return int(float(m.group(1))*{'':1,'K':1e3,'M':1e6}[m.group(2)]) if m else 0

# --- Hanck's own definitions, from the training ---
# BOF: "way more niche, way more advanced ... back testing, some spreadsheet stuff,
#       super niche down, beginners wouldn't even understand it ... and it could also
#       be testimonials on YouTube"
BOF = re.compile(r"""
 (backtest|back[- ]test|backtested)
|(spreadsheet|data\s+(behind|shows)|i\s+analys|statistic|sample\s+size|\d{2,3}(\.\d+)?\s*%)
|(student|students|testimonial|client\s+interview|he\s+went\s+from|went\s+from\s+unprofitable)
|(flew\s+\d+\s+students|trade\s+live\s+with)
""", re.I|re.X)

# MOF: "more niche down, a little bit more advanced, nurtures people" — the mechanism,
#      the named system, AND the documentary/payout series (Hanck classes it MOF)
MOF = re.compile(r"""
 (\bEp\.?\s*\d|\bEpisode\s*\d|road\s+to\s+\$|every\s+(single\s+)?trade|filmed\s+every|this\s+week|payout\s+breakdown)
|(module\s*\d)
|(time\s*based\s*range|time\s*&\s*price|time\s*and\s*price|fair\s*(price|value))
|(setup|entries|entry|confirmation\s+method|order\s*block|liquidity|price\s+delivery)
|(session|london|new\s*york|asia|candle|range)
|(how\s+i\s+trade|how\s+i\s+pass|explained|full\s+breakdown|a\s*-\s*z|complete\s+guide|step[-\s]by[-\s]step)
""", re.I|re.X)

# TOF: "broader videos that gets more views ... but doesn't sell that good"
TOF = re.compile(r"""
 (top\s*\d|ranked|ranking|best\s+)
|(how\s+to\s+make\s+\$|make\s+\$[\d,]+.*(month|day|week)|\$[\d,]+/month)
|(if\s+you\s+don'?t|nobody|no\s+one|99%|most\s+traders|why\s+.*lose|everyone)
|(my\s+story|struggled|don'?t\s+give\s+up|will\s+change|change\s+how\s+you)
|(psychology|mindset)
|(prop\s+firms?\s+(don'?t|are|hiding)|milk\s+prop|hiding\s+from\s+you)
|(learned\s+this|day\s+in\s+the\s+life)
""", re.I|re.X)

def classify(t):
    if BOF.search(t): return 'BOF'
    if TOF.search(t) and not MOF.search(t): return 'TOF'
    if MOF.search(t): return 'MOF'
    if TOF.search(t): return 'TOF'
    return 'MOF'

for h,label in [('itsjjsimon','JJ SIMON'),('DayTradingRauf','RAUF'),('HanckFXBusiness','HANCK')]:
    rows=json.load(open(f'{h}_all.json'))
    b={'TOF':[],'MOF':[],'BOF':[]}
    for r in rows:
        r['n']=v2n(r.get('views','')); b[classify(r['title'])].append(r)
    n=len(rows)
    print('='*80); print(f'{label} (n={n}) — classified by Hanck\'s own definitions'); print('='*80)
    for k in ['TOF','MOF','BOF']:
        g=b[k]; avg=sum(x['n'] for x in g)//len(g) if g else 0
        print(f"  {k}: {len(g):>2} ({len(g)/n:>5.1%})   avg {avg:>7,} views")
    if label=='RAUF':
        print("\n  RAUF's BOF videos:")
        for x in sorted(b['BOF'],key=lambda y:-y['n']): print(f"     {x['n']:>7,} | {x['title'][:76]}")
    if label=='JJ SIMON':
        print("\n  JJ's BOF videos:")
        for x in sorted(b['BOF'],key=lambda y:-y['n']): print(f"     {x['n']:>7,} | {x['title'][:76]}")
    print()
    json.dump({k:[x['title'] for x in v] for k,v in b.items()},open(f'{h}_hanck_stage.json','w'),indent=1)
