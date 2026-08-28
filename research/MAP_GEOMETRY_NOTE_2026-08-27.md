# Minnesota good-work map geometry note — 2026-08-27

## Why this note exists

The first `/good/` statewide map used a hand-built decorative silhouette. It was intentionally labeled schematic, but the outline was not recognizably Minnesota enough for publication.

## Replacement geometry

The v6.1 public response uses a simplified path derived from real Minnesota boundary coordinates rather than an invented blob. Reference geometry consulted during the correction:

- Public Minnesota GeoJSON: `https://raw.githubusercontent.com/glynnbird/usstatesgeojson/master/minnesota.geojson`
- CC0 visual cross-check: Wikimedia Commons, `Simple Rounded Outline of the state of Minnesota.svg`

The simplified path preserves the features necessary for immediate recognition at small display sizes:

- the long Iowa border
- the comparatively straight South Dakota border
- the Red River / North Dakota western edge
- the Northwest Angle above the 49th parallel
- the northern lake/border contour
- the Arrowhead and Lake Superior shoreline
- the Wisconsin / Mississippi River eastern boundary

The map remains an editorial locator, not a GIS layer.

## Marker placement

Pins are placed by approximate city longitude/latitude projected into the same simplified map coordinate system:

1. Bemidji
2. Keewatin
3. Moorhead
4. Detroit Lakes
5. Duluth
6. St. Cloud
7. Wyoming
8. Belle Plaine
9. Red Wing
10. Mankato
11. Rochester
12. Fairmont

No pin implies a precise project street address; it locates the named Minnesota community.
