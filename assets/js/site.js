// Zaid Saifan Portfolio — small enhancements only; the page works without this file.
(function () {
  // Headshot: show photo if assets/img/zaid.jpg exists, otherwise keep the initials.
  document.querySelectorAll('.avatar img').forEach(function (img) {
    function hide() { img.remove(); }
    if (img.complete && img.naturalWidth === 0) hide();
    img.addEventListener('error', hide);
  });

  // Copy-to-clipboard buttons
  document.querySelectorAll('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var text = btn.getAttribute('data-copy');
      var done = function () { var t = btn.textContent; btn.textContent = 'Copied'; setTimeout(function () { btn.textContent = t; }, 1400); };
      try {
        navigator.clipboard.writeText(text).then(done, function () { selectFallback(btn); });
      } catch (e) { selectFallback(btn); }
    });
  });
  function selectFallback(btn) {
    var target = btn.previousElementSibling;
    if (!target) return;
    var r = document.createRange(); r.selectNodeContents(target);
    var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
  }

  // Lightbox for project figures
  document.querySelectorAll('button.zoom').forEach(function (btn) {
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
      function close() { box.remove(); document.removeEventListener('keydown', onKey); btn.focus(); }
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
