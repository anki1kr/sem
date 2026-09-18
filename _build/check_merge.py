"""Merge agent outputs from tmp/merge/<GROUP>/ into ml-u2.
  python check_merge.py A          -> dry run for group A (temp file only), prints checks
  python check_merge.py A B --write -> real merge into frag/ml-u2.html + renumber h3 / figures / Q&A
"""
import re, sys, subprocess
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from build import Balance  # noqa: E402
import check_numbers  # noqa: E402

RANGES = {"A": (30, 49), "B": (50, 69), "C": (30, 49), "D": (50, 69), "E": (50, 69), "F": (70, 89),
          "G": (30, 49), "H": (50, 69), "I": (30, 49), "J": (50, 69), "K": (30, 49), "L": (50, 69),
          "M": (50, 69), "N": (50, 69), "O": (70, 89)}
args = [a for a in sys.argv[1:] if not a.startswith("--")]
FRAG = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--frag=")), "ml-u2")
UNIT = FRAG[-1]            # "1" or "2": figures, headings and Q&A ids are per unit
MATH = FRAG.split("-")[0] in ("ml", "speech")
write = "--write" in sys.argv
frag = HERE / "frag" / f"{FRAG}.html"
src = frag.read_bytes().decode("utf-8")
crlf = "\r\n" in src
s = src.replace("\r\n", "\n")
problems = []


def section_span(text, sid):
    start = text.find(f'<section class="topic" id="{sid}">')
    if start < 0:
        return None
    end = text.find("</section>", start)
    return start, end + len("</section>")


orig_figs = set(re.findall(rf"<figcaption><b>Fig ({UNIT}\.\d+)</b>", s))
for g in args:
    d = HERE / "tmp" / "merge" / g
    if not d.exists():
        problems.append(f"{g}: folder missing"); continue
    for f in sorted(d.glob("*.html")):
        body = f.read_text(encoding="utf-8").replace("\r\n", "\n").strip("\n")
        p = Balance(); p.feed(body); p.close()
        if p.errors or p.stack:
            problems.append(f"{g}/{f.name}: unbalanced tags {p.errors[:3]} {[t for t, _ in p.stack[:3]]}")
        for n in re.findall(rf"<figcaption><b>Fig ({UNIT}\.\d+)</b>", body):
            if n not in orig_figs:
                lo, hi = RANGES[g]
                if not lo <= int(n.split(".")[1]) <= hi:
                    problems.append(f"{g}/{f.name}: new Fig {n} outside {lo}-{hi}")
        name = f.stem
        if name.startswith("replace--"):
            sid = name[len("replace--"):]
            span = section_span(s, sid)
            if not span:
                problems.append(f"{g}/{f.name}: section {sid} not found"); continue
            if f'id="{sid}"' not in body.split(">", 1)[0] + ">":
                problems.append(f"{g}/{f.name}: first tag is not section id {sid}")
            s = s[:span[0]] + body + s[span[1]:]
        elif name.startswith("new--after-"):
            after, _, newid = name[len("new--after-"):].partition("--")
            span = section_span(s, after)
            if not span:
                problems.append(f"{g}/{f.name}: anchor section {after} not found"); continue
            s = s[:span[1]] + "\n\n" + body + s[span[1]:]
        elif name.startswith("new--before-"):
            before, _, newid = name[len("new--before-"):].partition("--")
            span = section_span(s, before)
            if not span:
                problems.append(f"{g}/{f.name}: anchor section {before} not found"); continue
            s = s[:span[0]] + body + "\n\n" + s[span[0]:]
        elif name == "short":
            span = section_span(s, f"u{UNIT}-short")
            i = s.rfind("</dl>", span[0], span[1])
            s = s[:i] + body + "\n" + s[i:]
        elif name == "long":
            span = section_span(s, f"u{UNIT}-long")
            i = s.rfind('<a class="top"', span[0], span[1])
            s = s[:i] + body + "\n" + s[i:]
        else:
            problems.append(f"{g}/{f.name}: unknown output file name")

figs = re.findall(rf"<figcaption><b>Fig ({UNIT}\.\d+)</b>", s)
dups = sorted(n for n, c in Counter(figs).items() if c > 1)
if dups:
    problems.append(f"duplicate figure numbers {dups}")

pre_renumber = s   # number check must ignore figure/heading renumbering

if write and not problems:
    # figures: document order -> 2.1, 2.2, ... ; one regex pass so renames never cascade
    mapping = {old: f"{UNIT}.{i}" for i, old in enumerate(figs, 1)}
    s = re.sub(rf"Fig ({UNIT}\.\d+)(?![\d.])", lambda m: "Fig " + mapping.get(m.group(1), m.group(1)), s)
    # topic headings 2.k in document order
    k = 0
    def h3(m):
        global k
        k += 1
        return f"<h3>{UNIT}.{k} "
    s = re.sub(rf"<h3>{UNIT}\.\d+ ", h3, s)
    # short answers and long frames: number every item in order
    span = section_span(s, f"u{UNIT}-short")
    block = s[span[0]:span[1]]
    n = 0
    def dt(m):
        global n
        n += 1
        return f"<dt>Q{n}. "
    block = re.sub(r"<dt>(?:Q\d+\.\s*)?", dt, block)
    s = s[:span[0]] + block + s[span[1]:]
    span = section_span(s, f"u{UNIT}-long")
    block = s[span[0]:span[1]]
    n = 0
    def h4(m):
        global n
        n += 1
        return f"<h4>Q{n}. "
    block = re.sub(r"<h4>(?:Q\d+\.\s*)?", h4, block)
    s = s[:span[0]] + block + s[span[1]:]

tmp = HERE / "tmp" / f"merge-check-{FRAG}-{''.join(args)}.html"
tmp.write_text(s, encoding="utf-8")
p = Balance(); p.feed(s); p.close()
if p.errors or p.stack:
    problems.append(f"merged file unbalanced {p.errors[:3]}")
r = subprocess.run(["node", str(HERE / "render_math.mjs"), str(tmp), str(tmp.with_suffix(".math.html"))],
                   capture_output=True, text=True) if MATH else None
if r is not None and r.returncode:
    problems.append("KaTeX: " + " | ".join(l for l in r.stderr.splitlines() if "KaTeX" in l or "source" in l or "unpaired" in l)[:600])
elif r is not None:
    print(r.stdout.strip())
pre = HERE / "tmp" / f"merge-pre-{FRAG}.html"
pre.write_text(pre_renumber, encoding="utf-8")
before, after = check_numbers.numbers(frag), check_numbers.numbers(pre)
lost = before - after
if lost:
    problems.append(f"LOST numbers vs current {FRAG}: {dict(lost)}")
print(f"figures: {len(figs)}, numbers before {sum(before.values())} after {sum(after.values())}")
for pr in problems:
    print("PROBLEM:", pr)
if write and not problems:
    frag.write_bytes((s.replace("\n", "\r\n") if crlf else s).encode("utf-8"))
    print("WROTE", frag)
sys.exit(1 if problems else 0)
