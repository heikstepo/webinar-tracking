import json,re,zipfile,html
V=json.load(open('verbatim.json'))
squash=lambda s: re.sub(r'\s+','',s)
z=zipfile.ZipFile('DTR_Intro_Content_designed.pptx')
names=sorted([x for x in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$',x)],
             key=lambda p:int(re.search(r'(\d+)',p.split('/')[-1]).group()))
slides=[]
for nm in names:
    x=z.read(nm).decode()
    slides.append(squash(html.unescape(''.join(re.findall(r'<a:t>(.*?)</a:t>',x,re.S)))))
allout=''.join(slides)
bad=[]
for n in range(1,322):
    for p in V[str(n)]:
        if not p.strip(): continue
        q=squash(p)
        if not any(q in s for s in slides): bad.append((n,p))
print(f'source paragraphs checked: 404')
print(f'NOT found intact on any output slide: {len(bad)}')
for n,p in bad: print(f'   slide {n}: {p[:95]!r}')
