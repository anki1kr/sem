# Sessional notes fragment contract (read fully before writing)

Build dir: `C:\Users\ankit\AppData\Local\Temp\claude\c--Users-ankit-OneDrive-Desktop-Coding-DSA-Tracker\84ff3c22-3793-4ee7-88f6-2a7694a79575\scratchpad\sess`
(below: `SESS`). You write exactly ONE file: `SESS\frag\<key>-u<N>.html`. Touch nothing else.
Markup reference that renders correctly: `SESS\demo\java-u1.html` (copy its patterns).
Assembler: `SESS\build.py` (read the CSS in it if unsure what a class does).

## Reader + goal
BCA Semester-V student (Indian university), sessional exam on Unit I + Unit II. Must understand from zero,
remember fast, and REPRODUCE answers + diagrams by hand in the exam. Paper (30 marks, 1.5 h): 6 x 1-mark questions (whole
syllabus) plus 3 x 8-mark questions (an 8 can come as 4 + 4). So: every syllabus sub-topic covered, exam-writable definitions,
diagrams simple enough to draw with pen in 1-2 minutes.

## Fragment skeleton
```html
<section class="unit" id="uN">
<h2><span class="uno">Unit I or II</span>Unit title from syllabus</h2>
<p class="unit-sub">one line: what this unit is about</p>
<section class="topic" id="uN-slug"> <h3>N.1 Topic title</h3> ... <a class="top" href="#top">↑ top</a></section>
... one topic section per syllabus sub-topic (group only truly tiny ones) ...
<section class="topic" id="uN-short"><h3>N.x Short answers (1 mark)</h3><dl class="sa"><dt>Q</dt><dd>2-3 line answer</dd>...</dl></section>
<section class="topic" id="uN-long"><h3>N.y Long-answer frames (8 marks)</h3> ...</section>
</section>
```
- `id` must be unique; prefix every id with `uN-`. h3 numbering "N.k".
- Short answers: 12-16 Q&A covering the whole unit (define / differentiate / expand / list).
- Long-answer frames: 5-7 probable 8-mark questions for this unit. For each: `<h4>` question, `<ol>` of the points to
  write in order (intro/definition -> body points -> diagram to draw (name its Fig number) -> example/code -> conclusion).
  Points only, no essay.

## Every topic section contains (in this order, skip only what truly does not apply)
1. `<p class="hook">` plain-English one-liner, can end with a Hinglish gloss `<span class="hg">(...)</span>`.
2. `<div class="def"><b>Definition:</b> ...</div>` - textbook-style, exam-writable, 1-3 lines.
3. `<figure class="fig">` - DIAGRAM FIRST, before long explanation. See diagram rules.
4. `<ul>` key points, `<mark>` on the keyword of each point, short Hinglish gloss where it helps memory.
   Points, never paragraphs; no `<p>` longer than 3 lines.
5. `<div class="tw"><table>` for any comparison / differences (Differentiate X vs Y is a favourite exam question).
6. Worked example `<div class="ex"><b>Example</b><div class="step">...</div><span class="ans">...</span></div>` or code.
7. `<div class="mn"><b>Mnemonic</b> ...</div>` whenever there is a list to remember (be sure letters match the list).
8. `<div class="note"><b>Common mistake:</b> ...</div>` only when a real confusion exists.
9. `<div class="recall"><b>Quick recall</b> ...</div>` 1-2 lines, always last before the `↑ top` link.
Real-world / everyday Indian examples are welcome (IRCTC, UPI, Swiggy, cricket) but must be factually true.

## Diagram rules (the most important part)
- At least ONE figure per topic; flowcharts/block diagrams/trees/tables-as-figures that a student can draw by hand.
  Keep each figure to <= 10 boxes, short labels (<= 4 words per box). No decorative art.
- Wrap: `<figure class="fig"><div class="canvas"> DIAGRAM </div><figcaption><b>Fig N.k</b> · what it shows</figcaption><p class="draw">✍ Draw it: 1-line recipe (shapes + order)</p></figure>`
- Fig numbers: `Fig N.1, N.2 ...` sequential through YOUR unit only (N = unit number). Never repeat a number.
- Prefer the CSS primitives (auto-layout, never overlap):
  - `.flow` vertical flowchart: children `.n t` (start/stop oval), `.n io` (input/output parallelogram, text directly inside),
    `.n d` (decision diamond, text directly inside), `.n` (process box), `.n hi` (highlight). Arrows are automatic.
    Linear only - for yes/no branches use SVG.
  - `.chain` horizontal pipeline: `.n` boxes with automatic arrows; put `<div class="ar">label</div>` between two `.n`
    to get a labelled arrow instead. Max ~5 nodes (it scrolls if wider).
  - `.tree` hierarchy/classification: nested `<ul><li><span>..</span><ul>..</ul></li></ul>`, `span.hi` for root.
    Max 3 levels, max ~6 leaves per level.
  - `.stack` layers: `.l` rows, `.row` of `.l` side by side, `.l hi`, `<small>` sublabel.
  - `.boxes c2|c3|c4` card grid: `.b` with `<b>Title</b>` then short text.
- Use inline SVG only when geometry matters (branching flowchart, waveform, graph/axes, decision tree, SVM margin,
  spiral, DFD with bubbles, ER diagram, signal block diagram with feedback, quantizer staircase):
  `<svg class="sv" viewBox="0 0 W H" width="W">` with W <= 760. Allowed: rect (rx ok), circle, ellipse, polygon,
  line, path, polyline, text. Classes: `arr` (arrowhead at end), `arr2` (both ends), `hi` (highlight fill),
  `acc` (brand stroke), `dash`, `dot` (filled small circle), `none` (no fill). text classes: default centred,
  `l` left, `r` right, `s` small grey, `b` bold. NEVER set fill/stroke/font inline - CSS themes it.
  Text is 14px: budget ~8px per character; a label must fit inside its shape with >= 8px padding and must not
  touch any other label. Leave >= 20px margin inside the viewBox. Plot curves with computed points (use Python).
- ER diagrams: rectangle = entity, diamond = relationship, ellipse = attribute (underline key via a line under text).
  DFD: circle = process, rectangle = external entity, two parallel lines = data store, arrows = data flow.
- No ASCII art, no box-drawing characters, no images, no external resources.

## Accuracy rules (non-negotiable)
- Every number in a worked example must be COMPUTED, not hand-typed: run Python
  (`C:\Users\ankit\OneDrive\Desktop\Coding\DSA-Tracker\venv\Scripts\python.exe` has numpy) and copy the values. Show the
  substitution steps; round consistently (state the rounding).
- Java code (Java units only): every `<pre class="code">` is a COMPLETE program: `data-file="Name.java"`, exactly one
  public class `Name`, no user input (hard-coded values), deterministic output, <= 25 lines, beginner style, comments
  via `<span class="c">// ...</span>`. Compile + run each one with the JDK at
  `C:\Users\ankit\AppData\Local\Temp\claude\c--Users-ankit-OneDrive-Desktop-Coding-DSA-Tracker\84ff3c22-3793-4ee7-88f6-2a7694a79575\scratchpad\jdk\jdk-21.0.12.1+1\bin\javac.exe`
  / `java.exe` (NOTE: this is the scratchpad ROOT, one level above SESS, not `SESS\jdk\`) in a temp folder under
  SESS\tmp\, and paste the REAL output
  into the `<pre class="out">` right after it. HTML-escape `<`, `>`, `&` inside code. Use a distinct class name for
  every program in your unit (prefix nothing, just keep them unique).
- If a fact is framed differently by different textbooks, give the common textbook version and add one short line
  noting the variation. Never invent sources, statistics, dates, or quotes. WebSearch is allowed to confirm a fact.
- Stay inside the syllabus wording for scope, but explain enough that each sub-topic can fill an 8-mark answer.

## Forbidden
- No "how to use these notes", no exam strategy/tips banners, no marks/score blocks, no prediction talk.
- No emoji except ✍ in `.draw` and ↑ in the top link. No `<style>`, `<script>`, inline `style=`.
- Do not write outside your fragment file (temp compile/python files under SESS\tmp\<key>-u<N>\ are fine).

## Self-check before you finish
1. `python SESS\build.py <key>` - fix every HARD error that mentions YOUR file (a "missing fragment" for the other unit
   is expected if it is not written yet). Check the soft keyword list for your unit: every missing term must be covered.
2. Every Java program compiled and its output pasted from the real run (Java units).
3. Count your figures: >= 1 per topic. Captions numbered without gaps/repeats.
4. Reply with: topic list, figure count, code/example count, anything you were unsure about (facts you could not confirm).
