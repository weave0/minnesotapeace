# MN SOS business-entity search — BLOCKED

Date: 2026-08-26

No records were retrieved. Blockers:

1. https://mblsportal.sos.state.mn.us/Business/Search — every attempt (browser and direct request, https and http, HTTP/1.1, TLS 1.2) failed with connection closed during TLS handshake / timeout. Host resolves to 156.98.17.58 but the portal did not serve any page.
2. Fallback https://www.sos.mn.gov/business-liens/search/ — served a Radware bot-manager CAPTCHA page ('We apologize for the inconvenience... solve this CAPTCHA'), hCaptcha 'I am human'. Incident ID logged on page.

A human needs to take the box browser and clear the CAPTCHA, or the portal must be reachable from this network, before any of the 14 names can be searched.

Names queued: Feeding Our Future, Empire Cuisine, Empire Enterprises, Brilliant Minds Services, Liberty Plus, Leo Human Services, Faladcare, Foundation First Services, Masjid Bilol, Masjid Bilal Islamic Center, Partners in Nutrition, Bet On Better Future, ThinkTechAct, Safari Restaurant
