export async function onRequest(context) {
  const requestUrl = new URL(context.request.url);
  const { pathname, hostname } = requestUrl;

  // Retire the inherited Pages development hostname without rebuilding the project.
  // Preserve path/query while permanently canonicalizing visitors and crawlers to MN Peace.
  if (hostname === "jamie-mediation.pages.dev") {
    requestUrl.protocol = "https:";
    requestUrl.hostname = "minnesotapeace.com";
    requestUrl.port = "";
    return Response.redirect(requestUrl.toString(), 308);
  }

  if (pathname === "/research" || pathname.startsWith("/research/")) {
    return new Response("Not found", {
      status: 404,
      headers: {
        "content-type": "text/plain; charset=utf-8",
        "cache-control": "no-store",
      },
    });
  }

  const response = await context.next();
  const publicHtmlPaths = new Set([
    "/",
    "/index.html",
    "/record",
    "/record/",
    "/record/index.html",
    "/status",
    "/status/",
    "/status/index.html",
    "/good",
    "/good/",
    "/good/index.html",
    "/guide",
    "/guide/",
    "/guide/index.html",
    "/oversight",
    "/oversight/",
    "/oversight/index.html",
    "/programs",
    "/programs/",
    "/programs/index.html",
    "/money",
    "/money/",
    "/money/index.html",
    "/authority",
    "/authority/",
    "/authority/index.html",
  ]);
  const isPublicHtml = publicHtmlPaths.has(pathname);
  if (!isPublicHtml) return response;

  const headers = new Headers(response.headers);
  headers.set("cache-control", "no-store, no-cache, must-revalidate, max-age=0");
  headers.set("pragma", "no-cache");
  headers.set("expires", "0");
  headers.set("x-mnpeace-publication", "context-first-v6");

  const contentType = response.headers.get("content-type") || "";
  if (!contentType.includes("text/html")) {
    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers,
    });
  }

  let body = await response.text();
  const isHome = pathname === "/" || pathname === "/index.html";
  const isGood = pathname === "/good" || pathname === "/good/" || pathname === "/good/index.html";

  // Social crawlers cache image URLs aggressively. The original OG filename contained a
  // legacy pre-MN-Peace binary even after the page copy was rebuilt for this publication.
  // Rewrite every public HTML response to a clean, versioned MN Peace asset so old social
  // caches cannot continue to attach the unrelated image to current pages or deep links.
  const socialImage = "https://minnesotapeace.com/assets/og/mn-peace-og-v2.png";
  body = body
    .replaceAll("https://minnesotapeace.com/assets/og/mn-peace-og.jpg", socialImage)
    .replace(
      /<meta property="og:image:alt" content="[^"]*">/g,
      '<meta property="og:image:alt" content="MN Peace editorial card with a geometric Minnesota monogram and cyan-and-gold evidence lines">'
    );

  if (!body.includes('name="twitter:image"')) {
    body = body.replace(
      '<meta name="twitter:card" content="summary_large_image">',
      '<meta name="twitter:card" content="summary_large_image">\n  <meta name="twitter:image" content="' + socialImage + '">'
    );
  }

  // The narrative homepage is comparatively stable; aggregate legal milestones are not.
  // Rewrite each stale field independently so harmless whitespace/layout changes cannot
  // prevent a newer official ordinal from reaching crawlers or no-JS readers.
  if (isHome) {
    body = body
      .replace(/77 defendants had been charged/g, "78 defendants had been charged")
      .replace(/<p class="status-value">\s*77\s*<\/p>/, '<p class="status-value">78</p>')
      .replace(/Feeding Our Future defendants charged by Nov\. 20, 2025/g, "Feeding Our Future defendants charged by Nov. 24, 2025")
      .replace(/DOJ called the investigation the largest COVID-19 fraud scheme in the country\./g, "DOJ identified Abdirashid Bixi Dool as the 78th defendant charged. Charges remain allegations until resolved.")
      .replace(/https:\/\/www\.justice\.gov\/usao-mn\/pr\/77th-defendant-charged-feeding-our-future-fraud-scheme/g, "https://www.justice.gov/usao-mn/pr/78th-defendant-charged-feeding-our-future-fraud-scheme");
  }

  // Keep the civic-results page current at the publication edge while preserving the
  // research/static-source distinction. Claims are promoted only where a local or primary
  // source documents actual service or a recurring program; scheduled/funded work stays labeled.
  if (isGood) {
    body = body
      .replace(/Updated Aug\. 27, 2026/g, "Updated Aug. 28, 2026")
      .replace(
        '<div class="map-story-index">2</div><div><div class="map-story-top"><span class="map-story-place">Keewatin</span><span class="map-story-type">Funding approved · 2025</span></div><h3>A police-community grant aimed at school snacks and clothing.</h3><p>The Minnesota Chiefs of Police Foundation’s 2025 recipient list names the Keewatin Police Department’s “School Snack and Clothing Drive.” The source establishes approved grant support; it does not, by itself, establish final participation or distribution totals.</p><div class="map-story-links"><a href="https://www.mnchiefs.org/news/c-notes-10-31-25">MCPA · grant recipient list →</a></div></div>',
        '<div class="map-story-index">2</div><div><div class="map-story-top"><span class="map-story-place">Keewatin</span><span class="map-story-type">Reported student support · 2025–26 school year</span></div><h3>The Spartan Care Closet is stocked by a wider community.</h3><p>Nashwauk-Keewatin Schools says students have access to essential items and snacks through the Spartan Care Closet. The district reported that Keewatin Police Chief Chris Whitney helped secure $4,850 in grants and donations from the Minnesota Chiefs of Police Foundation, Greenway Lions Club, Nashwauk Fire Relief, Keewatin Legion, Amvets, Hibbing Walmart and local residents.</p><div class="map-story-links"><a href="https://www.isd319.org/article/2533866">Nashwauk-Keewatin Schools · Spartan Care Closet →</a><a href="https://www.mnchiefs.org/news/c-notes-10-31-25">MCPA · 2025 grant recipient list →</a></div></div>'
      )
      .replace(
        '<div class="map-story-index">8</div><div><div class="map-story-top"><span class="map-story-place">Belle Plaine</span><span class="map-story-type">Funding approved · 2025</span></div><h3>Hook, Line, and Heroes: a youth river fishing derby.</h3><p>The Belle Plaine Police Department was approved for 2025 MCPF support for a youth river fishing derby. It sits in the same statewide grant portfolio as youth academies, sports mentorship and community safety programs.</p><div class="map-story-links"><a href="https://www.mnchiefs.org/news/c-notes-10-31-25">MCPA · grant recipient list →</a></div></div>',
        '<div class="map-story-index">8</div><div><div class="map-story-top"><span class="map-story-place">Belle Plaine</span><span class="map-story-type">Locally documented event · Aug. 16, 2025</span></div><h3>Hook, Line and Heroes reached the city calendar.</h3><p>Belle Plaine’s official calendar lists the Hook, Line and Heroes fishing event for August 16, 2025, after the city accepted donations for the youth event and MCPF approved grant support. The city record establishes the local event and funding trail; this page does not invent attendance or outcome totals.</p><div class="map-story-links"><a href="https://www.belleplainemn.gov/calendar.aspx?day=16&month=8&view=list&year=2025">City of Belle Plaine · 2025 event calendar →</a><a href="https://www.mnchiefs.org/news/c-notes-10-31-25">MCPA · 2025 grant recipient list →</a></div></div>'
      )
      .replace(
        '<div class="map-story-index">9</div><div><div class="map-story-top"><span class="map-story-place">Red Wing</span><span class="map-story-type">Funding approved · 2025</span></div><h3>A bike rodeo framed as community partnership.</h3><p>MCPF’s 2025 slate includes the Red Wing Police Department’s Bike Rodeo. The source establishes grant approval and program identity; MN Peace will add execution and participation figures only when a local or primary source documents them.</p><div class="map-story-links"><a href="https://www.mnchiefs.org/news/c-notes-10-31-25">MCPA · grant recipient list →</a></div></div>',
        '<div class="map-story-index">9</div><div><div class="map-story-top"><span class="map-story-place">Red Wing</span><span class="map-story-type">Annual city program · documented 2024–26</span></div><h3>Bike safety is a recurring police-community event.</h3><p>Red Wing describes its Bike Rodeo as an annual spring event where children practice riding skills on a simulated road course. The Police Department’s 2024 accomplishment report lists Bike Rodeo among community-engagement events held that year, and the city calendared the event again for 2026.</p><div class="map-story-links"><a href="https://www.redwingmn.gov/256/Other-Red-Wing-Police-Crime-Prevention-P">City of Red Wing · annual Bike Rodeo →</a><a href="https://www.redwingmn.gov/DocumentCenter/View/3994/2024-Police-Department-Accomplishment-Report-PDF">Red Wing Police · 2024 accomplishments →</a></div></div>'
      );

    const ruralSection = `
    <section class="deep-section rural-results" id="greater-minnesota-neighbors">
      <div class="deep-wrap">
        <div class="deep-section-head">
          <div><p class="deep-kicker">04B · Greater Minnesota</p><h2>Neighbor-to-neighbor work is not a police category.</h2></div>
          <p>Food shelves, volunteers and local public-private partnerships are doing measurable work beyond the Twin Cities. These examples are here for the act itself; no partisan identity is inferred from a community, donor, volunteer or recipient.</p>
        </div>
        <div class="good-grid">
          <article class="good-card featured">
            <div class="good-card-top"><span class="good-tag">Food access · nonprofit</span><span class="good-place">Bemidji</span></div>
            <h3>891,576 pounds of food distributed in 2025.</h3>
            <p>Bemidji Community Food Shelf reports 13,063 visits, 41,576 individuals served and 891,576 pounds of food distributed in 2025. More than 500 volunteers support the food shelf, warehouse and its 3.5-acre community farm.</p>
            <p class="example-line">The organization describes itself as faith-based and inclusive, serving people experiencing food insecurity in Beltrami County and the Bemidji School District.</p>
            <a class="story-source" href="https://www.bcfsmn.org/">Bemidji Community Food Shelf · 2025 impact →</a>
          </article>
          <article class="good-card">
            <div class="good-card-top"><span class="good-tag">Food access · nonprofit</span><span class="good-place">Mankato</span></div>
            <h3>About 160,000 pounds of food to 1,700 households each month.</h3>
            <p>ECHO Food Shelf says it currently distributes about 160,000 pounds of food each month to roughly 1,700 households in the Mankato area. Its services include client-choice groceries, ready-to-eat food for people without storage or cooking facilities, summer food for children and Thanksgiving meal baskets.</p>
            <a class="story-source" href="https://www.echofoodshelf.org/">ECHO Food Shelf · current programs and scale →</a>
          </article>
          <article class="good-card">
            <div class="good-card-top"><span class="good-tag">Food access · county + nonprofit</span><span class="good-place">Olmsted County</span></div>
            <h3>235,000 pounds of food. 3,900 neighbors. 361 volunteers.</h3>
            <p>During the November 2025 federal shutdown, Olmsted County reports that a $200,000 county contribution helped Channel One Food Bank distribute three food boxes per household to people facing food insecurity. The county says the November 7 distribution moved 235,000 pounds of food to 3,900 neighbors with help from 361 volunteers.</p>
            <a class="story-source" href="https://www.olmstedcounty.gov/government/county-news-events/county-news/partnering-provide-food-those-need">Olmsted County · distribution results →</a>
          </article>
          <article class="good-card">
            <div class="good-card-top"><span class="good-tag faith">Catholic · food access</span><span class="good-place">Central Minnesota</span></div>
            <h3>More than 2.6 million pounds of food in 2025.</h3>
            <p>Catholic Charities of the Diocese of St. Cloud reports that its Food Shelf provided more than 2.6 million pounds of food in 2025 and served more than 20,000 people. Its March 2026 Pack the Porches drive added 6,615 pounds of donated food and $24,665 in cash support.</p>
            <p class="example-line">The Catholic identity is disclosed because the organization makes it part of its mission; the measurable service is why it appears here.</p>
            <div class="purpose-links"><a class="story-source" href="https://www.ccstcloud.org/annual-report">Catholic Charities · 2025 annual report →</a><a class="story-source" href="https://www.ccstcloud.org/pack-the-porches-2026">Pack the Porches · 2026 results →</a></div>
          </article>
        </div>
      </div>
    </section>
`;

    if (!body.includes('id="greater-minnesota-neighbors"')) {
      body = body.replace('\n    <section class="deep-section" id="republican">', ruralSection + '\n    <section class="deep-section" id="republican">');
    }
  }

  // Version the discovery asset path. Static asset caches can outlive a Pages deployment
  // when a zone-level purge is unavailable; a content-versioned URL makes each public
  // release independently verifiable without depending on purge permission.
  const discoveryTag = '<script src="/js/discovery-v7.js" defer></script>';
  if (!body.includes('/js/discovery-v7.js')) body = body.replace("</body>", discoveryTag + "\n</body>");

  // The first statewide story-map outline was too schematic. v6.1 replaces its geometry
  // at the publication edge with a boundary-derived Minnesota silhouette and projected
  // city locations, while retaining the same accessible story links.
  if (isGood) {
    const mapTag = '<script src="/js/good-map-v61.js" defer></script>';
    if (!body.includes('/js/good-map-v61.js')) body = body.replace("</body>", mapTag + "\n</body>");
  }

  headers.delete("content-length");

  return new Response(body, {
    status: response.status,
    statusText: response.statusText,
    headers,
  });
}
