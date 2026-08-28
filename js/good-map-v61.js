/* MN Peace good-work map v6.1 — boundary-derived Minnesota silhouette and city-coordinate pins. */
(function () {
  "use strict";

  var map = document.querySelector("#across-minnesota .field-map svg");
  if (!map) return;

  var outline = map.querySelector(".mn-outline");
  if (outline) {
    outline.setAttribute("d", "M 344.5 327.0 L 330.5 395.0 L 315.8 407.4 L 306.0 432.2 L 317.3 451.9 L 312.5 478.1 L 312.4 499.0 L 310.5 526.2 L 320.6 537.1 L 338.4 551.5 L 357.2 565.7 L 370.7 589.7 L 386.8 603.5 L 396.3 624.6 L 398.8 654.8 L 344.1 654.8 L 299.1 654.9 L 245.4 654.9 L 188.4 654.8 L 121.3 654.8 L 107.2 654.8 L 107.2 603.2 L 107.2 557.7 L 107.2 509.1 L 107.2 481.2 L 107.1 468.7 L 98.0 457.7 L 84.9 437.6 L 90.9 427.3 L 100.7 408.1 L 100.2 378.9 L 97.2 359.9 L 91.2 340.3 L 87.7 312.5 L 86.5 293.9 L 86.0 268.6 L 84.9 241.6 L 77.8 208.9 L 71.8 183.7 L 68.5 169.8 L 70.3 156.4 L 68.6 148.8 L 69.6 136.1 L 67.6 133.6 L 71.6 119.4 L 65.6 98.8 L 64.0 86.4 L 109.8 86.5 L 167.6 86.6 L 179.5 86.6 L 179.6 67.4 L 179.6 46.8 L 181.1 48.3 L 184.8 50.0 L 188.7 48.4 L 193.2 50.3 L 197.9 54.6 L 199.4 66.1 L 202.0 76.2 L 202.0 86.5 L 205.8 98.5 L 207.8 112.3 L 214.1 117.4 L 222.1 116.3 L 229.8 119.2 L 240.9 123.3 L 252.7 124.9 L 262.6 136.5 L 273.5 133.4 L 285.3 123.4 L 294.6 125.0 L 314.6 134.1 L 320.4 136.8 L 329.8 147.0 L 338.8 161.3 L 352.1 152.7 L 362.6 167.3 L 371.9 174.9 L 383.7 182.8 L 397.0 181.1 L 408.9 170.3 L 419.4 164.6 L 424.7 180.4 L 434.8 178.8 L 447.4 180.1 L 456.7 178.2 L 465.3 181.1 L 472.3 191.1 L 480.5 187.4 L 490.8 189.5 L 495.0 188.3 L 490.4 193.2 L 481.6 197.6 L 474.7 202.9 L 465.8 208.3 L 456.1 212.8 L 445.1 216.6 L 434.0 222.8 L 418.2 235.6 L 409.6 245.1 L 401.4 255.3 L 391.2 271.2 L 378.9 283.9 L 369.8 294.9 L 359.9 305.2 L 351.9 312.8 L 349.9 315.1 L 351.6 319.5 L 353.8 323.6 L 350.2 319.1 L 345.7 321.5 L 344.3 323.2 L 344.2 323.9 L 344.7 326.3 Z");
  }

  var water = map.querySelector(".mn-water");
  if (water) water.remove();

  var pins = {
    "#map-bemidji": [194.8, 244.6],
    "#map-keewatin": [292.3, 251.8],
    "#map-moorhead": [89.5, 306.6],
    "#map-detroit-lakes": [140.8, 311.8],
    "#map-duluth": [349.6, 314.9],
    "#map-stcloud": [234.9, 442.0],
    "#map-wyoming": [299.7, 465.1],
    "#map-belle-plaine": [256.7, 538.8],
    "#map-red-wing": [325.5, 544.7],
    "#map-mankato": [243.9, 586.2],
    "#map-rochester": [329.4, 601.9],
    "#map-fairmont": [218.1, 639.0]
  };

  Object.keys(pins).forEach(function (href) {
    var pin = map.querySelector('a[href="' + href + '"]');
    if (!pin) return;
    var x = pins[href][0];
    var y = pins[href][1];
    pin.querySelectorAll("circle").forEach(function (circle) {
      circle.setAttribute("cx", x);
      circle.setAttribute("cy", y);
    });
    var text = pin.querySelector("text");
    if (text) {
      text.setAttribute("x", x);
      text.setAttribute("y", y);
    }
  });

  var desc = map.querySelector("#good-map-desc");
  if (desc) desc.textContent = "Minnesota outline derived from state boundary coordinates with numbered community markers for Bemidji, Keewatin, Moorhead, Detroit Lakes, Duluth, St. Cloud, Wyoming, Belle Plaine, Red Wing, Mankato, Rochester and Fairmont.";

  var key = document.querySelector("#across-minnesota .map-key span");
  if (key) key.innerHTML = "Community locations · boundary-derived state outline<br>Tap a number to open its source note";
})();
