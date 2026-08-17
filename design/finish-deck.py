#!/usr/bin/env python3
"""Patch the two things pptxgenjs cannot express, then repack.

    python3 finish-deck.py exports/five-pillars.pptx

1. pptxgenjs writes one <a:pPr> per run, so a paragraph built from several
   runs ends up with several. The schema allows exactly one, first; PowerPoint
   is forgiving but Keynote and Google Slides are not. Keep the first, drop
   the rest.

2. There is no option for bullet colour. The design's bullet is the accent
   blue while its text is near-black, which in OOXML is <a:buClr> — inserted
   here, in its required slot between <a:spcAft> and <a:buSzPct>.

Regex rather than an XML round-trip on purpose: ElementTree rewrites the
namespace prefixes and the result will not open.
"""

import re
import shutil
import sys
import zipfile

ACCENT = '0071E3'
BU_CLR = f'<a:buClr><a:srgbClr val="{ACCENT}"/></a:buClr>'
BU_FONT = '<a:buFont typeface="Arial" pitchFamily="34" charset="0"/>'

PARA = re.compile(r'<a:p>.*?</a:p>', re.S)
PPR = re.compile(r'<a:pPr(?:\s[^>]*)?/>|<a:pPr(?:\s[^>]*)?>.*?</a:pPr>', re.S)


def one_ppr(xml):
    """Leave a paragraph with a single <a:pPr>, the first one."""
    dropped = 0

    def fix(match):
        nonlocal dropped
        para = match.group(0)
        seen = 0

        def keep_first(m):
            nonlocal seen, dropped
            seen += 1
            if seen == 1:
                return m.group(0)
            dropped += 1
            return ''

        return PPR.sub(keep_first, para)

    return PARA.sub(fix, xml), dropped


def colour_bullets(xml):
    """Give every character bullet the accent colour and a known bullet font."""
    count = 0

    def fix(match):
        nonlocal count
        ppr = match.group(0)
        if '<a:buChar' not in ppr or '<a:buClr' in ppr:
            return ppr
        count += 1
        ppr = ppr.replace('<a:buSzPct', BU_CLR + '<a:buSzPct', 1)
        return ppr.replace('<a:buChar', BU_FONT + '<a:buChar', 1)

    return PPR.sub(fix, xml), count


def main(path):
    backup = path + '.raw'
    shutil.copy(path, backup)

    src = zipfile.ZipFile(backup)
    dropped = coloured = 0

    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as out:
        for item in src.infolist():
            data = src.read(item.filename)
            if re.fullmatch(r'ppt/slides/slide\d+\.xml', item.filename):
                xml = data.decode('utf-8')
                xml, d = one_ppr(xml)
                xml, c = colour_bullets(xml)
                dropped += d
                coloured += c
                data = xml.encode('utf-8')
            out.writestr(item, data)

    src.close()
    print(f'patched {path}: dropped {dropped} duplicate <a:pPr>, '
          f'coloured {coloured} bullets')

    # Nothing reads the pre-patch copy; it only exists so a failed run above
    # leaves the original intact.
    import os
    os.remove(backup)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'exports/five-pillars.pptx')
