/* MinnesotaPeace research viewer. Reads window.__CORPUS__ (see data/corpus.js). */
(function () {
  "use strict";

  const CORPUS = window.__CORPUS__;
  const app = document.getElementById("app");

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

  function metricLabel(type) {
    return type || "metric_type missing";
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

  function sourceLinks(ids) {
    return (ids || []).map((id) => {
      const src = sourceById(id);
      const title = src ? src.title || id : id;
      const parts = [];
      if (src && src.canonical_url) {
        parts.push(`<a href="${esc(src.canonical_url)}">${esc(title)}</a>`);
      } else {
        parts.push(esc(title));
      }
      if (src && src.archive_url) {
        parts.push(`<a href="${esc(src.archive_url)}">Internet Archive</a>`);
      }
      parts.push(`<span class="mono">${esc(id)}</span>`);
      return `<li>${parts.join(" · ")}</li>`;
    }).join("");
  }

  function hashParts() {
    const raw = (location.hash || "#/").replace(/^#/, "");
    const segs = raw.replace(/^\/+/, "").split("/").filter(Boolean);
    return segs;
  }

  function setNav(active) {
    document.querySelectorAll("nav [data-nav]").forEach((a) => {
      if (a.getAttribute("data-nav") === active) a.setAttribute("aria-current", "page");
      else a.removeAttribute("aria-current");
    });
  }

  function primaryDollarHtml(c) {
    if (c.gap) {
      return `<p class="no-sum">No charging-instrument dollar in this corpus. The information is not on RECAP.</p>`;
    }
    const amts = c.primary_amounts || [];
    if (!amts.length) {
      return `<p class="no-sum">${esc(c.primary_dollar_note || "No isolated case-level billed/paid total on this extract.")}</p>`;
    }
    return amts.map((a) => `
      <p class="dollar">
        <span class="num">${esc(formatUsd(a.value, a.exact_or_approximate))}</span>
        ${chip(metricLabel(a.metric_type), "metric")}
        ${chip(a.evidence_class, "ev-" + (a.evidence_class || ""))}
      </p>
    `).join("") + (amts.length > 1 ? `<p class="no-sum">These figures share an overlap group. Do not add them.</p>` : "");
  }

  function renderIndex() {
    setNav("index");
    document.title = "MinnesotaPeace research corpus";
    const families = CORPUS.families.map((f) => `
      <article class="family-card">
        <p class="meta">${esc(f.id)}</p>
        <h3>${esc(f.name)}</h3>
        <p>${esc(f.blurb)}</p>
        <p><a href="#/cases">Open cases</a></p>
      </article>
    `).join("");
    const gaps = CORPUS.gaps.map((g) => `
      <article class="gap-card">
        <h3>${esc(g.title)}</h3>
        <p>${esc(g.detail)}</p>
        ${g.case_id ? `<p><a href="#/cases/${esc(g.case_id)}">Open related case</a></p>` : ""}
      </article>
    `).join("");
    app.innerHTML = `
      <p class="lede">${esc(CORPUS.mandate)}</p>
      <div class="notice">
        <p><strong>No total</strong> This index does not add case figures. Overlapping dollars stay in their overlap groups. There is no corpus-wide loss number on this page.</p>
      </div>
      <h2>Investigation families</h2>
      <div class="family-grid">${families}</div>
      <h2>Mandate</h2>
      <ul class="rules">
        ${CORPUS.editorial_rules.map((r) => `<li>${esc(r)}</li>`).join("")}
      </ul>
      <h2>Actor classes</h2>
      <p class="small">v1 records private-actor charging documents (A) and does not claim official knowing duty violation (D) or official knowing crime (E). Oversight failure (B) and negligence (C) are not collapsed into D/E. Collected sources do not support D/E.</p>
      <h2>Documented gaps</h2>
      <div class="card-grid">${gaps}</div>
      <p class="muted small">Bundle generated ${esc(CORPUS.generated_at)}. ${CORPUS.claims.length} claims · ${CORPUS.cases.length} charging instruments · ${CORPUS.money.length} money rows · ${CORPUS.entities.length} organizations.</p>
    `;
  }

  function caseCard(c) {
    const klass = c.gap ? "gap-card" : "card";
    const family = CORPUS.families.find((f) => f.id === c.family);
    return `
      <article class="${klass}">
        <p class="meta">${esc(c.docket)} · ECF ${esc(c.ecf ?? "—")} · ${esc(c.instrument)}</p>
        <h3><a href="#/cases/${esc(c.id)}">${esc(c.short_name)}</a></h3>
        <p class="small">${esc(c.caption || "")}</p>
        <div class="chips">
          ${chip(family ? family.name : c.family)}
          ${chip(c.count_label)}
          ${c.gap ? chip("RECAP gap", "gap") : chip(c.evidentiary_status, "ev-" + c.evidentiary_status)}
        </div>
        <p class="small">${esc((c.defendants || []).join("; "))}</p>
        ${primaryDollarHtml(c)}
      </article>
    `;
  }

  function renderCases() {
    setNav("cases");
    document.title = "Cases — MinnesotaPeace research corpus";
    const fof = CORPUS.cases.filter((c) => c.family === "feeding-our-future");
    const hss = CORPUS.cases.filter((c) => c.family === "hss");
    app.innerHTML = `
      <h2>Charging instruments</h2>
      <p class="lede">One card per mapped instrument. Asad Adow 0:25-cr-00354 is a gap card: the felony information is missing from RECAP. Dollars are the primary claim figure with <span class="mono">metric_type</span>, not a case total.</p>
      <h3>Feeding Our Future / child nutrition</h3>
      <div class="card-grid">${fof.map(caseCard).join("")}</div>
      <h3>Housing Stabilization Services</h3>
      <div class="card-grid">${hss.map(caseCard).join("")}</div>
    `;
  }

  function renderCase(id) {
    setNav("cases");
    const c = caseById(id);
    if (!c) {
      app.innerHTML = `<div class="not-found"><p>No case <span class="mono">${esc(id)}</span>.</p><p><a href="#/cases">Back to cases</a></p></div>`;
      return;
    }
    document.title = `${c.short_name} — MinnesotaPeace research corpus`;
    const claims = (c.claim_ids || []).map(claimById).filter(Boolean);
    const countRows = (c.counts || []).map((row) => `
      <tr>
        <td class="mono">${esc(row.count ?? "")}</td>
        <td>${esc(row.title || "")}<div class="mono muted">${esc(row.statute || "")}</div></td>
        <td>${esc(row.date || "")}</td>
        <td>${esc(row.wire || row.notes || "")}</td>
        <td class="small">${esc((row.named_defendants || []).join("; "))}</td>
      </tr>
    `).join("");
    const extractAmtRows = (c.extract_amounts || []).filter((a) => a && a.value != null && a.metric_type).map((a) => `
      <tr>
        <td class="numcell">${esc(formatUsd(a.value, a.exact_or_approximate))}</td>
        <td>${chip(a.metric_type, "metric")}</td>
        <td class="mono small">${esc(a.overlap_group_id || "—")}</td>
        <td class="small">${esc(a.provider || a.period || a.period_start || "")}</td>
        <td class="small">${esc(a.notes || a.quote || "")}</td>
      </tr>
    `).join("");
    const related = (c.related_instruments || []).map((r) => `
      <p class="small"><span class="mono">ECF ${esc(r.ecf)}</span> ${esc(r.instrument)}. ${esc(r.note)}</p>
    `).join("");
    const statewide = c.statewide_recital ? `
      <h3>Statewide HSS program_spend recital</h3>
      <p class="small">${esc(c.statewide_recital.notes || "Program-wide payout recital on the charging document. Not this case’s alleged_loss.")}</p>
      <table>
        <thead><tr><th>Period</th><th>Amount</th><th>metric_type</th></tr></thead>
        <tbody>
          ${(c.statewide_recital.rows || []).map((r) => `
            <tr>
              <td>${esc(r.period)}</td>
              <td class="numcell">${esc(formatUsd(r.value, r.exact_or_approximate))}</td>
              <td>${chip(c.statewide_recital.metric_type, "metric")}</td>
            </tr>
          `).join("")}
        </tbody>
      </table>
    ` : "";
    const sources = sourceLinks(c.source_ids);
    app.innerHTML = `
      ${c.gap ? `<div class="gap-banner"><p><strong>Document gap</strong> ${esc((c.gap_notes || [])[0] || "Charging instrument not in the corpus.")}</p></div>` : ""}
      <p class="meta"><a href="#/cases">Cases</a> / ${esc(c.docket)}</p>
      <h2>${esc(c.caption || c.short_name)}</h2>
      <div class="chips">
        ${chip(c.instrument)}
        ${chip("ECF " + (c.ecf ?? "—"))}
        ${chip(c.count_label)}
        ${chip(c.evidentiary_status, "ev-" + (c.evidentiary_status || ""))}
        ${c.not_adjudicated ? chip("not adjudicated") : ""}
        ${c.gap ? chip("RECAP gap", "gap") : ""}
      </div>
      <div class="two-col">
        <div>
          <h3>Defendants on the caption</h3>
          <ul class="def-list">${(c.defendants || []).map((d) => `<li>${esc(d)}</li>`).join("") || "<li>Not mapped</li>"}</ul>
          <h3>Providers named on the face</h3>
          <ul class="def-list">${(c.providers || []).map((p) => {
            const link = p.entity_id && entityById(p.entity_id)
              ? `<a href="#/entities/${esc(p.entity_id)}">${esc(p.name)}</a>`
              : esc(p.name || "");
            return `<li>${link}${p.role_on_face ? `<div class="small muted">${esc(p.role_on_face)}</div>` : ""}</li>`;
          }).join("") || "<li>None mapped</li>"}</ul>
        </div>
        <div>
          <h3>Primary dollar</h3>
          ${primaryDollarHtml(c)}
          ${c.plea_note ? `<p class="small">${esc(c.plea_note)}</p>` : ""}
          ${c.filed ? `<p class="meta">Filed ${esc(c.filed)}${c.pages ? " · " + c.pages + " pp." : ""}</p>` : ""}
          ${c.sha256 ? `<p class="mono small">SHA-256 ${esc(c.sha256)}</p>` : ""}
          ${c.courtlistener_url ? `<p><a href="${esc(c.courtlistener_url)}">CourtListener docket</a></p>` : ""}
        </div>
      </div>
      ${related ? `<h3>Related instrument</h3>${related}` : ""}
      ${(c.gap_notes || []).slice(1).map((n) => `<p class="small">${esc(n)}</p>`).join("")}
      ${c.do_not && c.do_not.length ? `<h3>Do not</h3><ul class="rules">${c.do_not.map((d) => `<li>${esc(d)}</li>`).join("")}</ul>` : ""}
      <h3>Counts</h3>
      ${countRows ? `<table><thead><tr><th>Count</th><th>Charge</th><th>Date</th><th>Wire / notes</th><th>Named</th></tr></thead><tbody>${countRows}</tbody></table>` : `<p class="small muted">${c.gap ? "No count table: information not in the corpus." : "No expanded count rows."}</p>`}
      ${extractAmtRows ? `<h3>Figures on the extract</h3><p class="no-sum">Do not sum these rows. Statewide recitals are not this case’s alleged_loss.</p>
        <table><thead><tr><th>Amount</th><th>metric_type</th><th>overlap_group</th><th>Context</th><th>Notes</th></tr></thead><tbody>${extractAmtRows}</tbody></table>` : ""}
      ${statewide}
      <h3>Claims</h3>
      ${claims.length ? `<ul>${claims.map((cl) => `<li><a href="#/claims/${esc(cl.claim_id)}">${esc(cl.claim_id)}</a> — ${esc(cl.claim_text.slice(0, 180))}${(cl.claim_text.length > 180) ? "…" : ""}</li>`).join("")}</ul>` : "<p class='small muted'>No claim-*.json records keyed to this docket.</p>"}
      <h3>Sources</h3>
      <ul>${sources || "<li>None attached on the case catalog.</li>"}</ul>
    `;
  }

  function renderClaim(id) {
    setNav("cases");
    const cl = claimById(id);
    if (!cl) {
      app.innerHTML = `<div class="not-found"><p>No claim <span class="mono">${esc(id)}</span>.</p></div>`;
      return;
    }
    document.title = `${cl.claim_id} — MinnesotaPeace research corpus`;
    const cse = caseForDocket(cl.case_number);
    const passages = (cl.supporting_passages || []).map((p) => {
      const src = sourceById(p.source_id);
      const loc = [p.page != null ? "p. " + p.page : null, p.locator].filter(Boolean).join(", ");
      return `<li>
        <p class="meta">${esc(p.source_id)}${loc ? " · " + esc(loc) : ""}${src && src.canonical_url ? ` · <a href="${esc(src.canonical_url)}">source</a>` : ""}${src && src.archive_url ? ` · <a href="${esc(src.archive_url)}">IA</a>` : ""}</p>
        ${p.quote ? `<blockquote class="quote">${esc(p.quote)}</blockquote>` : ""}
      </li>`;
    }).join("");
    const amounts = (cl.amounts || []).map((a) => `
      <tr>
        <td class="numcell">${esc(formatUsd(a.value, a.exact_or_approximate))}</td>
        <td>${chip(a.metric_type, "metric")}</td>
        <td class="mono small">${esc(a.overlap_group_id || "—")}</td>
        <td class="small">${esc([a.period_start, a.period_end].filter(Boolean).join(" – "))}</td>
        <td class="small">${esc(a.methodology || "")}</td>
      </tr>
    `).join("");
    const orgs = (cl.organizations || cl.subject_ids || []).map((oid) => {
      const ent = entityById(oid);
      return ent
        ? `<a href="#/entities/${esc(oid)}">${esc(ent.canonical_name)}</a>`
        : `<span class="mono">${esc(oid)}</span>`;
    });
    app.innerHTML = `
      <p class="meta"><a href="#/cases">Cases</a>${cse ? ` / <a href="#/cases/${esc(cse.id)}">${esc(cse.short_name)}</a>` : ""} / ${esc(cl.claim_id)}</p>
      <h2>Claim</h2>
      <div class="chips">
        ${chip(cl.status, "status-" + cl.status)}
        ${chip(cl.evidence_class, "ev-" + cl.evidence_class)}
        ${chip(cl.claim_type)}
        ${cl.proposition_class ? chip(cl.proposition_class) : ""}
        ${cl.is_allegation ? chip("allegation") : ""}
        ${cl.case_number ? chip(cl.case_number) : ""}
      </div>
      <p class="claim-text">${esc(cl.claim_text)}</p>
      ${amounts ? `<h3>Amounts</h3><p class="no-sum">Each row keeps its metric_type. Do not add overlapping figures.</p>
        <table><thead><tr><th>Amount</th><th>metric_type</th><th>overlap_group</th><th>Period</th><th>Methodology</th></tr></thead><tbody>${amounts}</tbody></table>` : ""}
      ${cl.qualifiers && cl.qualifiers.length ? `<h3>Qualifiers</h3><ul class="rules">${cl.qualifiers.map((q) => `<li>${esc(q)}</li>`).join("")}</ul>` : ""}
      <h3>Supporting passages</h3>
      ${passages ? `<ul class="passages">${passages}</ul>` : "<p class='small muted'>No supporting_passages on this record.</p>"}
      <h3>Sources</h3>
      <ul>${sourceLinks(cl.source_ids) || "<li>None</li>"}</ul>
      ${orgs.length ? `<h3>Organizations</h3><p>${orgs.join(" · ")}</p>` : ""}
      ${cl.editorial_notes ? `<p class="small muted">${esc(cl.editorial_notes)}</p>` : ""}
    `;
  }

  function renderMoney() {
    setNav("money");
    document.title = "Money — MinnesotaPeace research corpus";
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
        const label = filtered[0].overlap_label || key;
        body += `<tr class="group-head"><td colspan="6">${esc(label)} <span class="mono muted">${esc(key)}</span> · do not sum this group</td></tr>`;
        filtered.forEach((r) => {
          shown += 1;
          const cse = caseForDocket(r.case_number);
          body += `<tr>
            <td class="numcell">${esc(formatUsd(r.value, r.exact_or_approximate))}</td>
            <td>${chip(r.metric_type, "metric")}</td>
            <td>${chip(r.evidence_class, "ev-" + (r.evidence_class || ""))}</td>
            <td>${cse ? `<a href="#/cases/${esc(cse.id)}">${esc(cse.short_name)}</a>` : esc(r.case_number || "—")}</td>
            <td><a href="#/claims/${esc(r.claim_id)}">${esc(r.claim_id)}</a></td>
            <td class="small">${esc(r.methodology || "")}</td>
          </tr>`;
        });
      });
      document.getElementById("money-body").innerHTML = body || `<tr><td colspan="6">No rows for this filter.</td></tr>`;
      document.getElementById("money-count").textContent = `${shown} rows shown. This is a count of rows, not a dollar total.`;
    }

    app.innerHTML = `
      <h2>Money</h2>
      <div class="sum-banner">
        <p><strong>Do not sum these rows</strong></p>
        <p>Each row is a sourced figure with a metric_type and an overlap group. amount_billed is not amount_paid is not alleged_loss is not program_spend is not as-filed 990 revenue. Statewide HSS payouts are not case losses. Empire $40M is not added to Bock. Mohamed family $12M is not added to Star $10M or to FOF sponsor recitals. Sallah $1.4M claimed is not added to $1.3M received.</p>
      </div>
      <div class="filters">
        <label>metric_type
          <select id="metric-filter">
            <option value="">All metric types</option>
            ${metrics.map((m) => `<option value="${esc(m)}">${esc(m)}</option>`).join("")}
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
            <th>metric_type</th>
            <th>evidence_class</th>
            <th>Case</th>
            <th>Claim</th>
            <th>Methodology</th>
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
    document.title = "Entities — MinnesotaPeace research corpus";
    const cards = CORPUS.entities.map((e) => `
      <article class="card">
        <p class="meta">${esc(e.entity_type || "")}${e.ein ? " · EIN " + esc(e.ein) : ""}</p>
        <h3><a href="#/entities/${esc(e.entity_id)}">${esc(e.canonical_name)}</a></h3>
        <p class="mono small">${esc(e.entity_id)}</p>
        ${(e.business_reg_ids || []).map((id) => chip(id)).join(" ")}
        ${e.notes ? `<p class="small">${esc(e.notes.slice(0, 220))}${e.notes.length > 220 ? "…" : ""}</p>` : ""}
      </article>
    `).join("");
    app.innerHTML = `
      <h2>Organizations</h2>
      <p class="lede">SOS- and 990-backed entities in this harvest. Feeding Our Future and Feeding Our Future II are separate organizations. Shared street address is not a conspiracy edge.</p>
      <div class="notice"><p><strong>Identity, not guilt</strong> An SOS file or Form 990 is not a charging instrument. Name-match to an indictment is not a conviction.</p></div>
      <div class="card-grid">${cards}</div>
    `;
  }

  function renderEntity(id) {
    setNav("entities");
    const e = entityById(id);
    if (!e) {
      app.innerHTML = `<div class="not-found"><p>No entity <span class="mono">${esc(id)}</span>.</p><p><a href="#/entities">Back to entities</a></p></div>`;
      return;
    }
    document.title = `${e.canonical_name} — MinnesotaPeace research corpus`;
    const claims = CORPUS.claims.filter((c) =>
      (c.organizations || []).includes(id) || (c.subject_ids || []).includes(id)
    );
    const officers = (e.officers || []).map((o) => `
      <tr>
        <td>${esc(o.name)}</td>
        <td>${esc(o.title || "")}</td>
        <td class="small">${esc([o.valid_from, o.valid_until].filter(Boolean).join(" – ") || "—")}</td>
        <td class="mono small">${esc((o.source_ids || []).join(", "))}</td>
      </tr>
    `).join("");
    const addrs = (e.addresses || []).map((a) => `
      <p class="addr">${esc([a.line1, a.line2, a.city, a.state, a.postal_code].filter(Boolean).join(", "))}</p>
    `).join("");
    app.innerHTML = `
      <p class="meta"><a href="#/entities">Entities</a> / ${esc(e.entity_id)}</p>
      <h2>${esc(e.canonical_name)}</h2>
      <div class="chips">
        ${chip(e.entity_type)}
        ${e.ein ? chip("EIN " + e.ein) : ""}
        ${(e.business_reg_ids || []).map((id) => chip(id)).join("")}
        ${(e.aliases || []).map((a) => chip(a)).join("")}
        ${(e.former_names || []).map((a) => chip("former: " + a)).join("")}
      </div>
      ${e.notes ? `<p>${esc(e.notes)}</p>` : ""}
      ${id === "org-feeding-our-future" ? `<p class="small">Kept separate from <a href="#/entities/org-feeding-our-future-ii">Feeding Our Future II</a> (EIN 86-1201700).</p>` : ""}
      ${id === "org-feeding-our-future-ii" ? `<p class="small">Kept separate from <a href="#/entities/org-feeding-our-future">Feeding Our Future</a> (EIN 81-4343304). Shared registered-office vendor is not a merge.</p>` : ""}
      <h3>Addresses</h3>
      ${addrs || "<p class='small muted'>None on this record.</p>"}
      <p class="small muted">Shared address is not conspiracy.</p>
      ${officers ? `<h3>Officers / agents (as sourced)</h3>
        <table><thead><tr><th>Name</th><th>Title</th><th>Valid</th><th>source_ids</th></tr></thead><tbody>${officers}</tbody></table>` : ""}
      <h3>Claims</h3>
      ${claims.length ? `<ul>${claims.map((cl) => `<li><a href="#/claims/${esc(cl.claim_id)}">${esc(cl.claim_id)}</a> · ${chip(cl.evidence_class)} ${esc(cl.claim_text.slice(0, 160))}${cl.claim_text.length > 160 ? "…" : ""}</li>`).join("")}</ul>` : "<p class='small muted'>No claims name this entity_id.</p>"}
      <h3>Sources</h3>
      <ul>${sourceLinks(e.source_ids) || "<li>None</li>"}</ul>
    `;
  }

  function route() {
    if (!CORPUS) {
      app.innerHTML = "<p>Corpus bundle failed to load.</p>";
      return;
    }
    const parts = hashParts();
    const head = parts[0] || "";
    if (!head) return renderIndex();
    if (head === "cases" && !parts[1]) return renderCases();
    if (head === "cases" && parts[1]) return renderCase(parts[1]);
    if (head === "claims" && parts[1]) return renderClaim(parts[1]);
    if (head === "money") return renderMoney();
    if (head === "entities" && !parts[1]) return renderEntities();
    if (head === "entities" && parts[1]) return renderEntity(parts[1]);
    app.innerHTML = `<div class="not-found"><p>No such page.</p><p><a href="#/">Index</a></p></div>`;
  }

  window.addEventListener("hashchange", route);
  route();
})();
