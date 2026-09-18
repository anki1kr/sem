import re, io
out = io.open("latex_patterns.txt", "w", encoding="utf-8")
for f in ["frag/speech-u1.html", "frag/speech-u2.html"]:
    s = open(f, encoding="utf-8").read()
    cmds = sorted(set(re.findall(r"\\[a-zA-Z]+", s)))
    out.write(f + ": " + repr(cmds) + "\n")
    out.write("dollar spans: " + str(len(re.findall(r"\$[^$]*\$", s))) + "\n")
    # sample a few bmatrix blocks
    for m in list(re.finditer(r"\\begin\{bmatrix\}.*?\\end\{bmatrix\}", s, flags=re.S))[:2]:
        out.write("BMATRIX: " + m.group(0)[:200] + "\n")
out.close()
