import json,re
def v2n(s):
    s=(s or '').replace(' views','').replace(',','').strip()
    m=re.match(r'^([\d.]+)([KM]?)$',s)
    return int(float(m.group(1))*{'':1,'K':1e3,'M':1e6}[m.group(2)]) if m else 0

# BOF = proof of result / decision stage: personal payouts, episodes, student results, day-in-life
BOF = re.compile(r"""
 (\bEp\.?\s*\d|\bEpisode\s*\d)                       # serialized payout show
|(every\s+(single\s+)?trade|filmed\s+every|this\s+week[^a-z]|payout\s+breakdown|road\s+to\s+\$)
|(my\s+biggest\s+day|in\s+one\s+day|i\s+lost\s+\$)
|(student|students)
|(day\s+in\s+the\s+life)
|(testimonial|client\s+interview|he\s+went\s+from|went\s+from\s+unprofitable)
|(behind\s+the\s+scenes|documentary|live\s+walkthrough)
|(how\s+we\s+(helped\s+)?scaled?|we\s+scaled|how\s+we\s+made|we\s+made\s+\$|we\s+booked|we\s+help)
""", re.I|re.X)

# MOF = mechanism / how-to / system / solution-aware
MOF = re.compile(r"""
 (strategy|setup|system|method|model|entries|entry|confirmation)
|(backtest|backtested|data|statistic|win\s*rate|%)
|(time\s*based\s*range|time\s*&\s*price|time\s*and\s*price|fair\s*(price|value))
|(candle|range|session|order\s*block|liquidity|price\s+delivery)
|(how\s+i\s+trade|how\s+i\s+pass|how\s+to\s+trade|explained|guide|full\s+breakdown|a\s*-\s*z|step[-\s]by[-\s]step)
|(blueprint|roadmap|funnel|vsl|framework|full\s+course|module)
""", re.I|re.X)

# TOF = broad / problem-aware / opinion / rankings / aspiration, no mechanism required
TOF = re.compile(r"""
 (top\s*\d|ranked|ranking|i\s+ranked|best\s+)
|(if\s+you\s+don'?t|nobody|no\s+one|everyone|99%|most\s+traders|why\s+.*lose)
|(don'?t\s+give\s+up|my\s+story|struggled|will\s+change|change\s+how\s+you)
|(psychology|mindset)
|(prop\s+firms?\s+(don'?t|are|hiding)|milk\s+prop|what\s+they'?re\s+hiding)
|(vs\.?\s|versus)
|(how\s+to\s+make\s+\$[\d,]+[km]?(/|\s+per\s+)?(month|mo|day|week)|make\s+\$[\d,]+.*(month|per\s+month))
|(is\s+not\s+gonna|f\*ck\s+you\s+money|life\s+update|my\s+plan\s+to)
""", re.I|re.X)

def classify(t):
    b,m,o = bool(BOF.search(t)), bool(MOF.search(t)), bool(TOF.search(t))
    if b: return 'BOF'
    if o and not m: return 'TOF'
    if o and m: return 'TOF'   # aspiration framing dominates click behaviour
    if m: return 'MOF'
    return 'TOF'

for h,label in [('itsjjsimon','JJ SIMON'),('DayTradingRauf','RAUF'),('HanckFXBusiness','HANCK')]:
    rows=json.load(open(f'{h}_all.json'))
    buckets={'TOF':[],'MOF':[],'BOF':[]}
    for r in rows:
        r['n']=v2n(r.get('views',''))
        buckets[classify(r['title'])].append(r)
    n=len(rows)
    print('='*92); print(f'{label}  (n={n})'); print('='*92)
    for k in ['TOF','MOF','BOF']:
        g=buckets[k]; avg=sum(x['n'] for x in g)//len(g) if g else 0
        tot=sum(x['n'] for x in g)
        print(f"  {k}: {len(g):>2} videos ({len(g)/n:>5.1%})   avg {avg:>7,} views   total {tot:>9,}")
    print()
    for k in ['TOF','MOF','BOF']:
        print(f'  --- {k} ---')
        for x in sorted(buckets[k],key=lambda y:-y['n'])[:40]:
            print(f"      {x['n']:>7,} | {x['title'][:82]}")
        print()
    json.dump({k:[x['title'] for x in v] for k,v in buckets.items()},open(f'{h}_funnel.json','w'),indent=1)
