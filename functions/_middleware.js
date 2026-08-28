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
  headers.set("x-mnpeace-publication", "context-first-v3");

  const shouldInjectDiscovery = pathname === "/" || pathname === "/index.html" || pathname === "/record" || pathname === "/record/" || pathname === "/record/index.html";
  const contentType = response.headers.get("content-type") || "";
  if (!shouldInjectDiscovery || !contentType.includes("text/html")) {
    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers,
    });
  }

  const html = await response.text();
  const tag = '<script src="/js/discovery.js" defer></script>';
  const body = html.includes('/js/discovery.js') ? html : html.replace("</body>", tag + "\n</body>");
  headers.delete("content-length");

  return new Response(body, {
    status: response.status,
    statusText: response.statusText,
    headers,
  });
}
