"""Strip raw LaTeX ($...$ and \\[...\\] spans) from the speech fragments and replace with
plain Unicode math text, matching the house style every other subject uses (the page loads
no MathJax/KaTeX, so shipping raw LaTeX means literal backslashes/braces on screen)."""
import re, io, html
from pylatexenc.latex2text import LatexNodes2Text

conv = LatexNodes2Text()


def resolve_frac(tex):
    """Replace \\frac{A}{B} with (A)/(B), recursively, using balanced-brace extraction
    so pylatexenc never has to guess grouping (it just does A/B with no parens)."""
    out = []
    i = 0
    while i < len(tex):
        m = re.match(r"\\frac\s*\{", tex[i:])
        if not m:
            out.append(tex[i])
            i += 1
            continue
        j = i + m.end()
        num, j = _read_group(tex, j)
        m2 = re.match(r"\s*\{", tex[j:])
        if not m2:
            out.append(tex[i:j])
            i = j
            continue
        j += m2.end()
        den, j = _read_group(tex, j)
        out.append("(" + resolve_frac(num) + ")/(" + resolve_frac(den) + ")")
        i = j
    return "".join(out)


def _read_group(tex, i):
    """tex[i-1] is the opening '{'; return (content, index after matching '}')."""
    depth = 1
    start = i
    while i < len(tex) and depth:
        if tex[i] == "{":
            depth += 1
        elif tex[i] == "}":
            depth -= 1
        i += 1
    return tex[start:i - 1], i


def clean(tex):
    tex = resolve_frac(tex)
    t = conv.latex_to_text(tex)
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"\s*×\s*", " × ", t)   # the only symbol TeX's space-eating actually breaks
    t = re.sub(r"\s+", " ", t).strip()
    return t


def fix_file(path):
    s = open(path, encoding="utf-8").read()
    n = 0

    def repl(m):
        nonlocal n
        n += 1
        return html.escape(clean(html.unescape(m.group(1))), quote=False)

    s = re.sub(r"\\\[(.+?)\\\]", repl, s, flags=re.S)   # display math \[ ... \] first
    s = re.sub(r"\$([^$]+)\$", repl, s)                  # then inline $ ... $
    io.open(path, "w", encoding="utf-8").write(s)
    print(path, "converted", n, "spans")


for f in ["frag/speech-u1.html", "frag/speech-u2.html"]:
    fix_file(f)
