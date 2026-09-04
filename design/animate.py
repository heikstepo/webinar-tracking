#!/usr/bin/env python3
"""Turn an animated slide into an MP4.

    python3 animate.py slides/foo.html exports/foo.mp4 [seconds] [fps]

The slide must expose a global render(t) that sets every visual from t alone.
We drive that function frame by frame and screenshot, rather than letting the
page animate in real time and recording it: a screenshotter cannot keep real
time, so a recorded CSS animation drops and doubles frames unpredictably.
Driving t by hand makes every frame exact and the render reproducible.
"""
import os, subprocess, sys, tempfile
from playwright.sync_api import sync_playwright
import imageio_ffmpeg

src   = os.path.abspath(sys.argv[1])
out   = os.path.abspath(sys.argv[2])
secs  = float(sys.argv[3]) if len(sys.argv) > 3 else 12.0
fps   = int(sys.argv[4])   if len(sys.argv) > 4 else 30
frames = int(secs * fps)

tmp = tempfile.mkdtemp(prefix='frames-')
with sync_playwright() as pw:
    # The pip playwright here wants a browser build the image doesn't carry,
    # so point it at the Chromium that is already installed rather than
    # downloading a second copy.
    b = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
                           args=['--force-color-profile=srgb',
                                 '--font-render-hinting=none'])
    # 1440x810 authored, 4/3 device scale => exactly 1920x1080 out, no resample.
    pg = b.new_page(viewport={'width': 1440, 'height': 810},
                    device_scale_factor=4 / 3)
    pg.goto('file://' + src)
    # Shoot the slide element, not the viewport: the stylesheet floats the
    # slide on a grey workbench so its edges read while editing, and a viewport
    # shot brings that grey into the video.
    slide = pg.locator('.slide')
    pg.wait_for_function('typeof window.render === "function"')
    # Belt and braces: the slide should already animate purely through
    # render(t), but any stray transition would smear across frames captured
    # off the wall clock, so make sure none can run.
    pg.add_style_tag(content='*{transition:none!important;animation:none!important}')
    for i in range(frames):
        pg.evaluate('window.render(%r)' % (i / fps))
        slide.screenshot(path=os.path.join(tmp, 'f%05d.png' % i))
        if i % 30 == 0:
            print('  %d/%d' % (i, frames), flush=True)
    b.close()

subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error',
                '-framerate', str(fps), '-i', os.path.join(tmp, 'f%05d.png'),
                '-c:v', 'libx264', '-preset', 'slow', '-crf', '18',
                '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], check=True)
subprocess.run(['rm', '-rf', tmp])
print('wrote', out, '(%.1fs @ %dfps)' % (secs, fps))
