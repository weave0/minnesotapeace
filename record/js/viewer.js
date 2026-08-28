/* The Record — public face. Reads window.__CORPUS__. Voice is civic; facts stay in the bundle. */
(function () {
  "use strict";

  const CORPUS = window.__CORPUS__;
  const app = document.getElementById("app");
  const TITLE_SUFFIX = " — The Record";

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

  const STATUS_LABEL = {
    CHARGED_ALLEGED: "Charged (not convicted)",
    charged: "Charged",
    alleged: "Alleged",
    confirmed: "Confirmed as sourced",
    AGENCY_POSITION: "Agency filing",
    CIVIL_ALLEGED_OR_RESOLVED: "Civil allegation",
  };

  const INSTRUMENT_LABEL = {
    indictment: "Indictment",
    superseding_indictment: "Superseding indictment",
    felony_information: "Felony information",
  };

  const ENTITY_TYPE_LABEL = {
    NONPROFIT: "Nonprofit",
    BUSINESS: "Business",
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
      {
        href: "/record/documents/22-cr-00124-ecf22.pdf",
        label: "Open the related charging document (PDF)",
      },
    ],
  };

  function esc(value) {
    return String(value ?? "").replace(/[&<>"']/g, (ch) => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#39;",
    }[ch]));
  }

  function formatUsd(value, exact) {
    if (value == null || value === "") return "—";
    const n = Number(value);
    if (!Number.isFinite(n)) return esc(String(value));
    const digits = exact === "exact" && Math.abs(n) < 1e7 ? 2 : 0;
    const formatted = new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      maximumFractionDigits: digits,
      minimumFractionDigits: 0,
    }).format(n);
    return exact === "approximate" ? "about " + formatted : formatted;
  }

  function kindLabel(type) {
    if (!type) return "Kind not labeled";
    return KIND_LABEL[type] || String(type).replace(/_/g, " ");
  }

  function statusLabel(raw) {
    if (!raw) return "";
    if (STATUS_LABEL[raw]) return STATUS_LABEL[raw];
    return String(raw).replace(/_/g, " ").toLowerCase().replace(/^\w/, (c) => c.toUpperCase());
  }

  function instrumentLabel(raw) {
    if (!raw) return "";
    return INSTRUMENT_LABEL[raw] || String(raw).replace(/_/g, " ");
  }

  function entityTypeLabel(raw) {
    if (!raw) return "";
    return ENTITY_TYPE_LABEL[raw] || String(raw).replace(/_/g, " ").toLowerCase();
  }

  function standingClass(raw) {
    if (raw === "CHARGED_ALLEGED" || raw === "charged" || raw === "alleged") return "is-charged";
    return "";
  }

  function chip(text, extra) {
    if (!text) return "";
    return `<span class="chip ${extra || ""}">${esc(text)}</span>`;
  }

  function sourceById(id) {
    return CORPUS.sources[id] || null;
  }

  function claimById(id) {
    return CORPUS.claims.find((c) => c.claim_id === id) || null;
  }

  function caseById(id) {
    return CORPUS.cases.find((c) => c.id === id) || null;
  }

  function entityById(id) {
    return CORPUS.entities.find((e) => e.entity_id === id) || null;
  }

  function caseForDocket(docket) {
    if (!docket) return null;
    const key = (docket.match(/0:\d{2}-cr-\d+/i) || [])[0];
    if (!key) return null;
    return CORPUS.cases.find((c) => c.docket.toLowerCase() === key.toLowerCase()) || null;
  }

  function sourceTitle(id) {
    const src = sourceById(id);
    if (src && src.title) return src.title;
    return "Source";
  }

  function sourceLinks(ids) {
    return (ids || []).map((id) => {
      const src = sourceById(id);
      const title = sourceTitle(id);
      const parts = [];
      if (src && src.canonical_url) {
        parts.push(`<a href="${esc(src.canonical_url)}">${esc(title)}</a>`);
      } else {
        parts.push(esc(title));
      }
      if (src && src.archive_url) {
        parts.push(`<a href="${esc(src.archive_url)}">Internet Archive</a>`);
      }
      return `<li>${parts.join(" · ")}</li>`;
    }).join("");
  }

  function overlapNote(amounts) {
    const list = (amounts || []).filter((a) => a && a.value != null);
    if (list.length < 2) return "";
    const counts = {};
    list.forEach((a) => {
      const g = a.overlap_group_id;
      if (!g) return;
      counts[g] = (counts[g] || 0) + 1;
    });
    const shared = Object.keys(counts).some((k) => counts[k] > 1);
    if (!shared) return "";
    return `<p class="no-sum">Same dollars, restated — do not add these.</p>`;
  }

  function pdfBlock(c) {
    const href = PUBLISHED_PDF[c.id];
    if (!href) return "";
    const related = (RELATED_PDF[c.id] || []).map((r) =>
      `<p class="small"><a class="pdf-link pdf-link-quiet" href="${esc(r.href)}">${esc(r.label)}</a></p>`
    ).join("");
    return `
      <p><a class="pdf-link" href="${esc(href)}">Open the charging document (PDF)</a></p>
      ${related}
    `;
  }

  function hashParts() {
    const raw = (location.hash || "#/").replace(/^#/, "");
    return raw.replace(/^\/+/, "").split("/").filter(Boolean);
  }

  function setNav(active) {
    document.querySelectorAll("[data-nav]").forEach((a) => {
      if (a.getAttribute("data-nav") === active) a.setAttribute("aria-current", "page");
      else a.removeAttribute("aria-current");
    });
  }

  function setTitle(prefix) {
    document.title = prefix + TITLE_SUFFIX;
  }

  function familyFilters(active) {
    const chips = [
      { id: "", href: "#/cases", label: "All" },
      { id: "feeding-our-future", href: "#/cases/family/feeding-our-future", label: "FOF" },
      { id: "hss", href: "#/cases/family/hss", label: "HSS" },
    ];
    return `<div class="case-filters" role="navigation" aria-label="Filter cases by family">${chips.map((c) =>
      `<a class="filter-chip${c.id === (active || "") ? " is-on" : ""}" href="${c.href}"${c.id === (active || "") ? ' aria-current="true"' : ""}>${c.label}</a>`
    ).join("")}</div>`;
  }

  function primaryDollarHtml(c) {
    if (c.gap) {
      return `<p class="quiet-note">This charging document is not in the file yet.</p>`;
    }
    const amts = c.primary_amounts || [];
    if (!amts.length) {
      return `<p class="no-sum">This indictment maps counts. It does not isolate a billed or paid total on the face of the document.</p>`;
    }
    return amts.map((a) => `
      <p class="dollar">
        <span class="num">${esc(formatUsd(a.value, a.exact_or_approximate))}</span>
        ${chip(kindLabel(a.metric_type), "metric")}
      </p>
    `).join("") + overlapNote(amts);
  }

  function renderIndex() {
    setNav("index");
    setTitle("How to read");
    app.innerHTML = `
      <span class="record-kicker">// How to read</span>
      <h2>A charge is not a conviction.</h2>
      <p class="lede">Read slowly. The labels are doing work a headline will not do.</p>
      <ul class="rules">
        <li>Charged means a prosecutor wrote it in an instrument. It is not a conviction.</li>
        <li>Billed is not paid. Paid is not alleged loss. Alleged loss is not proven.</li>
        <li>When two figures describe the same money, do not add them.</li>
        <li>A guilty plea in a docket minute is not a sentence.</li>
      </ul>
      <p>This record follows private actors charged with fraud against public programs. It does not accuse a named official of joining that crime.</p>
      <p>Two families: <a href="#/cases/family/feeding-our-future">Feeding Our Future / child nutrition</a>, and <a href="#/cases/family/hss">Housing Stabilization Services</a>.</p>
      <p><a href="#/cases">Open the cases</a></p>
    `;
  }

  function vtIdent(id) {
    return "vt-case-" + String(id || "").replace(/[^a-zA-Z0-9_-]/g, "");
  }

  function prefersReduce() {
    return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  }

  function caseCard(c) {
    const family = CORPUS.families.find((f) => f.id === c.family);
    return `
      <article class="card" style="view-transition-name:${vtIdent(c.id)}">
        <p class="meta">${esc(c.docket)} · ${esc(instrumentLabel(c.instrument))}</p>
        <h3><a href="#/cases/${esc(c.id)}">${esc(c.short_name)}</a></h3>
        <p class="small">${esc(c.caption || "")}</p>
        <div class="chips">
          ${chip(family ? family.name : c.family)}
          ${chip(c.count_label)}
          ${c.gap ? "" : chip(statusLabel(c.evidentiary_status), standingClass(c.evidentiary_status))}
        </div>
        <p class="small">${esc((c.defendants || []).join("; "))}</p>
        ${primaryDollarHtml(c)}
      </article>
    `;
  }

  function renderCases(familyId) {
    setNav("cases");
    const family = CORPUS.families.find((f) => f.id === familyId) || null;
    setTitle(family ? family.name + " · Cases" : "Cases");
    const fof = CORPUS.cases.filter((c) => c.family === "feeding-our-future");
    const hss = CORPUS.cases.filter((c) => c.family === "hss");
    const showFof = !familyId || familyId === "feeding-our-future";
    const showHss = !familyId || familyId === "hss";
    const unknown = familyId && !family;
    app.innerHTML = `
      <span class="record-kicker">// Cases</span>
      <h2>Charging documents</h2>
      <p class="lede">One card for each charging document in this record. Filter by family. Dollars keep their kind — billed is not paid.</p>
      ${familyFilters(familyId || "")}
      ${unknown ? `<div class="not-found"><p>No family named ${esc(familyId)}.</p></div>` : ""}
      ${showFof && !unknown ? `<h3>Feeding Our Future / child nutrition</h3><div class="card-grid">${fof.map(caseCard).join("")}</div>` : ""}
      ${showHss && !unknown ? `<h3>Housing Stabilization Services</h3><div class="card-grid">${hss.map(caseCard).join("")}</div>` : ""}
    `;
  }

  function allegationHtml(c) {
    const claims = (c.primary_claim_ids || []).map(claimById).filter(Boolean);
    if (claims.length) {
      return claims.map((cl) => `<p class="claim-text">${esc(cl.claim_text)}</p>`).join("");
    }
    if (c.gap) return "";
    if (c.count_label) {
      return `<p>${esc(c.count_label)}.</p>`;
    }
    return "";
  }

  function renderCase(id) {
    setNav("cases");
    const c = caseById(id);
    if (!c) {
      app.innerHTML = `<div class="not-found"><p>No case named ${esc(id)}.</p><p><a href="#/cases">Back to cases</a></p></div>`;
      return;
    }
    setTitle(c.short_name);
    const claims = (c.claim_ids || []).map(claimById).filter(Boolean);
    const countRows = (c.counts || []).map((row) => `
      <tr>
        <td>${esc(row.count ?? "")}</td>
        <td>${esc(row.title || "")}${row.statute ? `<div class="small muted">${esc(row.statute)}</div>` : ""}</td>
        <td>${esc(row.date || "")}</td>
        <td>${esc(row.wire || row.notes || "")}</td>
        <td class="small">${esc((row.named_defendants || []).join("; "))}</td>
      </tr>
    `).join("");
    const extractAmts = (c.extract_amounts || []).filter((a) => a && a.value != null);
    const extractAmtRows = extractAmts.map((a) => `
      <tr>
        <td class="numcell">${esc(formatUsd(a.value, a.exact_or_approximate))}</td>
        <td>${chip(kindLabel(a.metric_type), "metric")}</td>
        <td class="small">${esc(a.provider || a.period || a.period_start || "")}</td>
        <td class="small">${esc(a.notes || a.quote || "")}</td>
      </tr>
    `).join("");
    const related = (c.related_instruments || []).map((r) => `
      <p class="small">${esc(instrumentLabel(r.instrument) || r.instrument)} (ECF ${esc(r.ecf)}). ${esc(r.note)}</p>
    `).join("");
    const statewide = c.statewide_recital ? `
      <h3>Program payout (background)</h3>
      <p class="small">These figures are program-wide payouts recited on the charging document. They are not this case’s alleged loss. Do not add them to the case dollars.</p>
      <table>
        <thead><tr><th>Period</th><th>Amount</th><th>What this number is</th></tr></thead>
        <tbody>
          ${(c.statewide_recital.rows || []).map((r) => `
            <tr>
              <td>${esc(r.period)}</td>
              <td class="numcell">${esc(formatUsd(r.value, r.exact_or_approximate))}</td>
              <td>${chip(kindLabel(c.statewide_recital.metric_type), "metric")}</td>
            </tr>
          `).join("")}
        </tbody>
      </table>
    ` : "";
    const sources = sourceLinks(c.source_ids);
    const plea = c.plea_note
      ? `<p class="small">${esc(c.plea_note.replace(/Do not mark ADJUDICATED\.?/g, "").replace(/\bRECAP\b/g, "the public file").trim())}</p>`
      : "";
    app.innerHTML = `
      <span class="record-kicker">// Case</span>
      <p class="meta"><a href="#/cases">Cases</a> / ${esc(c.docket)}</p>
      <h2 style="view-transition-name:${vtIdent(c.id)}">${esc(c.caption || c.short_name)}</h2>
      <div class="chips">
        ${chip(instrumentLabel(c.instrument))}
        ${chip(c.count_label)}
        ${c.gap ? "" : chip(statusLabel(c.evidentiary_status), standingClass(c.evidentiary_status))}
      </div>
      ${pdfBlock(c)}
      <h3>What this instrument alleges</h3>
      ${allegationHtml(c)}
      <div class="two-col">
        <div>
          <h3>Defendants</h3>
          <ul class="def-list">${(c.defendants || []).map((d) => `<li>${esc(d)}</li>`).join("") || "<li>Not named on this card</li>"}</ul>
          <h3>Providers named on the face</h3>
          <ul class="def-list">${(c.providers || []).map((p) => {
            const link = p.entity_id && entityById(p.entity_id)
              ? `<a href="#/entities/${esc(p.entity_id)}">${esc(p.name)}</a>`
              : esc(p.name || "");
            return `<li>${link}${p.role_on_face ? `<div class="small muted">${esc(p.role_on_face)}</div>` : ""}</li>`;
          }).join("") || "<li>None named on this card</li>"}</ul>
        </div>
        <div>
          <h3>Dollars</h3>
          ${primaryDollarHtml(c)}
          ${plea}
          ${c.filed ? `<p class="meta">Filed ${esc(c.filed)}${c.pages ? " · " + c.pages + " pages" : ""}</p>` : ""}
          ${c.courtlistener_url ? `<p><a href="${esc(c.courtlistener_url)}">CourtListener docket</a></p>` : ""}
        </div>
      </div>
      ${related ? `<h3>Related instrument</h3>${related}` : ""}
      <h3>Counts</h3>
      ${countRows ? `<table><thead><tr><th>Count</th><th>Charge</th><th>Date</th><th>Notes</th><th>Named</th></tr></thead><tbody>${countRows}</tbody></table>` : `<p class="small muted">${c.gap ? "Counts are not mapped." : "No expanded count rows."}</p>`}
      ${extractAmtRows ? `<h3>Figures on the document</h3>${overlapNote(extractAmts) || `<p class="no-sum">Do not add these.</p>`}
        <table><thead><tr><th>Amount</th><th>What this number is</th><th>Context</th><th>Notes</th></tr></thead><tbody>${extractAmtRows}</tbody></table>` : ""}
      ${statewide}
      <h3>What else is sourced here</h3>
      ${claims.length ? `<ul>${claims.map((cl) => `<li><a href="#/claims/${esc(cl.claim_id)}">${esc(cl.claim_text.slice(0, 180))}${(cl.claim_text.length > 180) ? "…" : ""}</a></li>`).join("")}</ul>` : "<p class='small muted'>No additional sourced sentences are keyed to this docket.</p>"}
      <h3>Sources</h3>
      <ul>${sources || "<li>None attached on this card.</li>"}</ul>
    `;
  }

  function renderClaim(id) {
    setNav("cases");
    const cl = claimById(id);
    if (!cl) {
      app.innerHTML = `<div class="not-found"><p>That sourced sentence is not in this record.</p></div>`;
      return;
    }
    setTitle("Sourced sentence");
    const cse = caseForDocket(cl.case_number);
    const passages = (cl.supporting_passages || []).map((p) => {
      const src = sourceById(p.source_id);
      const loc = [p.page != null ? "p. " + p.page : null, p.locator].filter(Boolean).join(", ");
      const title = sourceTitle(p.source_id);
      return `<li>
        <p class="meta">${esc(title)}${loc ? " · " + esc(loc) : ""}${src && src.canonical_url ? ` · <a href="${esc(src.canonical_url)}">source</a>` : ""}${src && src.archive_url ? ` · <a href="${esc(src.archive_url)}">Internet Archive</a>` : ""}</p>
        ${p.quote ? `<blockquote class="quote">${esc(p.quote)}</blockquote>` : ""}
      </li>`;
    }).join("");
    const amounts = (cl.amounts || []).map((a) => `
      <tr>
        <td class="numcell">${esc(formatUsd(a.value, a.exact_or_approximate))}</td>
        <td>${chip(kindLabel(a.metric_type), "metric")}</td>
        <td class="small">${esc([a.period_start, a.period_end].filter(Boolean).join(" – "))}</td>
        <td class="small">${esc(a.methodology || "")}</td>
      </tr>
    `).join("");
    const orgs = (cl.organizations || cl.subject_ids || []).map((oid) => {
      const ent = entityById(oid);
      return ent
        ? `<a href="#/entities/${esc(oid)}">${esc(ent.canonical_name)}</a>`
        : "";
    }).filter(Boolean);
    app.innerHTML = `
      <p class="meta"><a href="#/cases">Cases</a>${cse ? ` / <a href="#/cases/${esc(cse.id)}">${esc(cse.short_name)}</a>` : ""}</p>
      <h2>What is sourced</h2>
      <div class="chips">
        ${chip(statusLabel(cl.status), standingClass(cl.status))}
        ${chip(statusLabel(cl.evidence_class), standingClass(cl.evidence_class))}
        ${cl.case_number ? chip(cl.case_number) : ""}
      </div>
      <p class="claim-text">${esc(cl.claim_text)}</p>
      ${amounts ? `<h3>Dollars</h3>${overlapNote(cl.amounts) || `<p class="no-sum">Each row keeps its kind. Do not add figures that describe the same money.</p>`}
        <table><thead><tr><th>Amount</th><th>What this number is</th><th>Period</th><th>How it was read</th></tr></thead><tbody>${amounts}</tbody></table>` : ""}
      ${cl.qualifiers && cl.qualifiers.length ? `<h3>How to hold this</h3><ul class="rules">${cl.qualifiers.map((q) => `<li>${esc(q)}</li>`).join("")}</ul>` : ""}
      <h3>Passages</h3>
      ${passages ? `<ul class="passages">${passages}</ul>` : "<p class='small muted'>No supporting passages on this record.</p>"}
      <h3>Sources</h3>
      <ul>${sourceLinks(cl.source_ids) || "<li>None</li>"}</ul>
      ${orgs.length ? `<h3>Organizations</h3><p>${orgs.join(" · ")}</p>` : ""}
    `;
  }

  function renderMoney() {
    setNav("money");
    setTitle("Money");
    const groups = new Map();
    CORPUS.money.forEach((row) => {
      const key = row.overlap_group_id;
      if (!groups.has(key)) groups.set(key, []);
      groups.get(key).push(row);
    });
    const metrics = [...new Set(CORPUS.money.map((r) => r.metric_type))].sort();
    const families = [
      { id: "", label: "All families" },
      { id: "feeding-our-future", label: "Feeding Our Future" },
      { id: "hss", label: "HSS" },
      { id: "other", label: "Other / filings" },
    ];

    function familyOf(row) {
      const cse = caseForDocket(row.case_number);
      return cse ? cse.family : "other";
    }

    function groupHeading(rows, key) {
      const label = rows[0].overlap_label;
      if (label && !/^ungrouped:/i.test(String(key))) {
        return String(label)
          .replace(/program_spend/g, "program payout")
          .replace(/alleged_loss/g, "alleged loss")
          .replace(/overlap group/gi, "same dollars");
      }
      return "Standalone figure";
    }

    function paint() {
      const metric = document.getElementById("metric-filter").value;
      const family = document.getElementById("family-filter").value;
      let body = "";
      let shown = 0;
      groups.forEach((rows, key) => {
        const filtered = rows.filter((r) => {
          if (metric && r.metric_type !== metric) return false;
          if (family && familyOf(r) !== family) return false;
          return true;
        });
        if (!filtered.length) return;
        const heading = groupHeading(filtered, key);
        const addNote = filtered.length > 1 ? " — do not add these" : "";
        body += `<tr class="group-head"><td colspan="5">${esc(heading)}${esc(addNote)}</td></tr>`;
        filtered.forEach((r) => {
          shown += 1;
          const cse = caseForDocket(r.case_number);
          body += `<tr>
            <td class="numcell">${esc(formatUsd(r.value, r.exact_or_approximate))}</td>
            <td>${chip(kindLabel(r.metric_type), "metric")}</td>
            <td>${chip(statusLabel(r.evidence_class), standingClass(r.evidence_class))}</td>
            <td>${cse ? `<a href="#/cases/${esc(cse.id)}">${esc(cse.short_name)}</a>` : esc(r.case_number || "—")}</td>
            <td class="small">${esc(r.methodology || "")}</td>
          </tr>`;
        });
      });
      document.getElementById("money-body").innerHTML = body || `<tr><td colspan="5">No rows for this filter.</td></tr>`;
      document.getElementById("money-count").textContent = `${shown} rows shown. This is a count of rows, not a dollar total.`;
    }

    app.innerHTML = `
      <span class="record-kicker">// Money</span>
      <h2>Money</h2>
      <div class="sum-banner">
        <p><strong>Do not add these rows</strong></p>
        <p>Billed is not paid. Paid is not alleged loss. Alleged loss is not a program payout. A program-wide payout recited on a charging document is background, not this case’s loss. When two figures describe the same money, do not add them.</p>
      </div>
      <div class="filters">
        <label>What this number is
          <select id="metric-filter">
            <option value="">All kinds</option>
            ${metrics.map((m) => `<option value="${esc(m)}">${esc(kindLabel(m))}</option>`).join("")}
          </select>
        </label>
        <label>Family
          <select id="family-filter">
            ${families.map((f) => `<option value="${esc(f.id)}">${esc(f.label)}</option>`).join("")}
          </select>
        </label>
      </div>
      <p class="small muted" id="money-count"></p>
      <table>
        <thead>
          <tr>
            <th>Amount</th>
            <th>What this number is</th>
            <th>Standing</th>
            <th>Case</th>
            <th>How it was read</th>
          </tr>
        </thead>
        <tbody id="money-body"></tbody>
      </table>
    `;
    document.getElementById("metric-filter").addEventListener("change", paint);
    document.getElementById("family-filter").addEventListener("change", paint);
    paint();
  }

  function renderEntities() {
    setNav("entities");
    setTitle("Entities");
    const cards = CORPUS.entities.map((e) => `
      <article class="card">
        <p class="meta">${esc(entityTypeLabel(e.entity_type))}${e.ein ? " · EIN " + esc(e.ein) : ""}</p>
        <h3><a href="#/entities/${esc(e.entity_id)}">${esc(e.canonical_name)}</a></h3>
        ${(e.business_reg_ids || []).map((id) => chip(id)).join(" ")}
        ${e.notes ? `<p class="small">${esc(e.notes.slice(0, 220))}${e.notes.length > 220 ? "…" : ""}</p>` : ""}
      </article>
    `).join("");
    app.innerHTML = `
      <span class="record-kicker">// Entities</span>
      <h2>Organizations</h2>
      <p class="lede">Organizations named in these files. Feeding Our Future and Feeding Our Future II are separate organizations. A shared street address is not a conspiracy.</p>
      <div class="notice"><p><strong>Identity, not guilt</strong> A business filing or a tax return is not a charging document. A name match is not a conviction.</p></div>
      <div class="card-grid">${cards}</div>
    `;
  }

  function renderEntity(id) {
    setNav("entities");
    const e = entityById(id);
    if (!e) {
      app.innerHTML = `<div class="not-found"><p>That organization is not in this record.</p><p><a href="#/entities">Back to entities</a></p></div>`;
      return;
    }
    setTitle(e.canonical_name);
    const claims = CORPUS.claims.filter((c) =>
      (c.organizations || []).includes(id) || (c.subject_ids || []).includes(id)
    );
    const officers = (e.officers || []).map((o) => `
      <tr>
        <td>${esc(o.name)}</td>
        <td>${esc(o.title || "")}</td>
        <td class="small">${esc([o.valid_from, o.valid_until].filter(Boolean).join(" – ") || "—")}</td>
      </tr>
    `).join("");
    const addrs = (e.addresses || []).map((a) => `
      <p class="addr">${esc([a.line1, a.line2, a.city, a.state, a.postal_code].filter(Boolean).join(", "))}</p>
    `).join("");
    app.innerHTML = `
      <p class="meta"><a href="#/entities">Entities</a> / ${esc(e.canonical_name)}</p>
      <h2>${esc(e.canonical_name)}</h2>
      <div class="chips">
        ${chip(entityTypeLabel(e.entity_type))}
        ${e.ein ? chip("EIN " + e.ein) : ""}
        ${(e.business_reg_ids || []).map((reg) => chip(reg)).join("")}
        ${(e.aliases || []).map((a) => chip(a)).join("")}
        ${(e.former_names || []).map((a) => chip("formerly " + a)).join("")}
      </div>
      ${e.notes ? `<p>${esc(e.notes)}</p>` : ""}
      ${id === "org-feeding-our-future" ? `<p class="small">Kept separate from <a href="#/entities/org-feeding-our-future-ii">Feeding Our Future II</a>.</p>` : ""}
      ${id === "org-feeding-our-future-ii" ? `<p class="small">Kept separate from <a href="#/entities/org-feeding-our-future">Feeding Our Future</a>. A shared registered-office vendor is not a merge.</p>` : ""}
      <h3>Addresses</h3>
      ${addrs || "<p class='small muted'>None on this record.</p>"}
      <p class="small muted">A shared address is not a conspiracy.</p>
      ${officers ? `<h3>Officers / agents (as sourced)</h3>
        <table><thead><tr><th>Name</th><th>Title</th><th>Dates</th></tr></thead><tbody>${officers}</tbody></table>` : ""}
      <h3>Sourced sentences</h3>
      ${claims.length ? `<ul>${claims.map((cl) => `<li><a href="#/claims/${esc(cl.claim_id)}">${esc(cl.claim_text.slice(0, 160))}${cl.claim_text.length > 160 ? "…" : ""}</a></li>`).join("")}</ul>` : "<p class='small muted'>No sourced sentences name this organization.</p>"}
      <h3>Sources</h3>
      <ul>${sourceLinks(e.source_ids) || "<li>None</li>"}</ul>
    `;
  }

  function paintRoute() {
    if (!CORPUS) {
      app.innerHTML = "<p>The record did not load.</p>";
      return;
    }
    const parts = hashParts();
    const head = parts[0] || "";
    if (!head) {
      if (location.hash !== "#/cases") {
        history.replaceState(null, "", "#/cases");
      }
      return renderCases();
    }
    if (head === "index") return renderIndex();
    if (head === "cases" && parts[1] === "family") return renderCases(parts[2] || "");
    if (head === "cases" && !parts[1]) return renderCases();
    if (head === "cases" && parts[1]) return renderCase(parts[1]);
    if (head === "claims" && parts[1]) return renderClaim(parts[1]);
    if (head === "money") return renderMoney();
    if (head === "entities" && !parts[1]) return renderEntities();
    if (head === "entities" && parts[1]) return renderEntity(parts[1]);
    app.innerHTML = `<div class="not-found"><p>No such page.</p><p><a href="#/cases">Cases</a> · <a href="#/index">How to read</a></p></div>`;
  }

  function onHashChange() {
    if (prefersReduce() || typeof document.startViewTransition !== "function") {
      paintRoute();
      return;
    }
    document.startViewTransition(function () {
      paintRoute();
    });
  }

  window.addEventListener("hashchange", onHashChange);
  paintRoute();
})();
