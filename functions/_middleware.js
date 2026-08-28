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
  return context.next();
}
