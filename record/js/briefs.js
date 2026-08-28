/* MN Peace — publication layer for The Record.
   The corpus stays machine-precise; this layer turns case routes into reader-first briefs. */
(function () {
  "use strict";

  const CORPUS = window.__CORPUS__;
  const app = document.getElementById("app");
  if (!CORPUS || !app) return;

  const KIND_LABEL = {
    amount_billed: "Billed",
    amount_claimed: "Claimed",
    amount_paid: "Paid / received",
    amount_received: "Paid / received",
    alleged_loss: "Alleged loss",
    program_spend: "Program payout (background)",
    proven_loss: "Proven loss",
    fraud_estimate: "Estimate (not proven)",
    unknown_or_disputed: "As filed (not a loss figure)",
  };

  const INSTRUMENT_LABEL = {
    indictment: "Indictment",
    superseding_indictment: "Superseding indictment",
    felony_information: "Felony information",
  };

  const PUBLISHED_PDF = {
    "bock-22cr223": "/record/documents/22-cr-00223-ecf1.pdf",
    "farah-22cr124": "/record/documents/22-cr-00124-ecf57.pdf",
    "mohamed-24cr015": "/record/documents/24-cr-00015-ecf1.pdf",
    "aden-25cr349": "/record/documents/25-cr-00349-ecf1.pdf",
    "falade-25cr351": "/record/documents/25-cr-00351-ecf1.pdf",
    "anwar-adow-25cr353": "/record/documents/25-cr-00353-ecf1.pdf",
    "hussein-25cr479": "/record/documents/25-cr-00479-ecf1.pdf",
    "sallah-25cr482": "/record/documents/25-cr-00482-ecf1.pdf",
  };

  const RELATED_PDF = {
    "farah-22cr124": [
      { href: "/record/documents/22-cr-00124-ecf22.pdf", label: "Related charging document" },
    ],
  };

  function esc(value) {
    return String(value == null ? "" : value).replace(/[&<>"']/g, function (ch) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch];
    });
  }

  function civic(value) {
    return String(value == null ? "" : value)
      .replace(/amount_billed/g, "billed")
      .replace(/amount_claimed/g, "claimed")
      .replace(/amount_paid/g, "paid")
      .replace(/amount_received/g, "received")
      .replace(/alleged_loss/g, "alleged loss")
      .replace(/proven_loss/g, "proven loss")
      .replace(/program_spend/g, "program payout")
      .replace(/fraud_estimate/g, "estimate")
      .replace(/metric_type/g, "kind")
      .replace(/overlap_group_id/g, "same dollars")
      .replace(/CHARGED_ALLEGED/g, "charged in this filing")
      .replace(/Do not mark ADJUDICATED\.?/gi, "")
      .replace(/\bRECAP\b/g, "the public file")
      .replace(/[ \t]+/g, " ")
      .trim();
  }

  function fmtUsd(value, exact) {
    if (value == null || value === "") return "—";
    const n = Number(value);
    if (!Number.isFinite(n)) return esc(value);
    const digits = exact === "exact" && Math.abs(n) < 1e7 ? 2 : 0;
    const formatted = new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      maximumFractionDigits: digits,
      minimumFractionDigits: 0,
    }).format(n);
    return exact === "approximate" ? "about " + formatted : formatted;
  }

  function kindLabel(raw) {
    return KIND_LABEL[raw] || civic(raw).replace(/_/g, " ");
  }

  function instrumentLabel(raw) {
    return INSTRUMENT_LABEL[raw] || civic(raw).replace(/_/g, " ");
  }

  function chip(text, extra) {
    if (!text) return "";
    return `<span class="chip ${extra || ""}">${esc(text)}</span>`;
  }

  function familyById(id) {
    return (CORPUS.families || []).find(function (f) { return f.id === id; }) || null;
  }

  function caseById(id) {
    return (CORPUS.cases || []).find(function (c) { return c.id === id; }) || null;
  }

  function claimById(id) {
    return (CORPUS.claims || []).find(function (c) { return c.claim_id === id; }) || null;
  }

  function entityById(id) {
    return (CORPUS.entities || []).find(function (e) { return e.entity_id === id; }) || null;
  }

  function primaryClaims(c) {
    return (c.primary_claim_ids || []).map(claimById).filter(Boolean);
  }

  function allClaims(c) {
    return (c.claim_ids || []).map(claimById).filter(Boolean);
  }

  function summaryFor(c) {
    const first = primaryClaims(c)[0];
    if (first && first.claim_text) return civic(first.claim_text);
    if (c.gap) return "A docket is known, but the charging document is not yet available in this site's published source set.";
    if (c.caption) return civic(c.caption);
    return "Open the case file for the charging record and its supporting sources.";
  }

  function sourceById(id) {
    return CORPUS.sources && CORPUS.sources[id] ? CORPUS.sources[id] : null;
  }

  function sourceList(ids) {
    return (ids || []).map(function (id) {
      const src = sourceById(id);
      if (!src) return "";
      const title = src.title || "Source";
      const links = [];
      if (src.canonical_url) links.push(`<a href="${esc(src.canonical_url)}">${esc(title)}</a>`);
      else links.push(esc(title));
      if (src.archive_url) links.push(`<a href="${esc(src.archive_url)}">Archived copy</a>`);
      return `<li>${links.join(" · ")}</li>`;
    }).filter(Boolean).join("");
  }

  function overlapWarning(amounts) {
    const seen = Object.create(null);
    let shared = false;
    (amounts || []).forEach(function (a) {
      if (!a || !a.overlap_group_id) return;
      if (seen[a.overlap_group_id]) shared = true;
      seen[a.overlap_group_id] = true;
    });
    return shared ? `<p class="brief-caution">Some figures restate the same dollars. Read the labels; do not add them.</p>` : "";
  }

  function primaryMoney(c) {
    const amounts = (c.primary_amounts || []).filter(function (a) { return a && a.value != null; });
    if (!amounts.length) {
      return `<p class="brief-muted">This filing does not isolate a single billed, paid or alleged-loss figure on its face.</p>`;
    }
    return `<div class="brief-money-list">${amounts.map(function (a) {
      return `<div class="brief-money-item"><strong>${esc(fmtUsd(a.value, a.exact_or_approximate))}</strong><span>${esc(kindLabel(a.metric_type))}</span></div>`;
    }).join("")}</div>${overlapWarning(amounts)}`;
  }

  function pdfLinks(c, compact) {
    const main = PUBLISHED_PDF[c.id];
    const related = RELATED_PDF[c.id] || [];
    if (!main && !related.length) return "";
    const cls = compact ? "brief-source-links compact" : "brief-source-links";
    return `<div class="${cls}">${main ? `<a class="pdf-link" href="${esc(main)}">Open the primary filing (PDF)</a>` : ""}${related.map(function (r) {
      return `<a class="pdf-link pdf-link-quiet" href="${esc(r.href)}">${esc(r.label)}</a>`;
    }).join("")}</div>`;
  }

  function filterChips(active) {
    const options = [
      { id: "", href: "#/cases", label: "All case files" },
      { id: "feeding-our-future", href: "#/cases/family/feeding-our-future", label: "Child nutrition" },
      { id: "hss", href: "#/cases/family/hss", label: "Housing services" },
    ];
    return `<div class="case-filters" role="navigation" aria-label="Filter case files">${options.map(function (o) {
      return `<a class="filter-chip${o.id === (active || "") ? " is-on" : ""}" href="${o.href}"${o.id === (active || "") ? ' aria-current="true"' : ""}>${o.label}</a>`;
    }).join("")}</div>`;
  }

  function caseCard(c) {
    const family = familyById(c.family);
    const defendants = c.defendants || [];
    const summary = summaryFor(c);
    const filed = c.filed ? `Filed ${esc(c.filed)}` : "Filing date not shown";
    return `
      <article class="brief-case-card${c.gap ? " is-source-pending" : ""}">
        <p class="brief-eyebrow">${esc(family ? family.name : c.family)} · ${esc(instrumentLabel(c.instrument))}</p>
        <h3><a href="#/cases/${esc(c.id)}">${esc(c.short_name || c.caption)}</a></h3>
        <p class="brief-case-summary">${esc(summary.length > 320 ? summary.slice(0, 317) + "…" : summary)}</p>
        <div class="chips">
          ${c.gap ? chip("Source file pending", "gap") : chip("Charging record")}
          ${c.count_label && !c.gap ? chip(civic(c.count_label)) : ""}
        </div>
        <div class="brief-case-meta">
          <span>${filed}</span>
          <span>${defendants.length ? defendants.length + (defendants.length === 1 ? " named defendant" : " named defendants") : "Defendants not expanded"}</span>
          <span>${esc(c.docket || "")}</span>
        </div>
        ${c.gap ? "" : `<div class="brief-card-money">${primaryMoney(c)}</div>`}
        <a class="brief-open" href="#/cases/${esc(c.id)}">Open case brief →</a>
      </article>`;
  }

  function renderCases(familyId) {
    const family = familyById(familyId);
    const unknown = familyId && !family;
    const groups = [
      {
        id: "feeding-our-future",
        heading: "Feeding Our Future / child nutrition",
        intro: "Federal child-nutrition charging records tied to the Feeding Our Future investigation and related meal-site activity. Each filing keeps its own defendants, charges and dollar figures.",
      },
      {
        id: "hss",
        heading: "Housing Stabilization Services",
        intro: "Federal charging records tied to Minnesota Medicaid's former Housing Stabilization Services benefit. These cases are separate from the child-nutrition prosecutions.",
      },
    ];
    const visible = groups.filter(function (g) { return !familyId || g.id === familyId; });
    document.title = (family ? family.name + " — Case files" : "Case files") + " — The Record";
    app.innerHTML = `
      <div class="brief-cases-root">
        <span class="record-kicker">// Case files</span>
        <h2>Start with a case, not a data table.</h2>
        <p class="lede">Each brief keeps the allegation, people, organizations, money, charges and source documents together. Open the PDF whenever you want the filing itself.</p>
        <p class="brief-context-link">New to the larger story? <a href="/#story">Read the 90-second Minnesota overview first.</a></p>
        ${filterChips(familyId || "")}
        ${unknown ? `<div class="not-found"><p>No investigation family named ${esc(familyId)}.</p></div>` : ""}
        ${visible.map(function (g) {
          const cases = (CORPUS.cases || []).filter(function (c) { return c.family === g.id; });
          return `<section class="brief-family"><div class="brief-family-head"><h3>${esc(g.heading)}</h3><p>${esc(g.intro)}</p></div><div class="brief-card-grid">${cases.map(caseCard).join("")}</div></section>`;
        }).join("")}
      </div>`;
  }

  function defendantsHtml(c) {
    const list = c.defendants || [];
    if (!list.length) return `<p class="brief-muted">No defendant names are expanded in this published card.</p>`;
    return `<ul class="brief-name-list">${list.map(function (name) { return `<li>${esc(name)}</li>`; }).join("")}</ul>`;
  }

  function providersHtml(c) {
    const providers = c.providers || [];
    if (!providers.length) return `<p class="brief-muted">No provider organizations are expanded on this published card.</p>`;
    return `<div class="brief-org-list">${providers.map(function (p) {
      const ent = p.entity_id ? entityById(p.entity_id) : null;
      const name = ent ? `<a href="#/entities/${esc(p.entity_id)}">${esc(p.name)}</a>` : esc(p.name || "");
      return `<div><strong>${name}</strong>${p.role_on_face ? `<span>${esc(civic(p.role_on_face))}</span>` : ""}</div>`;
    }).join("")}</div>`;
  }

  function countsHtml(c) {
    const rows = c.counts || [];
    if (!rows.length) return `<p class="brief-muted">${c.gap ? "The charging document is not available here, so counts are not expanded." : "No expanded count table is published for this filing."}</p>`;
    return `<div class="brief-table-wrap"><table><thead><tr><th>Count</th><th>Charge</th><th>Date / transaction</th><th>Named defendants</th></tr></thead><tbody>${rows.map(function (r) {
      const dateNotes = [r.date, r.wire || r.notes].filter(Boolean).join(" · ");
      return `<tr><td>${esc(r.count)}</td><td>${esc(r.title || "")}${r.statute ? `<div class="small muted">${esc(r.statute)}</div>` : ""}</td><td>${esc(civic(dateNotes))}</td><td class="small">${esc((r.named_defendants || []).join("; "))}</td></tr>`;
    }).join("")}</tbody></table></div>`;
  }

  function extractedMoneyHtml(c) {
    const amounts = (c.extract_amounts || []).filter(function (a) { return a && a.value != null; });
    if (!amounts.length) return "";
    return `<h4>Other figures appearing in the filing</h4>${overlapWarning(amounts)}<div class="brief-table-wrap"><table><thead><tr><th>Amount</th><th>What it measures</th><th>Context</th><th>Notes</th></tr></thead><tbody>${amounts.map(function (a) {
      return `<tr><td class="numcell">${esc(fmtUsd(a.value, a.exact_or_approximate))}</td><td>${esc(kindLabel(a.metric_type))}</td><td>${esc(a.provider || a.period || a.period_start || "")}</td><td class="small">${esc(civic(a.notes || a.quote || ""))}</td></tr>`;
    }).join("")}</tbody></table></div>`;
  }

  function statewideHtml(c) {
    if (!c.statewide_recital) return "";
    const r = c.statewide_recital;
    return `<div class="brief-background-box"><h4>Program-wide background quoted in this filing</h4><p>These are program-level payouts recited in the charging document. They are not automatically this case's alleged loss.</p><div class="brief-table-wrap"><table><thead><tr><th>Period</th><th>Amount</th><th>Meaning</th></tr></thead><tbody>${(r.rows || []).map(function (row) {
      return `<tr><td>${esc(row.period)}</td><td class="numcell">${esc(fmtUsd(row.value, row.exact_or_approximate))}</td><td>${esc(kindLabel(r.metric_type))}</td></tr>`;
    }).join("")}</tbody></table></div></div>`;
  }

  function relatedHtml(c) {
    const related = c.related_instruments || [];
    if (!related.length) return "";
    return `<div class="brief-related"><h4>Related filing</h4>${related.map(function (r) {
      return `<p>${esc(instrumentLabel(r.instrument) || r.instrument)}${r.ecf ? ` · ECF ${esc(r.ecf)}` : ""}${r.note ? ` — ${esc(civic(r.note))}` : ""}</p>`;
    }).join("")}</div>`;
  }

  function renderCase(c) {
    const family = familyById(c.family);
    const claims = primaryClaims(c);
    const all = allClaims(c);
    const primaryIds = Object.create(null);
    (c.primary_claim_ids || []).forEach(function (id) { primaryIds[id] = true; });
    const extraClaims = all.filter(function (cl) { return !primaryIds[cl.claim_id]; });
    const filedMeta = [c.docket, instrumentLabel(c.instrument), c.filed ? "Filed " + c.filed : null, c.pages ? c.pages + " pages" : null].filter(Boolean).join(" · ");
    const scope = c.gap
      ? "This page preserves the known docket entry while the charging document remains absent from this site's published source set."
      : `This brief summarizes the ${instrumentLabel(c.instrument).toLowerCase()} filed${c.filed ? " " + c.filed : " in this docket"}. It is a filing brief, not a live docket-status page; later pleas, verdicts, dismissals or sentences require later court records.`;

    document.title = (c.short_name || "Case") + " — The Record";
    app.innerHTML = `
      <article class="brief-case-root">
        <p class="meta"><a href="#/cases">Case files</a> / ${family ? `<a href="#/cases/family/${esc(family.id)}">${esc(family.name)}</a> / ` : ""}${esc(c.docket || "")}</p>
        <div class="brief-case-hero">
          <div>
            <span class="record-kicker">// Charging-file brief</span>
            <h2>${esc(c.caption || c.short_name)}</h2>
            <p class="brief-case-deck">${esc(summaryFor(c))}</p>
            <div class="chips">${chip(instrumentLabel(c.instrument))}${c.gap ? chip("Source file pending", "gap") : chip("Primary-source brief")}${c.count_label && !c.gap ? chip(civic(c.count_label)) : ""}</div>
          </div>
          <div class="brief-file-meta"><span>${esc(filedMeta)}</span>${pdfLinks(c, true)}</div>
        </div>

        <div class="brief-scope-note"><strong>Scope of this page</strong><p>${esc(scope)}</p>${!c.gap ? `<a href="/#status">See the broader investigation status →</a>` : ""}</div>

        <section class="brief-section brief-allegation">
          <span class="brief-section-number">01</span>
          <div><h3>What prosecutors allege in this filing</h3>${claims.length ? claims.map(function (cl) { return `<p class="brief-claim">${esc(civic(cl.claim_text))}</p>`; }).join("") : `<p class="brief-muted">${c.gap ? "The source filing is not yet published here." : esc(civic(c.count_label || "No narrative allegation has been expanded for this filing."))}</p>`}</div>
        </section>

        <section class="brief-section">
          <span class="brief-section-number">02</span>
          <div><h3>People and organizations named</h3><div class="brief-two-col"><div><h4>Defendants</h4>${defendantsHtml(c)}</div><div><h4>Organizations / providers</h4>${providersHtml(c)}</div></div></div>
        </section>

        <section class="brief-section">
          <span class="brief-section-number">03</span>
          <div><h3>Money in this filing</h3><p class="brief-section-intro">The label is part of the fact. Billed, paid, received, alleged loss and program-wide spending are different measurements.</p>${primaryMoney(c)}${c.plea_note ? `<p class="brief-procedure-note">${esc(civic(c.plea_note))}</p>` : ""}${extractedMoneyHtml(c)}${statewideHtml(c)}</div>
        </section>

        <section class="brief-section">
          <span class="brief-section-number">04</span>
          <div><h3>Charges in this filing</h3>${countsHtml(c)}${relatedHtml(c)}</div>
        </section>

        <section class="brief-section">
          <span class="brief-section-number">05</span>
          <div><h3>Other sourced context</h3>${extraClaims.length ? `<ul class="brief-source-notes">${extraClaims.map(function (cl) { return `<li><a href="#/claims/${esc(cl.claim_id)}">${esc(civic(cl.claim_text))}</a></li>`; }).join("")}</ul>` : `<p class="brief-muted">No additional source notes are attached to this filing in the current published set.</p>`}</div>
        </section>

        <section class="brief-section brief-sources">
          <span class="brief-section-number">06</span>
          <div><h3>Primary and supporting sources</h3><p class="brief-section-intro">Use the filing itself as the authority. The brief above is an aid for reading it.</p>${pdfLinks(c, false)}${c.courtlistener_url ? `<p><a href="${esc(c.courtlistener_url)}">Open the CourtListener docket →</a></p>` : ""}<ul class="brief-source-list">${sourceList(c.source_ids) || "<li>No additional source links are attached to this card.</li>"}</ul></div>
        </section>
      </article>`;
  }

  function enhanceReadingGuide() {
    if (app.querySelector(".brief-reading-marker")) return;
    const kicker = app.querySelector(".record-kicker");
    const h2 = app.querySelector("h2");
    const lede = app.querySelector(".lede");
    if (kicker) kicker.textContent = "// Reading guide";
    if (h2) h2.textContent = "Read the filing for what it is.";
    if (lede) lede.textContent = "Court records become misleading when procedural status or dollar categories are flattened. These distinctions keep the evidence honest.";
    const p = document.createElement("p");
    p.className = "brief-context-link brief-reading-marker";
    p.innerHTML = 'Need the larger story first? <a href="/#story">Read the 90-second Minnesota overview.</a>';
    if (lede) lede.insertAdjacentElement("afterend", p);
    document.title = "Reading guide — The Record";
  }

  function enhanceMoney() {
    if (app.querySelector(".brief-money-marker")) return;
    const h2 = app.querySelector("h2");
    if (h2) h2.textContent = "Money, with the labels intact.";
    const marker = document.createElement("p");
    marker.className = "lede brief-money-marker";
    marker.textContent = "Use this as a source table, not a scoreboard. Every row tells you what a number measures and which case or source it belongs to.";
    if (h2) h2.insertAdjacentElement("afterend", marker);
    const strong = app.querySelector(".sum-banner strong");
    if (strong) strong.textContent = "Read before adding";
    document.title = "Money — The Record";
  }

  function enhanceOrganizations(parts) {
    if (parts.length === 1) {
      if (app.querySelector(".brief-organizations-marker")) return;
      const kicker = app.querySelector(".record-kicker");
      const h2 = app.querySelector("h2");
      const lede = app.querySelector(".lede");
      if (kicker) kicker.textContent = "// Organizations";
      if (h2) h2.textContent = "Organizations named in the source set";
      if (lede) lede.textContent = "These cards identify organizations that appear in filings, business records or tax records. Appearance here is not a finding of wrongdoing.";
      const marker = document.createElement("span");
      marker.className = "brief-organizations-marker";
      marker.hidden = true;
      app.appendChild(marker);
      app.querySelectorAll(".card").forEach(function (card) {
        const link = card.querySelector('h3 a[href^="#/entities/"]');
        if (!link) return;
        const id = link.getAttribute("href").split("/").pop();
        const entity = entityById(id);
        if (!entity) return;
        const registrationIds = entity.business_reg_ids || [];
        card.querySelectorAll(".chip").forEach(function (el) {
          if (registrationIds.indexOf(el.textContent.trim()) !== -1) el.remove();
        });
      });
      document.title = "Organizations — The Record";
      return;
    }

    if (app.querySelector(".brief-entity-marker")) return;
    const breadcrumb = app.querySelector(".meta a");
    if (breadcrumb) breadcrumb.textContent = "Organizations";
    app.querySelectorAll("h3").forEach(function (h) {
      if (h.textContent.trim() === "Sourced sentences") h.textContent = "Related source notes";
      if (h.textContent.trim() === "Officers / agents (as sourced)") h.textContent = "Officers / agents shown in the source records";
    });
    const marker = document.createElement("span");
    marker.className = "brief-entity-marker";
    marker.hidden = true;
    app.appendChild(marker);
  }

  function enhanceClaim() {
    if (app.querySelector(".brief-claim-marker")) return;
    const h2 = app.querySelector("h2");
    if (h2) h2.textContent = "Source note";
    app.querySelectorAll("h3").forEach(function (h) {
      const text = h.textContent.trim();
      if (text === "How to hold this") h.textContent = "Why this needs context";
      if (text === "Passages") h.textContent = "Supporting passages";
    });
    const marker = document.createElement("span");
    marker.className = "brief-claim-marker";
    marker.hidden = true;
    app.appendChild(marker);
    document.title = "Source note — The Record";
  }

  function routeParts() {
    return (location.hash || "#/cases").replace(/^#\/?/, "").split("/").filter(Boolean);
  }

  function applyPublicationLayer() {
    const parts = routeParts();
    const head = parts[0] || "cases";

    if (head === "cases") {
      if (parts[1] === "family") {
        if (!app.querySelector(".brief-cases-root")) renderCases(parts[2] || "");
        return;
      }
      if (!parts[1]) {
        if (!app.querySelector(".brief-cases-root")) renderCases("");
        return;
      }
      if (!app.querySelector(".brief-case-root")) {
        const c = caseById(parts[1]);
        if (c) renderCase(c);
      }
      return;
    }
    if (head === "index") return enhanceReadingGuide();
    if (head === "money") return enhanceMoney();
    if (head === "entities") return enhanceOrganizations(parts);
    if (head === "claims") return enhanceClaim();
  }

  let scheduled = false;
  function schedule() {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(function () {
      scheduled = false;
      applyPublicationLayer();
    });
  }

  const observer = new MutationObserver(schedule);
  observer.observe(app, { childList: true, subtree: true });
  window.addEventListener("hashchange", function () { setTimeout(schedule, 40); });
  schedule();
})();
