import re, io

UP = '/root/.claude/uploads/ac2859f2-9cf5-528b-b31c-f3a90db6fcf8/'
REPO = '/home/user/webinar-tracking/webinar-rauf/'

def lines(p):
    return open(p, encoding='utf-8').read().split('\n')

# ---- new open (script portion only, stops at the NOTES banner) ----
op = lines(REPO + '34-intro-open-heik-angle.txt')
start = next(i for i, l in enumerate(op) if l.strip() == 'Live Dashboard')
end = next(i for i, l in enumerate(op) if l.strip().startswith('=====') and i > start)
new_open = op[start:end]

# ---- intro: everything AFTER the Jan-Aug PNLs line ----
intro = lines(UP + '629824c8-DTR__Webby_Intro_heik_3.txt')
pnl = next(i for i, l in enumerate(intro) if 'January - August PNLs' in l)
intro_rest = intro[pnl + 1:]

# ---- content: drop the metadata block accidentally pasted into step 4 ----
content = lines(UP + '9aa82525-DTR_content_section_heiko_3.txt')
bad = [
    'STEP 4: THE EXIT\nWhere you get out',
    '~490 words, down from ~750.',
    'Main cut: The Feb/Mar/Apr + Apex P&L block',
    'Notes at the bottom.',
    'Where you get out',
]
out, i = [], 0
dropped = 0
while i < len(content):
    l = content[i]
    s = l.strip()
    if (s == '~490 words, down from ~750.'
            or s.startswith('Main cut: The Feb/Mar/Apr')
            or s == 'Notes at the bottom.'
            or s == 'Where you get out'):
        dropped += 1
        i += 1
        continue
    out.append(l)
    i += 1
content = out

# drop the duplicated bare "STEP 4: THE EXIT" (keep the one inside the ==== banner)
seen4 = 0
out = []
for l in content:
    if l.strip() == 'STEP 4: THE EXIT':
        seen4 += 1
        if seen4 == 2:
            dropped += 1
            continue
    out.append(l)
content = out

all_lines = new_open + [''] + intro_rest + [''] + content
open('/tmp/claude-0/-home-user-webinar-tracking/ac2859f2-9cf5-528b-b31c-f3a90db6fcf8/scratchpad/combined.txt', 'w', encoding='utf-8').write('\n'.join(all_lines))
print('dropped', dropped, 'metadata lines;', len(all_lines), 'raw lines')
