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
    nav.querySelectorAll(".nav-panel a").forEach(function (a) {
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

  var density = document.getElementById("density-toggle");
  if (density) {
    var paper = false;
    try { paper = localStorage.getItem("mnpeace-record-density") === "paper"; } catch (err) { paper = false; }
    function applyDensity() {
      document.body.classList.toggle("is-paper", paper);
      density.setAttribute("aria-pressed", paper ? "true" : "false");
    }
    applyDensity();
    density.addEventListener("click", function () {
      paper = !paper;
      try { localStorage.setItem("mnpeace-record-density", paper ? "paper" : "dark"); } catch (err) { /* ignore */ }
      applyDensity();
    });
  }

  var stats = window.__CORPUS_STATS__;
  function countUp(el, target) {
    if (reduce) {
      el.textContent = String(target);
      return;
    }
    var t0 = performance.now();
    var dur = 900;
    function tick(now) {
      var p = Math.min(1, (now - t0) / dur);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = String(Math.round(target * eased));
      if (p < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }
  function fillStats() {
    if (!stats) return;
    ["documents", "claims", "mapped_cases", "gaps"].forEach(function (key) {
      var el = document.querySelector('[data-stat="' + key + '"]');
      if (el && stats[key] != null) countUp(el, Number(stats[key]));
    });
  }
  var statsRoot = document.getElementById("stats");
  if (statsRoot && stats && "IntersectionObserver" in window && !reduce) {
    var counted = false;
    var so = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting && !counted) {
          counted = true;
          fillStats();
          so.disconnect();
        }
      });
    }, { threshold: 0.35 });
    so.observe(statsRoot);
  } else {
    fillStats();
  }

  var progress = document.querySelector(".read-progress > span");
  var supportsScrollTimeline = typeof CSS !== "undefined" && CSS.supports && CSS.supports("animation-timeline: scroll()");
  var rail = document.querySelector(".chapter-rail");
  var railLinks = rail ? Array.prototype.slice.call(rail.querySelectorAll("a[data-rail]")) : [];
  var railSections = railLinks.map(function (a) {
    return document.getElementById(a.getAttribute("data-rail"));
  });

  function setRailActive(id) {
    railLinks.forEach(function (a) {
      a.classList.toggle("is-active", a.getAttribute("data-rail") === id);
    });
  }

  function onPageScroll() {
    if (progress && !supportsScrollTimeline && !reduce) {
      var doc = document.documentElement;
      var max = doc.scrollHeight - doc.clientHeight;
      var p = max > 0 ? window.scrollY / max : 0;
      progress.style.transform = "scaleX(" + p + ")";
    }
    if (!railLinks.length) return;
    var marker = window.scrollY + window.innerHeight * 0.28;
    var current = railLinks[0] && railLinks[0].getAttribute("data-rail");
    for (var i = 0; i < railSections.length; i++) {
      var sec = railSections[i];
      if (sec && sec.offsetTop <= marker) current = railLinks[i].getAttribute("data-rail");
    }
    setRailActive(current);
  }
  onPageScroll();
  window.addEventListener("scroll", onPageScroll, { passive: true });

  var canvas = document.getElementById("aurora");
  var motionMq = window.matchMedia("(prefers-reduced-motion: reduce)");
  if (!canvas || reduce || motionMq.matches) {
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

  var sparks = [];

  function build() {
    var n = w < 700 ? 42 : 78;
    strands = [];
    var colors = [
      "rgba(34, 211, 238, 0.55)",
      "rgba(103, 232, 249, 0.45)",
      "rgba(245, 158, 11, 0.42)",
      "rgba(34, 211, 238, 0.28)",
      "rgba(168, 85, 247, 0.18)"
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
    sparks = [];
    var pn = w < 700 ? 24 : 52;
    for (var p = 0; p < pn; p++) {
      sparks.push({
        x: Math.random() * w,
        y: Math.random() * h,
        vx: (Math.random() - 0.5) * 12,
        vy: -8 - Math.random() * 14,
        r: Math.random() * 1.3 + 0.25,
        gold: Math.random() > 0.72
      });
    }
  }

  function draw(now) {
    if (!running) return;
    var t = (now - start) / 1000;
    ctx.clearRect(0, 0, w, h);

    var g = ctx.createRadialGradient(w * 0.5, h * 0.38, 0, w * 0.5, h * 0.38, h * 0.78);
    g.addColorStop(0, "rgba(34, 211, 238, 0.08)");
    g.addColorStop(0.55, "rgba(168, 85, 247, 0.04)");
    g.addColorStop(1, "rgba(0,0,0,0)");
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, w, h);

    var g2 = ctx.createRadialGradient(w * 0.72, h * 0.7, 0, w * 0.72, h * 0.7, h * 0.45);
    g2.addColorStop(0, "rgba(245, 158, 11, 0.06)");
    g2.addColorStop(1, "rgba(0,0,0,0)");
    ctx.fillStyle = g2;
    ctx.fillRect(0, 0, w, h);

    ctx.lineWidth = 0.6;
    for (var a = 0; a < stars.length; a++) {
      for (var b = a + 1; b < stars.length; b++) {
        var dx = stars[a].x - stars[b].x;
        var dy = stars[a].y - stars[b].y;
        var dist = Math.hypot(dx, dy);
        if (dist < 88) {
          ctx.strokeStyle = "rgba(34, 211, 238," + (0.09 * (1 - dist / 88)) + ")";
          ctx.beginPath();
          ctx.moveTo(stars[a].x, stars[a].y);
          ctx.lineTo(stars[b].x, stars[b].y);
          ctx.stroke();
        }
      }
    }
    for (var s = 0; s < stars.length; s++) {
      var st = stars[s];
      var tw = 0.55 + 0.45 * Math.sin(t * (0.6 + st.tw) + st.x);
      ctx.fillStyle = "rgba(248,250,252," + (st.a * tw) + ")";
      ctx.beginPath();
      ctx.arc(st.x, st.y, st.r, 0, Math.PI * 2);
      ctx.fill();
    }

    for (var sp = 0; sp < sparks.length; sp++) {
      var spark = sparks[sp];
      spark.x += spark.vx * 0.016;
      spark.y += spark.vy * 0.016;
      if (spark.y < -8) spark.y = h + 8;
      if (spark.x < -8) spark.x = w + 8;
      if (spark.x > w + 8) spark.x = -8;
      ctx.fillStyle = spark.gold ? "rgba(245,158,11,0.55)" : "rgba(34,211,238,0.5)";
      ctx.beginPath();
      ctx.arc(spark.x, spark.y, spark.r, 0, Math.PI * 2);
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

  if (motionMq.addEventListener) {
    motionMq.addEventListener("change", function (e) {
      if (e.matches) {
        stop();
        canvas.style.display = "none";
      } else {
        canvas.style.display = "";
        startLoop();
      }
    });
  }

  window.addEventListener("resize", resize, { passive: true });
  resize();
  raf = requestAnimationFrame(draw);
})();
