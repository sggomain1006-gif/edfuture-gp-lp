/* グローバルプロジェクト LP / 依存ゼロJS */
(function () {
  'use strict';

  /* --- タブレットはPCレイアウトを縮小表示（原本と同じ viewport 差し替え方式） ---
     SP(≤480px)とPC(≥1100px)の2ブレークポイント設計のため、
     中間幅の端末には width=1200 を指定して横スクロールを防ぐ。 */
  (function () {
    var mv = document.querySelector('meta[name="viewport"]');
    if (!mv) return;
    var ua = navigator.userAgent;
    var isTablet = /iPad/.test(ua)
      || (/Android/.test(ua) && !/Mobile/.test(ua))
      || (/Macintosh/.test(ua) && navigator.maxTouchPoints > 1); /* iPadOS 13+ */
    if (isTablet || (window.innerWidth > 480 && window.innerWidth < 1100)) {
      mv.setAttribute('content', 'width=1200');
    }
  })();

  /* --- クリックで動画を読み込んで再生（初期表示はポスター画像のみ） --- */
  document.querySelectorAll('.js-video').forEach(function (box) {
    var btn = box.querySelector('.video_btn');
    if (!btn) return;
    btn.addEventListener('click', function () {
      if (box.classList.contains('is-playing')) return;
      var v = document.createElement('video');
      v.src = box.dataset.src;
      v.controls = true;
      v.playsInline = true;
      v.preload = 'auto';
      box.appendChild(v);
      box.classList.add('is-playing');
      v.play().catch(function () { /* 自動再生が拒否されたら操作バーから再生 */ });
    });
  });

  /* --- 読み込み後のKVアニメーション --- */
  function markLoaded() { document.body.classList.add('loaded'); }
  if (document.readyState === 'complete') { markLoaded(); }
  else { window.addEventListener('load', markLoaded); }
  // 画像待ちが長引いた場合の保険
  setTimeout(markLoaded, 2500);

  /* --- FAQアコーディオン --- */
  document.querySelectorAll('#s_faq .faq_list > li').forEach(function (li) {
    var btn = li.querySelector('.qu button');
    if (!btn) return;
    btn.addEventListener('click', function () {
      var open = li.classList.toggle('on');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });

  /* --- ページ内アンカーのスムーススクロール --- */
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var id = a.getAttribute('href');
      if (id === '#' || id.length < 2) return;
      var target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      window.scrollTo({ top: target.getBoundingClientRect().top + window.pageYOffset - 20, behavior: reduce ? 'auto' : 'smooth' });
    });
  });

  /* --- SPで応募セクションに来たら固定ボタンを隠す --- */
  var entry = document.getElementById('s_entry');
  if (entry && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        document.body.classList.toggle('btn_fix_off', en.isIntersecting);
      });
    }, { rootMargin: '-20% 0px -20% 0px' }).observe(entry);
  }
})();
