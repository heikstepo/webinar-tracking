import json, re, glob, os

S = json.load(open('byslide.json'))
ns = sorted(int(k) for k in S)

# ---- resolve each slide's pictures to real files ---------------------------
for n in ns:
    pics = S[str(n)]['pics']
    if not pics:
        continue
    relp = f'fu/ppt/slides/_rels/slide{n}.xml.rels'
    rels = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', open(relp).read()))
    for p in pics:
        t = rels.get(p['rid'], '')
        p['file'] = os.path.normpath(os.path.join('fu/ppt/slides', t)) if t else None

# ---- bands: the five steps -------------------------------------------------
band = {}
cur = 0
banners = {}
for n in ns:
    L = S[str(n)]['lines']
    joined = ' '.join(L[:2]) if L else ''
    m = re.match(r'^(STEP\s*(\d+))(\s*:)\s*(.+)$', joined)
    if m:
        cur = int(m.group(2))
        banners[cur] = dict(head=m.group(1), sep=m.group(3), tail=m.group(4),
                            full=joined, parts=L[:2])
        S[str(n)]['lines'] = [joined] + L[2:]
    band[n] = cur
# the offer/recap sections come after step 5 and carry no banner
first_offer = min([n for n in ns if S[str(n)]['stack']] or [10**9])
recap_start = 322
for n in ns:
    if n >= recap_start:
        band[n] = 0

# ---- offer components: rejoin the code with its title, and feed the stacks --
ITEM = re.compile(r'^(?:BONUS\s*\d+\s*:|\d+\))$')
items = []
stack_rows = {}
for n in ns:
    L = S[str(n)]['lines']
    if len(L) == 2 and ITEM.match(L[0].strip()):
        joined = L[0].strip() + ' ' + L[1].strip()
        S[str(n)]['lines'] = [joined]
        S[str(n)]['item'] = True
        items.append(joined)
    if S[str(n)]['stack']:
        stack_rows[n] = list(items)

# ---- what accumulates (deliberately rare) ----------------------------------
NUM = re.compile(r'^((?:Q\d+\s*[-–—:])|(?:BONUS\s*\d+\s*:)|(?:\d+\s*[.)\-]))\s')
runs = []
cur = []
for n in ns:
    L = S[str(n)]['lines']
    if L and NUM.match(L[0]) and not S[str(n)]['stack']:
        cur.append(n)
    else:
        if len(cur) > 1:
            runs.append(cur)
        cur = []
if len(cur) > 1:
    runs.append(cur)

ACC = []
for r in runs:                                   # a list needs its heading
    h = r[0] - 1
    L = S[str(h)]['lines'] if str(h) in S else []
    if len(L) == 1 and not NUM.match(L[0]) and (L[0].rstrip().endswith(':') or len(L[0]) < 90) \
       and not S[str(h)]['pics'] and not S[str(h)]['stack']:
        ACC.append([h] + r)
    else:
        ACC.append(r)

# the handful of moments where the stacking is the whole point
CURATED = [
    (54, 56),    # 8:20 / Not 8:00 / 8:20
    (137, 143),  # the losing-day spiral
    (205, 209),  # where we are, then the problem
    (261, 265),  # boxes / direction / target / price
    (422, 427),  # everything walked through
    (462, 464),  # And I mean me. / Not a chatbot / Me.
    (483, 486),  # the guarantee escalation
    (488, 491),  # I'm on the live sessions / calls / DMs
    (496, 500),  # everything just added on top
]
for a, b in CURATED:
    ACC.append([n for n in range(a, b + 1) if n in band])

taken = {n for g in ACC for n in g}
groups = []
for n in ns:
    if n in taken:
        continue
    groups.append([n])
groups += ACC
groups.sort(key=lambda g: g[0])
# no overlaps
flat = [n for g in groups for n in g]
assert flat == sorted(flat) and len(flat) == len(set(flat)) == len(ns), 'group overlap'

def kind_of(g):
    n = g[0]
    s = S[str(n)]
    L = s['lines']
    if s['stack']:
        return 'stack'
    if s['pics'] and (not L or (len(L) == 1 and len(L[0]) <= 30)):
        return 'shot'
    if s.get('item'):
        return 'item'
    if L and re.match(r'^STEP\s*\d+\s*:', L[0]):
        return 'div'
    if len(g) > 1 and any(NUM.match(S[str(m)]['lines'][0]) for m in g if S[str(m)]['lines']):
        return 'list'
    if len(g) == 1 and L and all(NUM.match(x) for x in L) and len(L) > 1:
        # every row is "N- TITLE -- descriptor": lay it out as a structure
        if all(re.search(r'—|–', x) for x in L):
            return 'steps'
        return 'list'
    return 'stmt'

plan = []
for g in groups:
    e = dict(k=kind_of(g), slides=g, band=band[g[0]])
    if e['k'] == 'stack':
        e['rows'] = stack_rows.get(g[0], [])
    plan.append(e)

json.dump(dict(plan=plan, slides=S, banners=banners), open('plan2.json', 'w'), ensure_ascii=False)
from collections import Counter
print('physical slides:', len(ns), '  conceptual slides:', len(plan))
print('kinds:', Counter(p['k'] for p in plan))
print('accumulating groups:', sum(1 for p in plan if len(p['slides']) > 1),
      f"({100*sum(1 for p in plan if len(p['slides'])>1)//len(plan)}% of slides)")
print('banners:', {k: v['full'] for k, v in banners.items()})
