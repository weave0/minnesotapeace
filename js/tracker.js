(function(){
  "use strict";
  var data=null, current=null;
  var $=function(s){return document.querySelector(s)};
  var esc=function(v){return String(v==null?"":v).replace(/[&<>"']/g,function(c){return({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[c]})};
  function sourceMap(){var m={};(data.sources||[]).forEach(function(s){m[s.source_id]=s});return m}
  function sources(ids){var m=sourceMap();return (ids||[]).map(function(id){return m[id]}).filter(Boolean)}
  function sourceLinks(ids){var ss=sources(ids);if(!ss.length)return '<span class="source-inline">No publishable source</span>';return '<span class="source-inline">'+ss.map(function(s){return '<a href="'+esc(s.canonical_url)+'">'+esc(s.issuing_body||s.title||s.source_id)+'</a>'+(s.publication_date?' · '+esc(s.publication_date):'')}).join(' · ')+'</span>'}
  function moneyLabel(c){return({program_spend:"Program spend",amount_billed:"Amount billed",amount_claimed:"Amount claimed",amount_paid:"Amount paid",alleged_loss:"Alleged loss",proven_loss:"Adjudicated amount",restitution_ordered:"Restitution ordered",forfeiture_ordered:"Forfeiture ordered",recovered_amount:"Recovered amount",identified_for_recovery:"Identified for recovery",cost_avoidance:"Cost avoidance",fraud_estimate:"Fraud estimate"})[c]||c}
  function usd(v){if(typeof v!=="number")return "Unknown";return new Intl.NumberFormat("en-US",{style:"currency",currency:"USD",maximumFractionDigits:0}).format(v)}
  function date(v){if(!v)return "Date unknown";return esc(v)}
  function renderNav(){
    var nav=$("#program-nav");nav.innerHTML=(data.programs||[]).map(function(p){return '<button type="button" data-program="'+esc(p.program_id)+'">'+esc(p.name)+'</button>'}).join("");
    nav.addEventListener("click",function(e){var b=e.target.closest("button[data-program]");if(!b)return;select(b.dataset.program,true)});
  }
  function metrics(p){
    if(!(p.legal_metrics||[]).length)return '<div class="unknown-box">No reconciled program-wide legal-stage aggregate is published here. Individual cases and events remain available below.</div>';
    return '<div class="metric-grid">'+p.legal_metrics.map(function(m){var stage=(m.status||"").toLowerCase();return '<article class="metric-card"><div class="metric-value">'+esc(m.value)+'</div><div class="metric-label">'+esc(m.metric_id.replace(/^fof-/,"").replace(/-count$/,"").replace(/-/g," "))+'</div><span class="status-chip '+esc(stage)+'">'+esc(m.status)+'</span><p class="metric-note">'+esc(m.explanation)+'</p>'+sourceLinks(m.source_ids)+'</article>'}).join("")+'</div>'
  }
  function facts(p){
    if(!(p.facts||[]).length)return '<p class="empty">No additional selected canonical facts for this program.</p>';
    return '<div class="card-grid">'+p.facts.map(function(f){return '<article class="fact-card"><span class="status-chip '+esc((f.status||"").toLowerCase())+'">'+esc(f.status||f.evidence_class)+'</span><p>'+esc(f.text)+'</p>'+sourceLinks(f.source_ids)+'</article>'}).join("")+'</div>'
  }
  function money(p){
    var rows=p.money||[];if(!rows.length)return '<p class="empty">No publishable money row in this projection.</p>';
    return '<div class="money-list">'+rows.map(function(r){return '<article class="money-row"><div><div class="money-value">'+usd(r.value)+'</div><div class="money-category">'+esc(moneyLabel(r.category))+'</div></div><div><span class="money-chip">'+esc(r.evidence_class||r.status||"sourced")+'</span></div><div><p class="card-note">'+esc(r.methodology||((r.qualifiers||[])[0])||"Category preserved from canonical record; not added to other rows.")+'</p>'+(r.source_ids?sourceLinks(r.source_ids):'')+'</div></article>'}).join("")+'</div>'
  }
  function cases(p){
    if(!(p.cases||[]).length)return '<p class="empty">No charge-era case bundle is published for this program in The Record.</p>';
    return '<div class="card-grid">'+p.cases.map(function(c){return '<article class="case-card"><span class="status-chip charged">'+esc(c.evidentiary_status||"record")+'</span><h4>'+esc(c.short_name||c.docket)+'</h4><p class="card-note">'+esc(c.docket||"")+' · '+esc(c.instrument||"")+(c.count_n!=null?' · '+esc(c.count_n)+' counts':'')+'</p><p class="card-note">'+esc((c.defendants||[]).length)+' named defendant'+((c.defendants||[]).length===1?'':'s')+' in this filing.</p>'+(c.docket?'<a href="/record/#/cases">Open case record →</a>':'')+sourceLinks(c.source_ids)+'</article>'}).join("")+'</div>'
  }
  function events(p){
    if(!(p.events||[]).length)return '<p class="empty">No later accountability event is published for this program yet.</p>';
    var sorted=p.events.slice().sort(function(a,b){return String(b.occurred_at||"").localeCompare(String(a.occurred_at||""))});
    return '<div class="timeline">'+sorted.map(function(e){return '<article class="event-row"><time class="event-date">'+date(e.occurred_at)+'</time><div><span class="status-chip '+esc((e.legal_stage||e.event_type||"").toLowerCase())+'">'+esc(e.event_type)+'</span><h4>'+esc(e.subject||"Program update")+'</h4><p>'+esc(e.summary)+'</p>'+sourceLinks(e.source_ids)+'</div></article>'}).join("")+'</div>'
  }
  function reforms(p){
    if(!(p.reform_events||[]).length)return '<div class="unknown-box">No reform sequence has enough linked canonical evidence to publish here yet.</div>';
    return '<div class="reform-list">'+p.reform_events.slice().sort(function(a,b){return String(b.event_date||"").localeCompare(String(a.event_date||""))}).map(function(e){return '<article class="reform-row"><time class="event-date">'+date(e.event_date)+'</time><div><span class="state-chip">'+esc(e.implementation_state)+'</span><h4>'+esc(e.actor||"Public agency")+'</h4><p>'+esc(e.summary)+'</p><p class="card-note"><strong>Effectiveness:</strong> '+esc(e.effectiveness||"UNKNOWN")+(e.qualification?' · '+esc(e.qualification):'')+'</p>'+sourceLinks(e.source_ids)+'</div></article>'}).join("")+'</div>'
  }
  function sourceSection(p){
    var ids={};[p.purpose_source_ids,p.legal_metrics.flatMap(function(x){return x.source_ids||[]}),p.facts.flatMap(function(x){return x.source_ids||[]}),p.events.flatMap(function(x){return x.source_ids||[]}),p.reform_events.flatMap(function(x){return x.source_ids||[]})].flat(2).forEach(function(id){if(id)ids[id]=true});
    var ss=sources(Object.keys(ids));if(!ss.length)return "";
    return '<details class="details-toggle section-block"><summary>Sources used on this program card ('+ss.length+')</summary><div class="source-list">'+ss.map(function(s){return '<a href="'+esc(s.canonical_url)+'">'+esc(s.title||s.source_id)+' · '+esc(s.publication_date||s.retrieval_date||"date unknown")+'</a>'}).join("")+'</div></details>'
  }
  function render(p){
    $("#program-view").innerHTML='<section class="program-head"><p class="tracker-label">Program</p><h2>'+esc(p.name)+'</h2><p class="purpose">'+esc(p.purpose)+'</p>'+sourceLinks(p.purpose_source_ids)+'</section>'+
      '<section class="section-block"><div class="section-head"><h3>Legal status</h3><span class="tracker-label">Exact stages only</span></div>'+metrics(p)+'</section>'+
      '<section class="section-block"><div class="section-head"><h3>Money</h3><span class="tracker-label">No cross-category totals</span></div>'+money(p)+'</section>'+
      '<section class="section-block"><div class="section-head"><h3>People & cases</h3><span class="tracker-label">Charging record</span></div>'+cases(p)+facts(p)+'</section>'+
      '<section class="section-block"><div class="section-head"><h3>What changed?</h3><span class="tracker-label">Later events</span></div>'+events(p)+'</section>'+
      '<section class="section-block"><div class="section-head"><h3>Oversight & reform</h3><span class="tracker-label">Announced ≠ implemented ≠ effective</span></div>'+reforms(p)+'</section>'+
      sourceSection(p);
    document.querySelectorAll("#program-nav button").forEach(function(b){b.setAttribute("aria-current",b.dataset.program===p.program_id?"true":"false")});
  }
  function select(id,push){var p=(data.programs||[]).find(function(x){return x.program_id===id})||data.programs[0];if(!p)return;current=p.program_id;if(push){var u=new URL(location.href);u.searchParams.set("program",current);history.pushState({program:current},"",u)}render(p)}
  window.addEventListener("popstate",function(){if(data)select(new URL(location.href).searchParams.get("program"),false)});
  $("#copy-link").addEventListener("click",function(){var u=new URL(location.href);if(current)u.searchParams.set("program",current);navigator.clipboard&&navigator.clipboard.writeText(u.toString());this.textContent="Copied";setTimeout(()=>this.textContent="Copy deep link",1200)});
  fetch("/tracker/data/tracker.json",{cache:"no-store"}).then(function(r){if(!r.ok)throw new Error("tracker data unavailable");return r.json()}).then(function(d){data=d;$("#tracker-meta").innerHTML='<span>Last verified '+esc(data.last_verified||"unknown")+'</span><span>'+esc((data.programs||[]).length)+' program views</span><span>Primary-source linked</span>';renderNav();select(new URL(location.href).searchParams.get("program"),false)}).catch(function(err){var box=$("#tracker-error");box.hidden=false;box.textContent="The tracker data failed closed: "+err.message});
})();