"""Compare numeric tokens (decimals and 2+ digit integers) outside <svg> between the pre-LaTeX backup
and the current fragment. Any difference is printed; an empty diff means no computed value changed."""
import re, sys, html
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
SUB = str.maketrans("₀₁₂₃₄₅₆₇₈₉⁰¹²³⁴⁵⁶⁷⁸⁹", "01234567890123456789")


def numbers(path):
    s = Path(path).read_text(encoding="utf-8")
    s = re.sub(r"<svg\b.*?</svg>", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    # a super/subscript digit is its own token: "0.6²" must not read as 0.62 (nor "log₂0.6" as 20.6)
    s = re.sub(r"[₀-₉⁰¹²³⁴-⁹]", lambda m: " " + m.group().translate(SUB) + " ", s)
    s = re.sub(r"\\[a-zA-Z]+|[\^_{}]", " ", s)          # LaTeX commands and ^ _ { } separate tokens too
    s = s.replace("−", "-").replace("{,}", ",")
    s = re.sub(r"(\d),(\d{3})", r"\1\2", s)          # 5,000,000 == 5000000
    return Counter(re.findall(r"\d+\.\d+|\d{2,}", s))


if __name__ == "__main__":
    args = sys.argv[1:]
    base = "backup_pre_latex"
    if args and args[0].startswith("--base="):
        base = args.pop(0).split("=", 1)[1]
    ok = True
    for key in args:
        before = numbers(HERE / base / f"{key}.html")
        after = numbers(HERE / "frag" / f"{key}.html")
        lost, gained = before - after, after - before
        print(f"== {key}: {sum(before.values())} numeric tokens before, {sum(after.values())} after")
        if lost:
            ok = False
            print("  LOST  :", dict(lost))
        if gained:
            print("  ADDED :", dict(gained))
    sys.exit(0 if ok else 1)
