// Zaid Saifan Portfolio — interactions and effects. The page is fully readable without this file.
(function () {
  'use strict';
  var root = document.documentElement;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var clamp = function (v, a, b) { return Math.min(b, Math.max(a, v)); };
  function cssVar(name) { return getComputedStyle(root).getPropertyValue(name).trim(); }

  /* ---------- Theme toggle ---------- */
  var themeBtn = $('.theme-toggle');
  if (themeBtn) themeBtn.addEventListener('click', function () {
    var next = root.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('theme', next); } catch (e) {}
    document.dispatchEvent(new Event('themechange'));
  });

  /* ---------- Mobile menu ---------- */
  var head = $('.site-head');
  var menuBtn = $('.menu-toggle');
  function setMenu(open) {
    head.classList.toggle('is-open', open);
    menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    menuBtn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  }
  if (menuBtn) {
    menuBtn.addEventListener('click', function () { setMenu(!head.classList.contains('is-open')); });
    $$('.nav a').forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });
  }

  /* ---------- Scroll-linked UI: sticky header, progress, back-to-top, active nav, timeline ---------- */
  var progress = $('.progress');
  var toTop = $('.to-top');
  var navLinks = $$('.nav a[data-nav]');
  var navInd = $('.nav-ind');
  var sections = navLinks.map(function (a) { return document.getElementById(a.getAttribute('data-nav')); });
  var timeline = $('.timeline');
  var jobs = $$('.job');
  var activeLink = null;

  function moveInd(link) {
    if (!navInd) return;
    if (!link || getComputedStyle(navInd).display === 'none') { navInd.style.opacity = 0; return; }
    navInd.style.opacity = 1;
    navInd.style.left = link.offsetLeft + 'px';
    navInd.style.width = link.offsetWidth + 'px';
  }

  function onScroll() {
    var y = window.scrollY, vh = window.innerHeight;
    var max = document.documentElement.scrollHeight - vh;
    var p = max > 0 ? clamp(y / max, 0, 1) : 0;
    if (head) head.classList.toggle('is-stuck', y > 10);
    if (progress) progress.style.setProperty('--p', p);
    if (toTop) { toTop.style.setProperty('--p', p); toTop.classList.toggle('is-on', y > vh * 0.8); }

    if (navLinks.length) {
      var current = null;
      sections.forEach(function (s, i) { if (s && s.getBoundingClientRect().top < vh * 0.4) current = navLinks[i]; });
      if (window.innerHeight + y >= document.documentElement.scrollHeight - 4) current = navLinks[navLinks.length - 1];
      if (current !== activeLink) {
        navLinks.forEach(function (a) { a.classList.toggle('is-active', a === current); });
        activeLink = current; moveInd(current);
      }
    }
    if (timeline) {
      var r = timeline.getBoundingClientRect();
      var t = clamp((vh * 0.6 - r.top) / r.height, 0, 1);
      timeline.style.setProperty('--t', t);
      jobs.forEach(function (j) { j.classList.toggle('is-lit', j.getBoundingClientRect().top + 30 < vh * 0.6); });
    }
  }
  var ticking = false;
  window.addEventListener('scroll', function () {
    if (!ticking) { ticking = true; requestAnimationFrame(function () { onScroll(); ticking = false; }); }
  }, { passive: true });
  window.addEventListener('resize', function () { moveInd(activeLink); onScroll(); });
  onScroll();

  /* ---------- Hero name: split into letters ---------- */
  $$('.hero-name .split').forEach(function (word, w) {
    var text = word.textContent; word.textContent = '';
    word.setAttribute('aria-hidden', 'true');
    for (var i = 0; i < text.length; i++) {
      var s = document.createElement('span');
      s.className = 'ch'; s.textContent = text[i];
      s.style.setProperty('--i', i + w * 5);
      word.appendChild(s);
    }
  });
  // Gradient words: each letter paints its own slice of one shared gradient.
  function paintGradLetters() {
    $$('.hero-name .grad').forEach(function (word) {
      var w = word.offsetWidth;
      $$('.ch', word).forEach(function (ch) {
        ch.style.backgroundSize = w + 'px 100%';
        ch.style.backgroundPosition = (-ch.offsetLeft + word.firstElementChild.offsetLeft) + 'px 0';
      });
    });
  }
  paintGradLetters();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(paintGradLetters);
  window.addEventListener('resize', paintGradLetters);

  /* ---------- Typed role line ---------- */
  var typed = $('.typed-text');
  if (typed && !reduce) {
    var words = typed.getAttribute('data-words').split('|');
    var wi = 0, ci = words[0].length, deleting = false;
    var tick = function () {
      var word = words[wi];
      if (!deleting) {
        ci++;
        typed.textContent = word.slice(0, ci);
        if (ci >= word.length) { deleting = true; return setTimeout(tick, 1900); }
        return setTimeout(tick, 42 + Math.random() * 40);
      }
      ci--;
      typed.textContent = word.slice(0, ci);
      if (ci <= 0) { deleting = false; wi = (wi + 1) % words.length; return setTimeout(tick, 350); }
      setTimeout(tick, 22);
    };
    setTimeout(function () { deleting = true; tick(); }, 2600);
  }

  /* ---------- Circuit-trace canvas ---------- */
  $$('.hero-canvas').forEach(function (canvas) {
    var ctx = canvas.getContext('2d');
    if (!ctx) return;
    var host = canvas.parentElement;
    var base = document.createElement('canvas'), bctx = base.getContext('2d');
    var hot = document.createElement('canvas'), hctx = hot.getContext('2d');
    var tmp = document.createElement('canvas'), tctx = tmp.getContext('2d');
    var W = 0, H = 0, dpr = 1, traces = [], colors = {}, mouse = { x: -9999, y: -9999, on: false };
    var CELL = 28, running = false, visible = true, raf = 0;
    var DIRS = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]];

    function readColors() {
      colors.cu = cssVar('--copper') || '#F08A4B';
      colors.cu2 = cssVar('--copper-2') || '#FFB37A';
      colors.line = cssVar('--line-2') || '#26344A';
      colors.mask = cssVar('--mask') || '#7FB0FF';
      colors.light = root.getAttribute('data-theme') === 'light';
    }

    function build() {
      var rect = host.getBoundingClientRect();
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = Math.max(1, Math.round(rect.width)); H = Math.max(1, Math.round(rect.height));
      [canvas, base, hot, tmp].forEach(function (c) { c.width = W * dpr; c.height = H * dpr; });
      canvas.style.width = W + 'px'; canvas.style.height = H + 'px';
      var cols = Math.ceil(W / CELL) + 1, rows = Math.ceil(H / CELL) + 1;
      var used = {};
      traces = [];
      var count = Math.round((cols * rows) / 26);
      for (var n = 0; n < count * 3 && traces.length < count; n++) {
        var x = Math.floor(Math.random() * cols), y = Math.floor(Math.random() * rows);
        if (used[x + ',' + y]) continue;
        var d = Math.floor(Math.random() * 4) * 2; // start orthogonal
        var pts = [[x, y]]; used[x + ',' + y] = 1;
        var len = 5 + Math.floor(Math.random() * 16);
        for (var k = 0; k < len; k++) {
          if (Math.random() < 0.22) d = (d + (Math.random() < 0.5 ? 1 : 7)) % 8; // 45° bend
          var nx = x + DIRS[d][0], ny = y + DIRS[d][1];
          if (nx < 0 || ny < 0 || nx >= cols || ny >= rows || used[nx + ',' + ny]) break;
          x = nx; y = ny; used[x + ',' + y] = 1; pts.push([x, y]);
        }
        if (pts.length < 4) continue;
        // simplify collinear points & measure
        var P = pts.map(function (p) { return [p[0] * CELL, p[1] * CELL]; });
        var cum = [0];
        for (var i = 1; i < P.length; i++) cum.push(cum[i - 1] + Math.hypot(P[i][0] - P[i - 1][0], P[i][1] - P[i - 1][1]));
        traces.push({
          p: P, cum: cum, total: cum[cum.length - 1], blue: Math.random() < 0.18,
          pos: -Math.random() * 900, speed: 1.2 + Math.random() * 2.2, pulse: Math.random() < 0.55
        });
      }
      paintStatic();
    }

    function strokeTraces(c, color, alpha, width) {
      c.save(); c.scale(dpr, dpr);
      c.lineJoin = 'round'; c.lineCap = 'round';
      traces.forEach(function (t) {
        c.globalAlpha = alpha;
        c.strokeStyle = t.blue ? colors.mask : color; c.lineWidth = width;
        c.beginPath(); c.moveTo(t.p[0][0], t.p[0][1]);
        for (var i = 1; i < t.p.length; i++) c.lineTo(t.p[i][0], t.p[i][1]);
        c.stroke();
        var a = t.p[0], b = t.p[t.p.length - 1];
        c.fillStyle = t.blue ? colors.mask : color;
        [a, b].forEach(function (q) { c.beginPath(); c.arc(q[0], q[1], width + 1.6, 0, Math.PI * 2); c.fill(); });
        c.globalAlpha = alpha * 1.4;
        c.fillStyle = colors.light ? '#F5F7FA' : '#070B12';
        [a, b].forEach(function (q) { c.beginPath(); c.arc(q[0], q[1], width * 0.5 + 0.4, 0, Math.PI * 2); c.fill(); });
      });
      c.restore();
    }

    function paintStatic() {
      bctx.clearRect(0, 0, base.width, base.height);
      hctx.clearRect(0, 0, hot.width, hot.height);
      strokeTraces(bctx, colors.light ? colors.line : colors.line, colors.light ? 0.9 : 0.75, 1.4);
      strokeTraces(hctx, colors.cu, 0.95, 1.6);
      draw();
    }

    function pointAt(t, d) {
      var c = t.cum, i = 1;
      while (i < c.length - 1 && c[i] < d) i++;
      var seg = c[i] - c[i - 1] || 1, f = clamp((d - c[i - 1]) / seg, 0, 1);
      return [t.p[i - 1][0] + (t.p[i][0] - t.p[i - 1][0]) * f, t.p[i - 1][1] + (t.p[i][1] - t.p[i - 1][1]) * f];
    }

    function draw() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(base, 0, 0);
      if (mouse.on) {
        tctx.globalCompositeOperation = 'source-over';
        tctx.clearRect(0, 0, tmp.width, tmp.height);
        tctx.drawImage(hot, 0, 0);
        tctx.globalCompositeOperation = 'destination-in';
        var g = tctx.createRadialGradient(mouse.x * dpr, mouse.y * dpr, 0, mouse.x * dpr, mouse.y * dpr, 190 * dpr);
        g.addColorStop(0, 'rgba(0,0,0,1)'); g.addColorStop(1, 'rgba(0,0,0,0)');
        tctx.fillStyle = g; tctx.fillRect(0, 0, tmp.width, tmp.height);
        ctx.drawImage(tmp, 0, 0);
      }
      if (reduce) return;
      ctx.save(); ctx.scale(dpr, dpr);
      traces.forEach(function (t) {
        if (!t.pulse) return;
        t.pos += t.speed;
        if (t.pos > t.total + 60) t.pos = -200 - Math.random() * 900;
        if (t.pos < 0) return;
        var col = t.blue ? colors.mask : colors.cu2;
        for (var k = 0; k < 10; k++) {
          var d = t.pos - k * 5;
          if (d < 0 || d > t.total) continue;
          var q = pointAt(t, d);
          ctx.globalAlpha = (1 - k / 10) * (colors.light ? 0.7 : 0.9);
          ctx.fillStyle = col;
          ctx.beginPath(); ctx.arc(q[0], q[1], k === 0 ? 2.4 : 1.8 - k * 0.12, 0, Math.PI * 2); ctx.fill();
        }
        if (t.pos <= t.total) {
          var h = pointAt(t, t.pos);
          ctx.globalAlpha = colors.light ? 0.25 : 0.35;
          var gg = ctx.createRadialGradient(h[0], h[1], 0, h[0], h[1], 14);
          gg.addColorStop(0, col); gg.addColorStop(1, 'rgba(0,0,0,0)');
          ctx.fillStyle = gg; ctx.beginPath(); ctx.arc(h[0], h[1], 14, 0, Math.PI * 2); ctx.fill();
        }
      });
      ctx.restore();
    }

    function loop() {
      draw();
      raf = running ? requestAnimationFrame(loop) : 0;
    }
    function start() { if (!running && !reduce && visible && !document.hidden) { running = true; raf = requestAnimationFrame(loop); } }
    function stop() { running = false; if (raf) cancelAnimationFrame(raf); raf = 0; }

    readColors(); build();
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) { visible = es[0].isIntersecting; visible ? start() : stop(); }).observe(host);
    }
    start();
    document.addEventListener('visibilitychange', function () { document.hidden ? stop() : start(); });
    document.addEventListener('themechange', function () { readColors(); paintStatic(); });
    var rt; window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(build, 200); });
    if (finePointer) {
      host.addEventListener('pointermove', function (e) {
        var r = canvas.getBoundingClientRect();
        mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top; mouse.on = true;
        if (reduce) draw();
      });
      host.addEventListener('pointerleave', function () { mouse.on = false; if (reduce) draw(); });
    }
  });

  /* ---------- Reveal on scroll (auto-tags project-page blocks too) ---------- */
  $$('.ds-head > *, .ds-hero, .prose > section, .prose > .note, .spec, .ds-aside > .btn, .pager a, .result, .gallery .figure, .videos .figure')
    .forEach(function (el) { if (!el.hasAttribute('data-reveal')) el.setAttribute('data-reveal', ''); });
  var revealEls = $$('[data-reveal]');
  revealEls.forEach(function (el) {
    var sibs = Array.prototype.filter.call(el.parentElement.children, function (c) { return c.hasAttribute('data-reveal'); });
    var idx = sibs.indexOf(el);
    if (idx > 0) el.style.setProperty('--d', Math.min(idx * 0.08, 0.4) + 's');
  });

  function countUp(el) {
    var end = parseFloat(el.getAttribute('data-count')), dec = parseInt(el.getAttribute('data-dec') || '0', 10);
    if (reduce) { el.textContent = end.toFixed(dec); return; }
    var t0 = null, dur = 1500;
    function step(ts) {
      if (!t0) t0 = ts;
      var k = clamp((ts - t0) / dur, 0, 1), e = 1 - Math.pow(1 - k, 3);
      el.textContent = (end * e).toFixed(dec);
      if (k < 1) requestAnimationFrame(step);
    }
    el.textContent = (0).toFixed(dec);
    requestAnimationFrame(step);
  }

  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target;
        el.classList.add('is-in');
        $$('[data-count]', el).forEach(countUp);
        $$('.gauge', el).forEach(function (g) { g.classList.add('is-in'); });
        io.unobserve(el);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('is-in'); });
  }

  /* ---------- SVG wires draw themselves in ---------- */
  var drawHosts = $$('.proj-media svg, .figure .media svg').map(function (svg) { return svg.parentElement; });
  drawHosts.forEach(function (h) {
    h.classList.add('draw');
    $$('.dg-cu, .dg-mask, .dg-line', h).forEach(function (p) {
      try { p.style.setProperty('--len', Math.ceil(p.getTotalLength()) + 1); } catch (e) {}
    });
  });
  if ('IntersectionObserver' in window && !reduce) {
    var dio = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) { setTimeout(function () { en.target.classList.add('is-in'); }, 250); dio.unobserve(en.target); } });
    }, { threshold: 0.3 });
    drawHosts.forEach(function (h) { dio.observe(h); });
  } else drawHosts.forEach(function (h) { h.classList.add('is-in'); });

  /* ---------- Pointer effects: spotlight, card glow, tilt, magnetic buttons ---------- */
  if (finePointer && !reduce) {
    var spot = $('.spotlight');
    window.addEventListener('pointermove', function (e) {
      root.classList.add('has-pointer');
      if (spot) { spot.style.setProperty('--cx', e.clientX + 'px'); spot.style.setProperty('--cy', e.clientY + 'px'); }
    }, { passive: true });

    $$('.spot').forEach(function (el) {
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        el.style.setProperty('--mx', (e.clientX - r.left) + 'px');
        el.style.setProperty('--my', (e.clientY - r.top) + 'px');
      });
    });

    $$('.tilt').forEach(function (el) {
      var max = parseFloat(el.getAttribute('data-tilt') || '6');
      el.addEventListener('pointermove', function (e) {
        if (el.hasAttribute('data-reveal') && !el.classList.contains('is-in')) return;
        var r = el.getBoundingClientRect();
        var px = (e.clientX - r.left) / r.width - 0.5, py = (e.clientY - r.top) / r.height - 0.5;
        el.style.transform = 'perspective(1000px) rotateX(' + (-py * max).toFixed(2) + 'deg) rotateY(' + (px * max).toFixed(2) + 'deg) translateY(-4px)';
      });
      el.addEventListener('pointerleave', function () { el.style.transform = ''; });
    });

    $$('.magnetic').forEach(function (el) {
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        var dx = e.clientX - (r.left + r.width / 2), dy = e.clientY - (r.top + r.height / 2);
        el.style.transform = 'translate(' + (dx * 0.18).toFixed(1) + 'px,' + (dy * 0.3).toFixed(1) + 'px)';
      });
      el.addEventListener('pointerleave', function () { el.style.transform = ''; });
    });
  }

  /* ---------- Project filters ---------- */
  var filterBtns = $$('.filters button');
  var grid = $('.projects');
  filterBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var f = btn.getAttribute('data-filter');
      filterBtns.forEach(function (b) { b.classList.toggle('is-on', b === btn); b.setAttribute('aria-pressed', b === btn ? 'true' : 'false'); });
      grid.classList.toggle('is-filtered', f !== 'all');
      var n = 0;
      $$('.proj', grid).forEach(function (card) {
        var show = f === 'all' || (card.getAttribute('data-cat') || '').split(' ').indexOf(f) > -1;
        card.classList.toggle('is-hidden', !show);
        card.classList.remove('is-entering');
        if (show) {
          card.classList.add('is-in');
          void card.offsetWidth;
          card.style.animationDelay = (n++ * 0.06) + 's';
          card.classList.add('is-entering');
        }
      });
    });
  });
  filterBtns.forEach(function (b) { b.setAttribute('aria-pressed', b.classList.contains('is-on') ? 'true' : 'false'); });

  /* ---------- Copy-to-clipboard ---------- */
  $$('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var text = btn.getAttribute('data-copy');
      var done = function () {
        var t = btn.textContent; btn.textContent = 'Copied ✓'; btn.classList.add('is-done');
        setTimeout(function () { btn.textContent = t; btn.classList.remove('is-done'); }, 1500);
      };
      var fallback = function () {
        var target = btn.previousElementSibling; if (!target) return;
        var r = document.createRange(); r.selectNodeContents(target);
        var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
      };
      try { navigator.clipboard.writeText(text).then(done, fallback); } catch (e) { fallback(); }
    });
  });

  /* ---------- Lightbox for project figures ---------- */
  $$('button.zoom').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var img = btn.querySelector('img');
      if (!img) return;
      var box = document.createElement('div');
      box.className = 'lightbox';
      box.setAttribute('role', 'dialog');
      box.setAttribute('aria-modal', 'true');
      box.setAttribute('aria-label', img.alt);
      box.innerHTML = '<div><img alt=""><p></p></div><button type="button">Close</button>';
      box.querySelector('img').src = img.src;
      box.querySelector('img').alt = img.alt;
      box.querySelector('p').textContent = img.alt;
      var prevOverflow = document.body.style.overflow;
      document.body.style.overflow = 'hidden';
      function close() { box.remove(); document.body.style.overflow = prevOverflow; document.removeEventListener('keydown', onKey); btn.focus(); }
      function onKey(e) { if (e.key === 'Escape') close(); }
      box.addEventListener('click', function (e) { if (e.target === box || e.target.tagName === 'BUTTON') close(); });
      document.addEventListener('keydown', onKey);
      document.body.appendChild(box);
      box.querySelector('button').focus();
    });
  });

  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();
