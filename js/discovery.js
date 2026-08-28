/* Adds discoverable public deep dives without bloating the main story. */
(function () {
  "use strict";

  function ensureStyles() {
    if (document.querySelector('link[href="/css/discovery.css"]')) return;
    var link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = "/css/discovery.css";
    document.head.appendChild(link);
  }

  function ensureNavLinks() {
    var nav = document.querySelector(".nav-links");
    if (!nav) return;
    [
      { href: "/guide/", label: "Field guide" },
      { href: "/oversight/", label: "Oversight" }
    ].forEach(function (item) {
      if (nav.querySelector('a[href="' + item.href + '"]')) return;
      var li = document.createElement("li");
      var a = document.createElement("a");
      a.href = item.href;
      a.textContent = item.label;
      a.setAttribute("data-deep-link", "true");
      li.appendChild(a);
      nav.appendChild(li);
    });
  }

  function refreshHomepageMilestones() {
    if (!(location.pathname === "/" || location.pathname === "/index.html")) return;
    var status = document.getElementById("status");
    if (!status) return;

    var cards = status.querySelectorAll(".status-card");
    if (cards.length) {
      var charged = cards[0];
      var value = charged.querySelector(".status-value");
      var label = charged.querySelector(".status-label");
      var detail = charged.querySelector(".status-detail");
      var source = charged.querySelector("a");
      if (value) value.textContent = "78";
      if (label) label.textContent = "Feeding Our Future defendants charged by Nov. 24, 2025";
      if (detail) detail.textContent = "DOJ identified Abdirashid Bixi Dool as the 78th defendant charged. Charges remain allegations until resolved.";
      if (source) source.href = "https://www.justice.gov/usao-mn/pr/78th-defendant-charged-feeding-our-future-fraud-scheme";
    }

    document.querySelectorAll(".story-step p").forEach(function (p) {
      if (p.textContent.indexOf("77 defendants had been charged") !== -1) {
        p.textContent = p.textContent.replace("77 defendants had been charged", "78 defendants had been charged");
      }
    });

    var latest = status.querySelector(".latest-bar");
    if (latest && !latest.querySelector('a[href="/status/"]')) {
      var full = document.createElement("a");
      full.href = "/status/";
      full.textContent = "Open the current status desk →";
      latest.appendChild(full);
    }
  }

  function addHomepageDiscovery() {
    if (!(location.pathname === "/" || location.pathname === "/index.html")) return;
    if (document.querySelector(".deep-discovery")) return;
    var story = document.getElementById("story");
    if (!story || !story.parentNode) return;

    var section = document.createElement("section");
    section.className = "orientation deep-discovery";
    section.setAttribute("aria-label", "Deep dives");
    section.innerHTML = [
      '<div class="wrap orientation-grid">',
      '  <div class="orientation-copy reveal">',
      '    <span class="chapter-label is-purple">Go deeper without getting lost</span>',
      '    <h2>Need the current outcomes, names, institutions or oversight story?</h2>',
      '    <p>The homepage gives you the arc. The deeper desks separate what is happening now from the original charging record, decode the institutions and legal language, and examine what Minnesota auditors and agencies say went wrong.</p>',
      '  </div>',
      '  <div class="deep-discovery-actions reveal d1">',
      '    <a class="deep-discovery-link is-purple" href="/status/"><span>Current status</span><strong>Where do the cases actually stand now?</strong><small>78 charged. 68 convicted. 26 sentenced in Feeding Our Future — each with its own date and source — plus current HSS outcomes.</small></a>',
      '    <a class="deep-discovery-link" href="/guide/"><span>Field guide</span><strong>Who is who — and what do all these words mean?</strong><small>Agencies, organizations, court terms, money labels and a global-reader system map.</small></a>',
      '    <a class="deep-discovery-link is-gold" href="/oversight/"><span>Oversight</span><strong>The fraud story is only half the story.</strong><small>Warnings, auditor findings, the agency response, HSS vulnerabilities and reforms.</small></a>',
      '  </div>',
      '</div>'
    ].join("");
    story.parentNode.insertBefore(section, story);
  }

  ensureStyles();
  ensureNavLinks();
  refreshHomepageMilestones();
  addHomepageDiscovery();
})();
