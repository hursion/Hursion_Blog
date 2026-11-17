(function () {
  'use strict';

  var root = document.documentElement;

  /* 深浅色切换 */
  var themeToggle = document.querySelector('.theme-toggle');
  if (themeToggle) {
    themeToggle.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('hb-theme', next); } catch (e) {}
      var meta = document.querySelector('meta[name="theme-color"]');
      if (meta) meta.setAttribute('content', next === 'dark' ? '#15171c' : '#f6f3ec');
    });
  }

  /* 导航状态 / 阅读进度 / 返回顶部 */
  var nav = document.querySelector('.site-nav');
  var backTop = document.querySelector('.back-top');
  var progress = document.querySelector('.progress-bar');
  var articleBody = document.querySelector('.article-content');

  function onScroll() {
    var y = window.scrollY || window.pageYOffset;
    if (nav) nav.classList.toggle('scrolled', y > 8);
    if (backTop) backTop.classList.toggle('show', y > 600);
    if (progress) {
      if (articleBody) {
        var start = articleBody.getBoundingClientRect().top + y - 140;
        var total = articleBody.offsetHeight - window.innerHeight * 0.5;
        var p = Math.min(1, Math.max(0, (y - start) / Math.max(1, total)));
        progress.style.width = (p * 100) + '%';
      } else {
        progress.style.width = '0';
      }
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();

  if (backTop) {
    backTop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* 移动端菜单 */
  var burger = document.querySelector('.nav-toggle');
  var navLinks = document.querySelector('.nav-links');
  if (burger && navLinks) {
    burger.addEventListener('click', function () {
      var open = navLinks.classList.toggle('open');
      burger.classList.toggle('open', open);
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    navLinks.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        navLinks.classList.remove('open');
        burger.classList.remove('open');
        burger.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* 当前页导航高亮 */
  var path = location.pathname;
  document.querySelectorAll('.nav-links a').forEach(function (a) {
    var href = a.getAttribute('href') || '';
    var active;
    if (a.hasAttribute('data-home')) {
      active = path === href || path === href + 'index.html' || path.indexOf(href + 'page/') === 0;
    } else {
      active = path.indexOf(href) === 0;
    }
    if (active) a.classList.add('active');
  });

  /* 滚动入场 */
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.06, rootMargin: '0px 0px -24px 0px' });
    reveals.forEach(function (el, i) {
      el.style.transitionDelay = Math.min((i % 6) * 70, 350) + 'ms';
      io.observe(el);
    });
  } else {
    reveals.forEach(function (el) { el.classList.add('visible'); });
  }

  /* 表格横向滚动容器 */
  document.querySelectorAll('.article-content > table').forEach(function (t) {
    var w = document.createElement('div');
    w.className = 'table-wrap';
    t.parentNode.insertBefore(w, t);
    w.appendChild(t);
  });

  /* 复制文章链接 */
  var copyBtn = document.querySelector('.copy-btn[type="button"]');
  if (copyBtn) {
    var original = copyBtn.innerHTML;
    var timer = null;
    copyBtn.addEventListener('click', function () {
      function done() {
        copyBtn.classList.add('copied');
        copyBtn.innerHTML = '<i class="fa fa-check" aria-hidden="true"></i> 已复制';
        clearTimeout(timer);
        timer = setTimeout(function () {
          copyBtn.classList.remove('copied');
          copyBtn.innerHTML = original;
        }, 2000);
      }
      function fallback() {
        var ta = document.createElement('textarea');
        ta.value = location.href;
        ta.style.position = 'fixed';
        ta.style.opacity = '0';
        document.body.appendChild(ta);
        ta.select();
        try { document.execCommand('copy'); done(); } catch (e) {}
        document.body.removeChild(ta);
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(location.href).then(done, fallback);
      } else {
        fallback();
      }
    });
  }
})();