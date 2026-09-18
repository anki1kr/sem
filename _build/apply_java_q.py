"""Insert '2.14 Sessional questions: ready answers' into java-u2 (code + real output generated from
tmp/jq), renumber short/long, add an 'Important for sessional' index at the top of java-u1."""
import html, re, shutil, subprocess
from pathlib import Path

F = Path("frag")
JQ = Path("tmp/jq")
BIN = Path("..") / "jdk" / "jdk-21.0.12.1+1" / "bin"
Path("backup").mkdir(exist_ok=True)
shutil.copy(F / "java-u1.html", "backup/java-u1.html")
shutil.copy(F / "java-u2.html", "backup/java-u2.html")

KW = r"\b(public|class|static|void|int|double|abstract|interface|extends|implements|return|new|package|import|for)\b"


def code_html(src):
    out = []
    for line in src.rstrip("\n").split("\n"):
        code, sep, comment = line.partition("//")
        code = re.sub(KW, r'<span class="k">\1</span>', html.escape(code, quote=False))
        if sep:
            code += '<span class="c">//' + html.escape(comment, quote=False) + "</span>"
        out.append(code)
    return "\n".join(out)


def run(dirname, cls):
    d = JQ / dirname
    subprocess.run([str(BIN / "javac.exe"), f"{cls}.java"], cwd=d, check=True)
    r = subprocess.run([str(BIN / "java.exe"), cls], cwd=d, capture_output=True, text=True, check=True)
    return r.stdout.rstrip()


def block(dirname, cls):
    src = (JQ / dirname / f"{cls}.java").read_text(encoding="utf-8")
    return (f'<pre class="code" data-file="{cls}.java"><code>{code_html(src)}</code></pre>\n'
            f'<pre class="out">{html.escape(run(dirname, cls), quote=False)}</pre>')


pk = JQ / "pk"
subprocess.run([str(BIN / "javac.exe"), "-d", ".", "mypack/Calculator.java"], cwd=pk, check=True)
subprocess.run([str(BIN / "javac.exe"), "UsePackage.java"], cwd=pk, check=True)
pk_out = subprocess.run([str(BIN / "java.exe"), "UsePackage"], cwd=pk, capture_output=True, text=True, check=True).stdout.rstrip()
pk_block = ("<p><b>File 1</b> <code>mypack/Calculator.java</code>:</p>\n"
            f'<pre class="code"><code>{code_html((pk / "mypack/Calculator.java").read_text())}</code></pre>\n'
            "<p><b>File 2</b> <code>UsePackage.java</code> (in the folder that contains <code>mypack</code>):</p>\n"
            f'<pre class="code"><code>{code_html((pk / "UsePackage.java").read_text())}</code></pre>\n'
            '<p><b>Commands:</b> <code>javac -d . mypack/Calculator.java</code> → <code>javac UsePackage.java</code> → <code>java UsePackage</code></p>\n'
            f'<pre class="out">{html.escape(pk_out, quote=False)}</pre>')

tpl = Path("java_q_template.html").read_text(encoding="utf-8")
section = (tpl.replace("{P1}", block("p1", "OverloadOverride"))
              .replace("{P2}", block("p2", "AbstractInterface"))
              .replace("{P3}", block("p3", "StudentArray"))
              .replace("{P4}", block("p4", "CarDemo"))
              .replace("{PK}", pk_block))
assert "{P" not in section


def swap(s, old, new):
    assert s.count(old) == 1, (old, s.count(old))
    return s.replace(old, new)


u2 = (F / "java-u2.html").read_text(encoding="utf-8")
u2 = swap(u2, '<section class="topic" id="u2-short">', section + '<section class="topic" id="u2-short">')
u2 = swap(u2, "<h3>2.14 Short answers (1.5 marks)</h3>", "<h3>2.15 Short answers (1.5 marks)</h3>")
u2 = swap(u2, "<h3>2.15 Long-answer frames (15 marks)</h3>", "<h3>2.16 Long-answer frames (15 marks)</h3>")
(F / "java-u2.html").write_text(u2, encoding="utf-8")

u1 = (F / "java-u1.html").read_text(encoding="utf-8")
index = """<section class="topic" id="u1-important">
<h3>Important for the sessional</h3>
<ol>
<li><b>Full Unit I</b>: every section 1.1 to 1.9 (<a href="#u1-intro">start here</a>)</li>
<li><a href="#u2-q-overload">Difference between method overloading and method overriding, with example</a></li>
<li><a href="#u2-q-abstract">Explain abstract class and interface in Java</a></li>
<li>Short note: <a href="#u2-q-array">(a) Array of objects</a>, <a href="#u2-q-class">(b) Class and objects</a></li>
<li><a href="#u2-q-package">Packages</a> (in the syllabus)</li>
</ol>
</section>
"""
u1 = swap(u1, '<section class="topic" id="u1-intro">', index + '<section class="topic" id="u1-intro">')
(F / "java-u1.html").write_text(u1, encoding="utf-8")
print("ok")
