"""Re-map stale figure numbers in an agent's merge folder to the CURRENT fragment numbering.
A pre-existing figure is identified by its caption text (after the number); the group's own new figures
(its assigned high range, minor >= 30) are left alone.
Usage: python remap_figs.py <GROUP> <fragment> [--write]"""
import re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
g, frag = sys.argv[1], sys.argv[2]
write = "--write" in sys.argv
CAP = re.compile(r"<figcaption><b>Fig (\d+\.\d+)</b>(.*?)</figcaption>", re.S)
norm = lambda t: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t)).strip()

cur = (HERE / "frag" / f"{frag}.html").read_text(encoding="utf-8")
by_caption = {}
for num, text in CAP.findall(cur):
    by_caption.setdefault(norm(text), num)

bad = 0
for f in sorted((HERE / "tmp" / "merge" / g).glob("*.html")):
    s = f.read_text(encoding="utf-8")
    mapping = {}
    for num, text in CAP.findall(s):
        if int(num.split(".")[1]) >= 30:
            continue                      # the group's own new figure
        new = by_caption.get(norm(text))
        if new is None:
            bad += 1
            print(f"  UNMATCHED {f.name}: Fig {num} {norm(text)[:70]}")
        else:
            mapping[num] = new
    changed = {k: v for k, v in mapping.items() if k != v}
    if changed:
        s = re.sub(r"Fig (\d+\.\d+)(?![\d.])", lambda m: "Fig " + mapping.get(m.group(1), m.group(1)), s)
        print(f"  {f.name}: {changed}")
        if write:
            f.write_text(s, encoding="utf-8")
print("unmatched:", bad)
sys.exit(1 if bad else 0)
