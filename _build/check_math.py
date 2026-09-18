"""Per-fragment math check: KaTeX-render ONE fragment, report errors, leftover plain-text maths and control chars.
Usage: python check_math.py ml-u2"""
import re, subprocess, sys, html
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
stem = sys.argv[1]
src = HERE / "frag" / f"{stem}.html"
out = HERE / "tmp" / f"mathcheck-{stem}.html"
s = src.read_text(encoding="utf-8")
bad = 0

ctrl = [(m.start(), repr(m.group())) for m in re.finditer(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", s)]
if ctrl:
    bad += 1
    print("CONTROL CHARS (eaten backslashes):", ctrl[:10])

r = subprocess.run(["node", str(HERE / "render_math.mjs"), str(src), str(out)], capture_output=True, text=True)
if r.returncode:
    bad += 1
    print("KATEX FAIL:", "\n".join(l for l in r.stderr.splitlines() if "KaTeX" in l or "source:" in l or "unpaired" in l)[:800])
else:
    print(r.stdout.strip())

# leftover plain-text maths outside svg/pre/code and outside $...$
t = re.sub(r"<(svg|pre|code)\b.*?</\1>", " ", s, flags=re.S)
t = re.sub(r"\$\$.*?\$\$", " ", t, flags=re.S)
t = re.sub(r"\$[^$\n]*\$", " ", t)
t = html.unescape(re.sub(r"<[^>]+>", " ", t))
hits = []
for pat in [r"[Σ∑√∏∂]", r"[₀-₉]", r"[²³⁻¹]", r"x̄|ȳ|ŷ|ŝ", r"\b\w+\s*=\s*[\d(]"]:
    for m in re.finditer(pat, t):
        hits.append(t[max(0, m.start() - 40): m.start() + 40].replace("\n", " "))
if hits:
    print(f"POSSIBLE PLAIN-TEXT MATH ({len(hits)}), review each:")
    for h in hits[:40]:
        print("   …" + h + "…")
sys.exit(1 if bad else 0)
