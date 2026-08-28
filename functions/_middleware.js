export async function onRequest(context) {
  const { pathname } = new URL(context.request.url);

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
  ]);
  const isPublicHtml = publicHtmlPaths.has(pathname);
  if (!isPublicHtml) return response;

  const headers = new Headers(response.headers);
  headers.set("cache-control", "no-store, no-cache, must-revalidate, max-age=0");
  headers.set("pragma", "no-cache");
  headers.set("expires", "0");
  headers.set("x-mnpeace-publication", "context-first-v5");

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

  const tag = '<script src="/js/discovery.js" defer></script>';
  if (!body.includes('/js/discovery.js')) body = body.replace("</body>", tag + "\n</body>");
  headers.delete("content-length");

  return new Response(body, {
    status: response.status,
    statusText: response.statusText,
    headers,
  });
}
