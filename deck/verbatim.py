import re,glob,json,html
fs=sorted(glob.glob('unpacked/ppt/slides/slide*.xml'),key=lambda p:int(re.search(r'slide(\d+)',p).group(1)))
out={}
for p in fs:
    n=int(re.search(r'slide(\d+)',p).group(1))
    x=open(p).read()
    paras=[]
    for m in re.finditer(r'<a:p>(.*?)</a:p>',x,re.S):
        runs=[html.unescape(t) for t in re.findall(r'<a:t>(.*?)</a:t>',m.group(1),re.S)]
        paras.append(''.join(runs))
    out[n]=paras
json.dump(out,open('verbatim.json','w'),ensure_ascii=False,indent=0)
tot=sum(len(''.join(v)) for v in out.values())
print('slides',len(out),'chars',tot)
# multi-paragraph slides
mp=[(n,v) for n,v in out.items() if len([q for q in v if q.strip()])>1]
print('multi-paragraph slides:',len(mp))
