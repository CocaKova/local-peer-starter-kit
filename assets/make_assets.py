#!/usr/bin/env python3
"""Regenerate the README header art (hero-light.svg, hero-dark.svg). Stdlib only."""
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))

THEMES = {
    "dark": dict(bg="#0d1117", panel="#161b22", line="#30363d", text="#e6edf3", dim="#8b949e", accent="#4fb3bf"),
    "light": dict(bg="#ffffff", panel="#f6f8fa", line="#d0d7de", text="#1f2328", dim="#656d76", accent="#1b6b75"),
}
FONT = "ui-sans-serif, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
ALT = ("local-peer-starter-kit: setup.sh checks for the NVIDIA driver and Docker Compose, writes .env, then docker compose "
       "starts Open WebUI on port 3000, which talks to Ollama on port 11434 and Qdrant on port 6333")


def box(x, y, w, h, label, sub, c, stroke, mono=False):
    fam = MONO if mono else FONT
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{c["panel"]}" stroke="{stroke}" stroke-width="1.5"/>'
            f'<text x="{x + w / 2}" y="{y + h / 2 - 4}" text-anchor="middle" font-family="{fam}" font-size="17" font-weight="600" fill="{c["text"]}">{label}</text>'
            f'<text x="{x + w / 2}" y="{y + h / 2 + 17}" text-anchor="middle" font-family="{FONT}" font-size="12.5" fill="{c["dim"]}">{sub}</text>')


def arrow(x1, y1, x2, y2, color):
    # line plus a head pointing along the line's direction
    a = math.atan2(y2 - y1, x2 - x1)
    bx, by = x2 - 8 * math.cos(a), y2 - 8 * math.sin(a)
    px, py = 5 * -math.sin(a), 5 * math.cos(a)
    return (f'<line x1="{x1}" y1="{y1}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{color}" stroke-width="1.8"/>'
            f'<path d="M{bx + px:.1f},{by + py:.1f} L{x2},{y2} L{bx - px:.1f},{by - py:.1f} Z" fill="{color}"/>')


def port(x, y, w, text, c):
    """Port label in the top-right corner inside a box."""
    return (f'<text x="{x + w - 12}" y="{y + 20}" text-anchor="end" font-family="{MONO}" font-size="12.5" '
            f'font-weight="600" fill="{c["accent"]}">{text}</text>')


def hero(c):
    W, H = 1200, 320
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{ALT}">',
         f'<rect width="{W}" height="{H}" rx="16" fill="{c["bg"]}" stroke="{c["line"]}"/>',
         f'<text x="60" y="78" font-family="{MONO}" font-size="38" font-weight="700" fill="{c["text"]}">local-peer-starter-kit</text>',
         f'<text x="60" y="112" font-family="{FONT}" font-size="18" fill="{c["dim"]}">'
         'Ollama, Open WebUI and Qdrant on your own NVIDIA machine, started by one script.</text>']
    mid = 212
    s.append(box(60, mid - 35, 220, 70, "./setup.sh", "checks driver + Docker, writes .env", c, c["line"], mono=True))
    s.append(arrow(280, mid, 320, mid, c["dim"]))
    s.append(box(320, mid - 35, 200, 70, "docker compose", "pull, then up -d", c, c["line"], mono=True))
    s.append(arrow(520, mid, 560, mid, c["dim"]))
    s.append(box(560, mid - 35, 250, 70, "Open WebUI", "chat in the browser", c, c["accent"]))
    s.append(port(560, mid - 35, 250, ":3000", c))
    # Open WebUI uses Ollama for the models and Qdrant as its RAG vector store
    s.append(arrow(810, mid - 14, 860, mid - 46, c["dim"]))
    s.append(box(860, mid - 80, 280, 62, "Ollama", "runs the models on the GPU", c, c["line"]))
    s.append(port(860, mid - 80, 280, ":11434", c))
    s.append(arrow(810, mid + 14, 860, mid + 46, c["dim"]))
    s.append(box(860, mid + 18, 280, 62, "Qdrant", "vector store for documents (RAG)", c, c["line"]))
    s.append(port(860, mid + 18, 280, ":6333", c))
    s.append("</svg>")
    return "".join(s)


for theme, colors in THEMES.items():
    with open(os.path.join(HERE, f"hero-{theme}.svg"), "w", encoding="utf-8") as f:
        f.write(hero(colors))
print("ok")
