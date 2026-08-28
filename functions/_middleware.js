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
  const isPublicHtml = pathname === "/" || pathname === "/index.html" || pathname === "/record" || pathname === "/record/" || pathname === "/record/index.html";
  if (!isPublicHtml) return response;

  const headers = new Headers(response.headers);
  headers.set("cache-control", "no-store, no-cache, must-revalidate, max-age=0");
  headers.set("pragma", "no-cache");
  headers.set("expires", "0");
  headers.set("x-mnpeace-publication", "context-first-v2");

  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers,
  });
}
