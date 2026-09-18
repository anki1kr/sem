p = r"C:\Users\ankit\.agents\memory\wiki\hot.md"
s = open(p, encoding="utf-8").read()
anchor = "## ▶ Recent sessions (newest first)"
i = s.index(anchor)
j = s.index("\n- ", i)
line = (r"""
- **SEM5 sessional notes (2026-09-16/17)**: 5 offline guides for Unit I+II in `C:\Users\ankit\OneDrive\Desktop\SEM5\sessional\` (java, daav, ml, se, speech), built from a Python shell (`scratchpad/sess/build.py`) plus per-unit fragments. Verified: 27 Java programs compiled and run with a portable JDK, every numeric example recomputed, SVG layout probe. The owner's important-question lists are folded in (ML: cost function derivation, outliers, ensemble; Java: overloading vs overriding, abstract vs interface, array of objects, class/objects, packages; DAAV: NoSQL pros/cons, customer-data management plan, real-world DS techniques). agy, opencode and freebuff all failed headless at this size (agy 8-min timeouts, opencode config bug, freebuff TUI only).""")
assert "SEM5 sessional notes" not in s
s = s[:j] + line + s[j:]
open(p, "w", encoding="utf-8").write(s)
print("ok")
