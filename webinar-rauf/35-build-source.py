import os, re, shutil, zipfile

SCR = '/tmp/claude-0/-home-user-webinar-tracking/ac2859f2-9cf5-528b-b31c-f3a90db6fcf8/scratchpad'
TPL, BLD = SCR + '/tpl', SCR + '/build'
OUT = '/home/user/webinar-tracking/webinar-rauf/35-DTR-intro-and-content.pptx'

# ---------------- 1. script -> slides ----------------
raw = open(SCR + '/combined.txt', encoding='utf-8').read().split('\n')

# rejoin lines hard-wrapped mid-sentence in the source files
joined, prev = [], None
for l in raw:
    s = l.strip()
    if s and prev is not None and joined[prev].strip():
        p_ = joined[prev].strip()
        if (s[:1].islower() and not p_.startswith('[')
                and not p_.endswith(('.', '!', '?', '\u2026', ':', ';', '-', '\u2014'))):
            joined[prev] = p_ + ' ' + s
            continue
    joined.append(l)
    if s:
        prev = len(joined) - 1
raw = joined

slides = []          # list of (list_of_paragraphs, italic_bool)
in_live = False
i = 0
while i < len(raw):
    s = raw[i].strip()
    i += 1
    if not s or re.fullmatch(r'=+', s):
        continue
    if s == 'LIVE START':
        in_live = True
        continue
    if s == 'LIVE END':
        in_live = False
        continue
    if s == 'SHOW LIVE':
        slides.append((['LIVE'], False))
        continue
    if s.startswith('SHOW DATA'):
        slides.append((['SHOW DATA'], False))
        url = s.split('REFERENCE:', 1)[-1].strip() if 'REFERENCE:' in s else ''
        if url:
            slides.append(([url], True))
        continue
    if s.startswith('*'):                      # group a run of bullets onto one slide
        bullets = [s.lstrip('* ').strip()]
        while i < len(raw) and (not raw[i].strip() or raw[i].strip().startswith('*')):
            t = raw[i].strip()
            i += 1
            if t.startswith('*'):
                bullets.append(t.lstrip('* ').strip())
            elif bullets and i < len(raw) and not raw[i].strip().startswith('*'):
                break
        slides.append((bullets, in_live))
        continue
    slides.append(([s], in_live or s.startswith('[')))

print(len(slides), 'slides')

# ---------------- 2. package ----------------
shutil.rmtree(BLD, ignore_errors=True)
shutil.copytree(TPL, BLD)
for d in ('ppt/slides', 'ppt/notesSlides'):
    p = os.path.join(BLD, d)
    if os.path.isdir(p):
        shutil.rmtree(p)
os.makedirs(BLD + '/ppt/slides/_rels')

NS = ('xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
      'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"')

def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def para(text, italic):
    ital = ' i="1"' if italic else ''
    fonts = ('<a:latin typeface="Poppins"/><a:ea typeface="Poppins"/>'
             '<a:cs typeface="Poppins"/><a:sym typeface="Poppins"/>')
    fill = '<a:solidFill><a:srgbClr val="000000"/></a:solidFill>'
    return ('<a:p><a:pPr indent="0" lvl="0" marL="0" rtl="0" algn="ctr">'
            '<a:spcBef><a:spcPts val="0"/></a:spcBef>'
            '<a:spcAft><a:spcPts val="0"/></a:spcAft><a:buNone/></a:pPr>'
            f'<a:r><a:rPr b="1"{ital} lang="en" sz="3200">{fill}{fonts}</a:rPr>'
            f'<a:t>{esc(text)}</a:t></a:r>'
            f'<a:endParaRPr b="1"{ital} sz="3200">{fill}{fonts}</a:endParaRPr></a:p>')

SLIDE = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
         f'<p:sld {NS}><p:cSld><p:spTree>'
         '<p:nvGrpSpPr><p:cNvPr id="1" name="Shape 1"/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
         '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
         '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
         '<p:sp><p:nvSpPr><p:cNvPr id="2" name="Script"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
         '<p:spPr><a:xfrm><a:off x="85500" y="257175"/><a:ext cx="8973000" cy="4629150"/></a:xfrm>'
         '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>'
         '<p:txBody><a:bodyPr anchorCtr="0" anchor="ctr" bIns="91425" lIns="91425" '
         'spcFirstLastPara="1" rIns="91425" wrap="square" tIns="91425"/><a:lstStyle/>'
         '{BODY}</p:txBody></p:sp>'
         '</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>')

RELS = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" '
        'Target="../slideLayouts/slideLayout1.xml"/></Relationships>')

for n, (paras, italic) in enumerate(slides, 1):
    body = ''.join(para(t, italic) for t in paras)
    open(f'{BLD}/ppt/slides/slide{n}.xml', 'w', encoding='utf-8').write(
        SLIDE.replace('{BODY}', body))
    open(f'{BLD}/ppt/slides/_rels/slide{n}.xml.rels', 'w', encoding='utf-8').write(RELS)

# ---------------- 3. presentation.xml + rels + content types ----------------
pres = open(BLD + '/ppt/presentation.xml', encoding='utf-8').read()
sldids = ''.join(f'<p:sldId id="{255+n}" r:id="rId{5000+n}"/>' for n in range(1, len(slides) + 1))
pres = re.sub(r'<p:sldIdLst>.*?</p:sldIdLst>', f'<p:sldIdLst>{sldids}</p:sldIdLst>', pres, flags=re.S)
open(BLD + '/ppt/presentation.xml', 'w', encoding='utf-8').write(pres)

pr = open(BLD + '/ppt/_rels/presentation.xml.rels', encoding='utf-8').read()
pr = re.sub(r'<Relationship [^>]*Target="slides/slide\d+\.xml"/>', '', pr)
new = ''.join(
    f'<Relationship Id="rId{5000+n}" '
    'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" '
    f'Target="slides/slide{n}.xml"/>' for n in range(1, len(slides) + 1))
pr = pr.replace('</Relationships>', new + '</Relationships>')
open(BLD + '/ppt/_rels/presentation.xml.rels', 'w', encoding='utf-8').write(pr)

ct = open(BLD + '/[Content_Types].xml', encoding='utf-8').read()
ct = re.sub(r'<Override [^>]*PartName="/ppt/(?:slides|notesSlides)/[^"]*"/>', '', ct)
new = ''.join(
    '<Override ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml" '
    f'PartName="/ppt/slides/slide{n}.xml"/>' for n in range(1, len(slides) + 1))
ct = ct.replace('</Types>', new + '</Types>')
open(BLD + '/[Content_Types].xml', 'w', encoding='utf-8').write(ct)

# ---------------- 4. zip ----------------
if os.path.exists(OUT):
    os.remove(OUT)
zf = zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED)
for root, _, files in os.walk(BLD):
    for f in files:
        full = os.path.join(root, f)
        zf.write(full, os.path.relpath(full, BLD))
zf.close()
print('wrote', OUT, os.path.getsize(OUT), 'bytes')
