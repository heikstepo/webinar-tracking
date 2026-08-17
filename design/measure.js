/* Injected into a slide before render. Walks the elements the pptx builder
   cares about and writes their real, laid-out geometry into #measure-out, so
   the deck is positioned from what Chrome actually did rather than from a
   hand-recomputed box model. Read it back with `chrome --dump-dom`. */
(function () {
  var slide = document.querySelector('.slide');
  var base = slide.getBoundingClientRect();

  function px(v) { return Math.round(v * 100) / 100; }

  function box(el) {
    var r = el.getBoundingClientRect();
    return { x: px(r.left - base.left), y: px(r.top - base.top), w: px(r.width), h: px(r.height) };
  }

  function type(el) {
    var s = getComputedStyle(el);
    var lh = s.lineHeight === 'normal'
      ? parseFloat(s.fontSize) * 1.2
      : parseFloat(s.lineHeight);
    return {
      size: parseFloat(s.fontSize),
      weight: parseInt(s.fontWeight, 10),
      lineHeight: px(lh),
      tracking: s.letterSpacing === 'normal' ? 0 : parseFloat(s.letterSpacing),
      color: s.color,
      align: s.textAlign
    };
  }

  /* The first line's baseline, found by measuring a one-character range —
     the only reliable way to know where Chrome actually set the text. */
  function baseline(el) {
    var walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    var node;
    while ((node = walker.nextNode())) {
      if (!node.nodeValue.trim()) continue;
      var i = node.nodeValue.search(/\S/);
      var range = document.createRange();
      range.setStart(node, i);
      range.setEnd(node, i + 1);
      var r = range.getBoundingClientRect();
      /* A range box spans the font's em box, not the line box; its bottom sits
         at the descender, so back off by the descent to reach the baseline. */
      return px(r.bottom - base.top);
    }
    return null;
  }

  function part(el) {
    if (!el) return null;
    var o = box(el);
    o.text = el.textContent.trim();
    o.type = type(el);
    o.baseline = baseline(el);
    return o;
  }

  var out = {
    slide: { w: px(base.width), h: px(base.height) },
    background: getComputedStyle(slide).backgroundColor
  };

  out.eyebrow = part(slide.querySelector('.eyebrow'));
  out.h1 = part(slide.querySelector('.h1'));

  var head = slide.querySelector('.pillar-head');
  if (head) {
    out.head = part(head);
    out.head.num = part(head.querySelector('.pillar-head__num'));
    out.head.label = part(head.querySelector('.pillar-head__num + span'));
  }

  var list = slide.querySelector('.build');
  if (list) {
    out.list = box(list);
    out.list.classes = list.className;
    out.list.items = [].map.call(list.querySelectorAll('li'), function (li) {
      var o = part(li);
      o.numbered = li.classList.contains('numbered');
      var n = li.querySelector('.build__n');
      if (n) {
        o.num = part(n);
        o.label = part(li.querySelector('.build__n + span'));
      } else {
        var d = getComputedStyle(li, '::before');
        var lr = li.getBoundingClientRect();
        o.dot = {
          x: px(lr.left - base.left + parseFloat(d.left || 0)),
          y: px(lr.top - base.top + parseFloat(d.top || 0)),
          size: parseFloat(d.width),
          color: d.backgroundColor
        };
      }
      /* Line count, so the builder knows which items wrap. */
      o.lines = Math.round(o.h / o.type.lineHeight);
      return o;
    });
  }

  var pre = document.createElement('pre');
  pre.id = 'measure-out';
  pre.textContent = JSON.stringify(out);
  document.body.appendChild(pre);
})();
