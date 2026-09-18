# Cross-check task (READ-ONLY review; write exactly one report file)

Do NOT run any shell command, terminal command, test, build, git command, MCP tool or browser tool.
Do NOT edit any existing file. Use file READ only, plus ONE file WRITE for your report.

Folder: `C:\Users\ankit\AppData\Local\Temp\claude\c--Users-ankit-OneDrive-Desktop-Coding-DSA-Tracker\84ff3c22-3793-4ee7-88f6-2a7694a79575\scratchpad\sess`

Subject key: given in your prompt (one of ml, se, daav, java, speech).

Read:
1. `frag\<key>-imp.html` — the important-question answer file to review (8-mark exam answers + 1-mark list).
2. `frag\<key>-u1.html` and `frag\<key>-u2.html` — the verified source notes it must be built from.

The rule the answer file had to follow: every fact, number, name, date, company claim, formula and program in it must
already appear in the two source files (it re-composes verified material; it must not add new facts).

Check every question section and the 1-mark list. Report ONLY real problems, each as one line:
`<question id> | <severity HIGH/MED/LOW> | <exact short quote from the answer> | <what is wrong> | <what the source says>`

Look for:
- a fact, number, name or claim that is NOT in the source files, or CONTRADICTS them (HIGH);
- a worked numerical whose arithmetic does not follow step to step, or whose final answer differs from the source (HIGH);
- a figure whose caption does not match what the answer text says it shows (MED);
- an answer too thin to earn 8 marks (fewer than ~6 real points and no diagram/example) (MED);
- a "If it comes as 4 marks" note that points at content not in that answer (LOW).

Write the report to `crosscheck\<key>-<yourname>.md` (yourname = agy or opencode). If you find nothing, write
"NO PROBLEMS FOUND" and the list of question ids you checked. Do not rewrite answers; the reviewer applies fixes.
