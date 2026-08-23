import re,glob,json,html
E=914400.0
def slides():
    return sorted(glob.glob('fu/ppt/slides/slide*.xml'),
                  key=lambda p:int(re.search(r'slide(\d+)',p).group(1)))

def parse(p):
    n=int(re.search(r'slide(\d+)',p).group(1)); x=open(p).read()
    bg=re.search(r'<p:bg>.*?srgbClr val="([0-9A-Fa-f]{6})"',x,re.S)
    dark = bool(bg) and bg.group(1).upper() in ('0A0A0A','000000')
    boxes=[]; pics=[]; ell=0; spine=False
    for m in re.finditer(r'<p:(sp|pic|cxnSp)>(.*?)</p:\1>',x,re.S):
        kind,b=m.group(1),m.group(2)
        off=re.search(r'<a:off x="(-?\d+)" y="(-?\d+)"/><a:ext cx="(\d+)" cy="(\d+)"',b)
        if not off: continue
        X,Y,W,H=[int(off.group(i))/E for i in (1,2,3,4)]
        if kind=='pic':
            r=re.search(r'r:embed="(rId\d+)"',b)
            pics.append(dict(rid=r.group(1) if r else None,x=round(X,2),y=round(Y,2),
                             w=round(W,2),h=round(H,2))); continue
        g=re.search(r'<a:prstGeom prst="(\w+)"',b)
        if g and g.group(1)=='ellipse' and W<0.35: ell+=1
        if kind=='cxnSp' and abs(X-0.80)<0.06: spine=True
        # the chapter banner, precisely: top strip, 7.19in wide, centred 11.7pt
        if Y<0.20 and abs(W-7.19)<0.6: continue
        ps=[html.unescape(''.join(re.findall(r'<a:t>(.*?)</a:t>',q.group(1),re.S))).strip()
            for q in re.finditer(r'<a:p>(.*?)</a:p>',b,re.S)]
        ps=[q for q in ps if q]
        if not ps: continue
        sz=re.search(r'sz="(\d+)"',b); sz=int(sz.group(1))/100 if sz else 18
        boxes.append(dict(x=X,y=Y,w=W,sz=sz,ps=ps))
    return dict(n=n,dark=dark,boxes=boxes,pics=pics,ell=ell,spine=spine)

def lines_of(s):
    bs=list(s['boxes'])
    # drop the decorative 150pt divider numeral (the digit already shown in "STEP n:")
    steps={m.group(1) for b in bs for q in b['ps'] for m in [re.match(r'STEP\s*(\d+)',q)] if m}
    bs=[b for b in bs if not (b['sz']>=100 and len(b['ps'])==1
                              and b['ps'][0].isdigit() and b['ps'][0] in steps)]
    bands={}
    for b in bs:
        k=round(b['y']/0.09)
        hit=next((kk for kk in bands if abs(kk-k)<=1), None)
        bands.setdefault(hit if hit is not None else k,[]).append(b)
    out=[]
    for k in sorted(bands):
        grp=sorted(bands[k],key=lambda b:b['x'])
        if all(len(b['ps'])==1 for b in grp) and len(grp)>1:
            out.append((min(b['y'] for b in grp), ' '.join(b['ps'][0] for b in grp)))
        else:
            for b in grp:
                for q in b['ps']: out.append((b['y'],q))
    out.sort(key=lambda r:r[0])
    return [t for _,t in out]

OFFER=[ "1on1 Onboarding call, just you and me",
  "Full Time Based Ranges Course",
  "3 live trading sessions with me, every single week.",
  "Weekly group coaching calls.",
  "The private community, my weekly blueprint, and my market commentaries.",
  "The Scaling Phase - 3 extra months with me FOR FREE.",
  "I'll pay for your first prop firm challenge myself.",
  "Unlimited 1on1 DM access to me.",
  "Bi weekly 1on1 calls with me" ]
sqz=lambda s: re.sub(r'\s+','',s)
OFFSET={sqz(o) for o in OFFER}
def is_stack(s, L):
    if not s['dark'] or not L: return False
    return all(any(sqz(o) in sqz(t) for o in OFFER) for t in L)

S=[parse(p) for p in slides()]
script=[]
prev=[]
for s in S:
    L=lines_of(s)
    if is_stack(s,L):
        script.append(dict(t='STACK',kind='stack',n=s['n'],pics=[])); prev=[]; continue
    if prev and len(L)>len(prev) and L[:len(prev)]==prev: new=L[len(prev):]
    elif prev and L==prev: new=[]
    else: new=L
    if not new and s['pics']:
        script.append(dict(t='',kind='pic',n=s['n'],pics=s['pics']))
    for i,t in enumerate(new):
        script.append(dict(t=t,kind='line',n=s['n'],
                           pics=s['pics'] if i==len(new)-1 else []))
    prev=L
json.dump(script,open('recovered.json','w'),ensure_ascii=False)
print('slides:',len(S),' recovered entries:',len(script),
      ' lines:',sum(1 for e in script if e['t'] and e['t']!='STACK'),
      ' STACK:',sum(1 for e in script if e['t']=='STACK'))
