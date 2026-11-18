"""Generate the themed SVG assets for the GitHub profile README (dark + light)."""
import math
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

THEMES = {
    "dark": dict(bg="#0D0F14", line="#232733", text="#ECEEF2", muted="#9098A9",
                 faint="#2A2F3B", accent="#FF7A45", accent_soft="#FF7A4522"),
    "light": dict(bg="#FBFAF7", line="#E4E0D6", text="#14161B", muted="#565D6B",
                  faint="#DCD7CB", accent="#D9480F", accent_soft="#D9480F1A"),
}
SANS = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"


def banner(t):
    W, H = 1200, 360
    cx, cy, R = 935, 178, 108
    labels = ["retrieve", "rerank", "guard", "reason", "verify"]
    nodes = []
    for i, lab in enumerate(labels):
        a = math.radians(-90 + i * 72)
        nodes.append((cx + R * math.cos(a), cy + R * math.sin(a), lab))

    edges, packets, sats = [], [], []
    for i, (x, y, lab) in enumerate(nodes):
        edges.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="{t["faint"]}" stroke-width="1.5"/>')
        nx, ny = nodes[(i + 1) % 5][:2]
        edges.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{nx:.1f}" y2="{ny:.1f}" stroke="{t["line"]}" stroke-width="1" stroke-dasharray="3 5"/>')
        dur = 2.4 + i * 0.35
        packets.append(
            f'<circle r="3" fill="{t["accent"]}"><animateMotion dur="{dur:.2f}s" repeatCount="indefinite" '
            f'path="M{cx},{cy} L{x:.1f},{y:.1f}"/></circle>')
        lx = x + (16 if x > cx + 5 else -16 if x < cx - 5 else 0)
        anchor = "start" if x > cx + 5 else "end" if x < cx - 5 else "middle"
        ly = y - 16 if y < cy - 60 else y + 5 if abs(y - cy) < 60 else y + 24
        sats.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="{t["bg"]}" stroke="{t["muted"]}" stroke-width="1.5"/>')
        sats.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}" class="mono small">{lab}</text>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Chaitanya Panchal, AI Engineer, building RAG systems and agentic workflows">
<style>
  .sans {{ font-family: {SANS}; }}
  .mono {{ font-family: {MONO}; fill: {t["muted"]}; }}
  .small {{ font-size: 13px; letter-spacing: .02em; }}
  .pulse {{ animation: pulse 2.4s ease-in-out infinite; transform-origin: 66px 62px; }}
  .halo {{ animation: halo 3s ease-in-out infinite; transform-origin: {cx}px {cy}px; }}
  @keyframes pulse {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: .25; }} }}
  @keyframes halo {{ 0%,100% {{ transform: scale(1); opacity: .9; }} 50% {{ transform: scale(1.35); opacity: .25; }} }}
  @media (prefers-reduced-motion: reduce) {{ .pulse, .halo {{ animation: none; }} }}
</style>
<defs>
  <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">
    <circle cx="2" cy="2" r="1" fill="{t["line"]}"/>
  </pattern>
</defs>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="18" fill="{t["bg"]}" stroke="{t["line"]}"/>
<rect x="760" y="1" width="439" height="{H-2}" fill="url(#dots)" opacity=".9"/>

<circle class="pulse" cx="66" cy="62" r="5" fill="{t["accent"]}"/>
<text x="82" y="67" class="mono small">open to AI engineering roles · toronto, on</text>

<text x="56" y="158" class="sans" font-size="66" font-weight="700" letter-spacing="-1.5" fill="{t["text"]}">Chaitanya Panchal</text>
<text x="58" y="208" class="sans" font-size="26" font-weight="600" fill="{t["accent"]}">AI Engineer<tspan fill="{t["text"]}" font-weight="400"> — RAG systems, agents, and the data under them.</tspan></text>
<text x="58" y="246" class="sans" font-size="18" fill="{t["muted"]}">I build LLM applications that cite their sources, pass their evals, and keep a human in the loop.</text>

<line x1="58" y1="290" x2="700" y2="290" stroke="{t["line"]}"/>
<text x="58" y="320" class="mono small">LangGraph · MCP · hybrid retrieval · RAGAS evals · guardrails · FastAPI · PySpark</text>

{''.join(edges)}
{''.join(packets)}
<circle class="halo" cx="{cx}" cy="{cy}" r="22" fill="{t["accent_soft"]}"/>
<circle cx="{cx}" cy="{cy}" r="11" fill="{t["accent"]}"/>
{''.join(sats)}
<text x="{cx}" y="{cy + 40}" text-anchor="middle" class="mono small">coordinator</text>
</svg>
'''


METRICS = [
    ("~85%", "faster legal research", "vs manual · 1.1s P50"),
    ("0.94", "RAGAS context precision", "up from 0.62"),
    ("0.95", "answer faithfulness", "up from 0.78"),
    ("&lt;1.2%", "false refusals", "PII + injection guardrails"),
]


def impact(t):
    W, H = 1200, 220
    col = (W - 112) / 4
    cells = []
    for i, (big, label, ctx) in enumerate(METRICS):
        x = 56 + i * col
        if i:
            cells.append(f'<line x1="{x - 24:.0f}" y1="78" x2="{x - 24:.0f}" y2="186" stroke="{t["line"]}"/>')
        cells.append(
            f'<text x="{x:.0f}" y="132" class="sans" font-size="48" font-weight="700" letter-spacing="-1" fill="{t["accent"]}">{big}</text>'
            f'<text x="{x:.0f}" y="160" class="sans" font-size="17" font-weight="600" fill="{t["text"]}">{label}</text>'
            f'<text x="{x:.0f}" y="183" class="mono small">{ctx}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Production impact: about 85 percent faster legal research, RAGAS context precision 0.62 to 0.94, faithfulness 0.78 to 0.95, under 1.2 percent false refusals">
<style>
  .sans {{ font-family: {SANS}; }}
  .mono {{ font-family: {MONO}; fill: {t["muted"]}; }}
  .small {{ font-size: 13px; letter-spacing: .02em; }}
</style>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="18" fill="{t["bg"]}" stroke="{t["line"]}"/>
<text x="56" y="52" class="mono small" fill="{t["muted"]}">PRODUCTION RAG PLATFORM — KRAFTBASE, 2025–26</text>
{''.join(cells)}
</svg>
'''


for name, t in THEMES.items():
    (OUT / f"banner-{name}.svg").write_text(banner(t))
    (OUT / f"impact-{name}.svg").write_text(impact(t))
print("wrote", sorted(p.name for p in OUT.iterdir()))
