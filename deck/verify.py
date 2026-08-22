import json,re,zipfile,html,sys
V=json.load(open('verbatim.json'))
# every non-empty source paragraph, normalised
def norm(s): return re.sub(r'\s+',' ',s).strip()
src=[]
for n in range(1,322):
    for p in V[str(n)]:
        if p.strip(): src.append((n,norm(p)))
# text actually in the output deck, per slide, runs concatenated per paragraph
z=zipfile.ZipFile('DTR_Intro_Content_designed.pptx')
names=sorted([x for x in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$',x)],
             key=lambda p:int(re.search(r'(\d+)',p.split('/')[-1]).group()))
out=set(); outraw=[]
for nm in names:
    x=z.read(nm).decode()
    for m in re.finditer(r'<a:p>(.*?)</a:p>',x,re.S):
        t=html.unescape(''.join(re.findall(r'<a:t>(.*?)</a:t>',m.group(1),re.S)))
        if t.strip(): out.add(norm(t)); outraw.append(norm(t))
print('output slides:',len(names))
missing=[(n,s) for n,s in src if s not in out]
print(f'source paragraphs: {len(src)}   present in output: {len(src)-len(missing)}   MISSING: {len(missing)}')
for n,s in missing[:25]: print(f'   slide {n}: {s[:100]!r}')
# words check
sw=set(); 
for n,s in src: sw|=set(re.findall(r"[A-Za-z0-9$%]+",s))
ow=set()
for s in out: ow|=set(re.findall(r"[A-Za-z0-9$%]+",s))
lost=sorted(sw-ow)
print(f'\ndistinct word-tokens in source: {len(sw)}   lost: {len(lost)}')
if lost: print('   ',lost[:40])
