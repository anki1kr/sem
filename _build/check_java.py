"""Compile + run every <pre class="code" data-file> and compare with the following <pre class="out">.
Optional data-stdin="line1|line2" on the code block feeds keyboard input (| = new line).
Usage: python check_java.py                 (all frag/java-u*.html)
       python check_java.py path1.html ...  (specific files, e.g. tmp/merge/C/*.html)"""
import re, html, subprocess, sys, shutil
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
BIN = HERE.parent / "jdk" / "jdk-21.0.12.1+1" / "bin"
files = [Path(a) for a in sys.argv[1:]] or sorted((HERE / "frag").glob("java-u*.html"))
fails = 0
norm = lambda t: "\n".join(l.rstrip() for l in t.replace("\r", "").strip("\n").split("\n"))
for frag in files:
    s = frag.read_text(encoding="utf-8")
    blocks = list(re.finditer(
        r'<pre class="code" data-file="([^"]+)"([^>]*)>(.*?)</pre>\s*(<pre class="out">(.*?)</pre>)?', s, flags=re.S))
    print(f"== {frag.name}: {len(blocks)} programs")
    for i, m in enumerate(blocks):
        name, attrs, code, out = m.group(1), m.group(2), m.group(3), m.group(5)
        stdin_m = re.search(r'data-stdin="([^"]*)"', attrs)
        stdin = html.unescape(stdin_m.group(1)).replace("|", "\n") + "\n" if stdin_m else ""
        src = html.unescape(re.sub(r"<[^>]+>", "", code))
        d = HERE / "tmp" / "verify" / f"{frag.stem}-{i}"
        shutil.rmtree(d, ignore_errors=True); d.mkdir(parents=True)
        (d / name).write_text(src, encoding="utf-8")
        c = subprocess.run([str(BIN / "javac.exe"), "-encoding", "UTF-8", name], cwd=d, capture_output=True, text=True)
        if c.returncode:
            fails += 1; print(f"  COMPILE FAIL {name}:\n{c.stderr[:800]}"); continue
        try:
            r = subprocess.run([str(BIN / "java.exe"), "-Dfile.encoding=UTF-8", "-Dstdout.encoding=UTF-8", name[:-5]],
                               cwd=d, input=stdin, capture_output=True, text=True, encoding="utf-8", timeout=20)
        except subprocess.TimeoutExpired:
            fails += 1; print(f"  TIMEOUT {name} (waiting for input? add data-stdin)"); continue
        got = (r.stdout + r.stderr).rstrip()
        if out is None:
            fails += 1; print(f"  NO OUTPUT BLOCK {name}"); continue
        exp = html.unescape(re.sub(r"<[^>]+>", "", out)).rstrip()
        if norm(got) != norm(exp):
            fails += 1; print(f"  OUTPUT MISMATCH {name}\n  expected:\n{exp}\n  got:\n{got}")
    nodata = len(re.findall(r'<pre class="code">', s))
    if nodata:
        print(f"  ({nodata} code blocks without data-file, not run)")
print("FAILS:", fails)
sys.exit(1 if fails else 0)
