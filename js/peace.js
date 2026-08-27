/* MN Peace public face. Canvas aurora degrades; reduced-motion skips spectacle. */
(function () {
  "use strict";

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var nav = document.getElementById("nav");
  var toggle = document.querySelector(".nav-toggle");

  function onScroll() {
    if (!nav) return;
    nav.classList.toggle("is-scrolled", window.scrollY > 48);
  }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = !nav.classList.contains("is-open");
      nav.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    });
    nav.querySelectorAll(".nav-links a, .nav-cta").forEach(function (a) {
      a.addEventListener("click", function () {
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.setAttribute("aria-label", "Open menu");
      });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) {
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.focus();
      }
    });
  }

  var reveals = document.querySelectorAll(".reveal");
  if (reduce) {
    reveals.forEach(function (el) { el.classList.add("is-in"); });
  } else if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-in");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: "0px 0px -24px 0px" });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-in"); });
  }

  var stats = window.__CORPUS_STATS__;
  if (stats) {
    ["documents", "claims", "mapped_cases", "gaps"].forEach(function (key) {
      var el = document.querySelector('[data-stat="' + key + '"]');
      if (el && stats[key] != null) el.textContent = String(stats[key]);
    });
  }

  var canvas = document.getElementById("aurora");
  if (!canvas || reduce || window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    return;
  }

  var ctx = canvas.getContext("2d", { alpha: true });
  if (!ctx) return;

  var dpr = Math.min(window.devicePixelRatio || 1, 2);
  var w = 0;
  var h = 0;
  var running = true;
  var start = performance.now();
  var strands = [];
  var stars = [];
  var raf = 0;

  function bezier(p0, p1, p2, p3, t) {
    var u = 1 - t;
    var tt = t * t;
    var uu = u * u;
    var uuu = uu * u;
    var ttt = tt * t;
    return {
      x: uuu * p0.x + 3 * uu * t * p1.x + 3 * u * tt * p2.x + ttt * p3.x,
      y: uuu * p0.y + 3 * uu * t * p1.y + 3 * u * tt * p2.y + ttt * p3.y
    };
  }

  function tangent(p0, p1, p2, p3, t) {
    var u = 1 - t;
    return {
      x: 3 * u * u * (p1.x - p0.x) + 6 * u * t * (p2.x - p1.x) + 3 * t * t * (p3.x - p2.x),
      y: 3 * u * u * (p1.y - p0.y) + 6 * u * t * (p2.y - p1.y) + 3 * t * t * (p3.y - p2.y)
    };
  }

  function resize() {
    var rect = canvas.getBoundingClientRect();
    w = Math.max(1, Math.floor(rect.width));
    h = Math.max(1, Math.floor(rect.height));
    canvas.width = Math.floor(w * dpr);
    canvas.height = Math.floor(h * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    build();
  }

  function riverCtrl() {
    return {
      p0: { x: w * 0.48, y: -h * 0.08 },
      p1: { x: w * 0.18, y: h * 0.32 },
      p2: { x: w * 0.78, y: h * 0.58 },
      p3: { x: w * 0.96, y: h * 1.08 }
    };
  }

  function build() {
    var n = w < 700 ? 42 : 78;
    strands = [];
    var colors = [
      "rgba(6, 182, 212, 0.55)",
      "rgba(103, 232, 249, 0.45)",
      "rgba(245, 158, 11, 0.42)",
      "rgba(6, 182, 212, 0.28)",
      "rgba(168, 85, 247, 0.16)"
    ];
    for (var i = 0; i < n; i++) {
      strands.push({
        offset: (i / n - 0.5) * (w * 0.22),
        width: 0.6 + Math.random() * 1.6,
        color: colors[i % colors.length],
        speed: 0.12 + Math.random() * 0.25,
        phase: Math.random() * Math.PI * 2
      });
    }
    stars = [];
    var sn = w < 700 ? 40 : 90;
    for (var s = 0; s < sn; s++) {
      stars.push({
        x: Math.random() * w,
        y: Math.random() * h,
        r: Math.random() * 1.1 + 0.2,
        a: 0.15 + Math.random() * 0.55,
        tw: Math.random() * 2
      });
    }
  }

  function draw(now) {
    if (!running) return;
    var t = (now - start) / 1000;
    ctx.clearRect(0, 0, w, h);

    var g = ctx.createRadialGradient(w * 0.7, h * 0.2, 0, w * 0.7, h * 0.2, h * 0.7);
    g.addColorStop(0, "rgba(6, 182, 212, 0.07)");
    g.addColorStop(1, "rgba(0,0,0,0)");
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, w, h);

    for (var s = 0; s < stars.length; s++) {
      var st = stars[s];
      var tw = 0.55 + 0.45 * Math.sin(t * (0.6 + st.tw) + st.x);
      ctx.fillStyle = "rgba(248,250,252," + (st.a * tw) + ")";
      ctx.beginPath();
      ctx.arc(st.x, st.y, st.r, 0, Math.PI * 2);
      ctx.fill();
    }

    var c = riverCtrl();
    for (var i = 0; i < strands.length; i++) {
      var str = strands[i];
      ctx.beginPath();
      var steps = 36;
      for (var k = 0; k <= steps; k++) {
        var u = k / steps;
        var p = bezier(c.p0, c.p1, c.p2, c.p3, u);
        var tan = tangent(c.p0, c.p1, c.p2, c.p3, u);
        var len = Math.hypot(tan.x, tan.y) || 1;
        var nx = -tan.y / len;
        var ny = tan.x / len;
        var wobble = Math.sin(u * 10 + t * str.speed + str.phase) * 8;
        var x = p.x + nx * (str.offset + wobble);
        var y = p.y + ny * (str.offset * 0.35 + wobble * 0.25);
        if (k === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.strokeStyle = str.color;
      ctx.lineWidth = str.width;
      ctx.lineCap = "round";
      ctx.stroke();
    }

    raf = requestAnimationFrame(draw);
  }

  function stop() {
    running = false;
    if (raf) cancelAnimationFrame(raf);
  }

  function startLoop() {
    if (running) return;
    running = true;
    raf = requestAnimationFrame(draw);
  }

  document.addEventListener("visibilitychange", function () {
    if (document.hidden) stop();
    else startLoop();
  });

  window.addEventListener("resize", resize, { passive: true });
  resize();
  raf = requestAnimationFrame(draw);
})();
