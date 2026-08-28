#!/usr/bin/env python3
"""Generate the public MN Peace Open Graph card using only the Python stdlib."""

from __future__ import annotations

import struct
import sys
import zlib
from pathlib import Path

W, H = 1200, 630
BG = (6, 8, 12)
CYAN = (103, 229, 239)
GOLD = (226, 181, 87)
WHITE = (239, 244, 247)
MUTED = (119, 132, 141)

PIXEL_FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "C": ("01111", "10000", "10000", "10000", "10000", "10000", "01111"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
}


def blend(a: int, b: int, t: float) -> int:
    return int(a + (b - a) * t)


def rect(buf: bytearray, x0: int, y0: int, x1: int, y1: int, color: tuple[int, int, int]) -> None:
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(W, x1), min(H, y1)
    for y in range(y0, y1):
        row = y * W * 3
        for x in range(x0, x1):
            i = row + x * 3
            buf[i : i + 3] = bytes(color)


def line(buf: bytearray, points: list[tuple[int, int]], color: tuple[int, int, int], width: int = 2) -> None:
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        dx, dy = x1 - x0, y1 - y0
        steps = max(abs(dx), abs(dy), 1)
        for n in range(steps + 1):
            x = int(x0 + dx * n / steps)
            y = int(y0 + dy * n / steps)
            rect(buf, x - width // 2, y - width // 2, x + width // 2 + 1, y + width // 2 + 1, color)


def glyph(buf: bytearray, ch: str, x: int, y: int, scale: int, color: tuple[int, int, int]) -> int:
    rows = PIXEL_FONT[ch]
    for ry, row in enumerate(rows):
        for rx, bit in enumerate(row):
            if bit == "1":
                rect(buf, x + rx * scale, y + ry * scale, x + (rx + 1) * scale, y + (ry + 1) * scale, color)
    return 6 * scale


def text_peace(buf: bytearray, x: int, y: int, scale: int) -> None:
    for ch in "PEACE":
        x += glyph(buf, ch, x, y, scale, WHITE)


def png_chunk(kind: bytes, data: bytes) -> bytes:
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)


def write_png(path: Path, buf: bytearray) -> None:
    raw = bytearray()
    stride = W * 3
    for y in range(H):
        raw.append(0)
        start = y * stride
        raw.extend(buf[start : start + stride])
    payload = b"\x89PNG\r\n\x1a\n"
    payload += png_chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
    payload += png_chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    payload += png_chunk(b"IEND", b"")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def build(path: Path) -> None:
    buf = bytearray(W * H * 3)
    for y in range(H):
        for x in range(W):
            # restrained cyan-left / gold-right atmosphere over near-black
            left = max(0.0, 1.0 - ((x - 130) ** 2 + (y - 180) ** 2) ** 0.5 / 520)
            right = max(0.0, 1.0 - ((x - 1040) ** 2 + (y - 460) ** 2) ** 0.5 / 620)
            r = min(255, BG[0] + int(18 * left + 34 * right))
            g = min(255, BG[1] + int(48 * left + 27 * right))
            b = min(255, BG[2] + int(54 * left + 7 * right))
            i = (y * W + x) * 3
            buf[i : i + 3] = bytes((r, g, b))

    # Monumental MN monogram.
    rect(buf, 92, 112, 122, 352, WHITE)
    rect(buf, 266, 112, 296, 352, WHITE)
    line(buf, [(112, 126), (194, 260), (276, 126)], WHITE, 29)
    rect(buf, 358, 112, 388, 352, CYAN)
    rect(buf, 538, 112, 568, 352, CYAN)
    line(buf, [(380, 124), (548, 340)], CYAN, 29)

    # PEACE wordmark in deliberately geometric display lettering.
    text_peace(buf, 650, 150, 24)

    # River/evidence lines.
    for i in range(7):
        y = 430 + i * 17
        line(buf, [(-20, y + 18), (180, y - 7), (390, y + 5), (610, y - 15), (820, y + 7), (1030, y - 13), (1220, y + 8)], CYAN, max(1, 5 - i // 2))
    for i in range(4):
        y = 530 + i * 15
        line(buf, [(50, y), (1160, y - 27)], GOLD, 1)

    # Four evidence blocks: case status, systems, oversight, civic repair.
    x = 92
    for width in (166, 222, 150, 178):
        rect(buf, x, 565, x + width, 571, MUTED)
        rect(buf, x, 576, x + width - 25, 582, GOLD if x > 500 else CYAN)
        x += width + 28

    write_png(path, buf)


if __name__ == "__main__":
    output = Path(sys.argv[1] if len(sys.argv) > 1 else "assets/og/mn-peace-og-v2.png")
    build(output)
    print(output)
