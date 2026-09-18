p = r"C:\Users\ankit\.agents\memory\wiki\meta\lessons-learned.md"
s = open(p, encoding="utf-8").read()
before = s.count("\x0c") + s.count("\x08")
s = s.replace("\x0crac{}{}", "\\frac{}{}").replace("\x08egin{bmatrix}", "\\begin{bmatrix}")
s = s.replace("and `\\[a-z]+` before assembling", "and `\\\\[a-z]+` before assembling")
open(p, "w", encoding="utf-8").write(s)
print("control chars before", before, "after", s.count("\x0c") + s.count("\x08"))
line = [l for l in s.splitlines() if "Agent-written HTML" in l][0]
print(line[:330])
