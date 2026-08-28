/* Adds discoverable links to the Field Guide and Oversight pages without bloating the main story. */
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
      '    <h2>Need the names, institutions or oversight story?</h2>',
      '    <p>The homepage gives you the arc. Two deeper guides explain who does what, how U.S. court language works, what the money labels mean, what Minnesota auditors found, how agencies responded, and what changed afterward.</p>',
      '  </div>',
      '  <div class="deep-discovery-actions reveal d1">',
      '    <a class="deep-discovery-link" href="/guide/"><span>Field guide</span><strong>Who is who — and what do all these words mean?</strong><small>Agencies, organizations, court terms, money labels and a global-reader system map.</small></a>',
      '    <a class="deep-discovery-link is-gold" href="/oversight/"><span>Oversight</span><strong>The fraud story is only half the story.</strong><small>Warnings, auditor findings, the agency response, HSS vulnerabilities and reforms.</small></a>',
      '  </div>',
      '</div>'
    ].join("");
    story.parentNode.insertBefore(section, story);
  }

  ensureStyles();
  ensureNavLinks();
  addHomepageDiscovery();
})();
