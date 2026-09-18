# Important-question answer file — contract (read fully)

SESS = `C:\Users\ankit\AppData\Local\Temp\claude\c--Users-ankit-OneDrive-Desktop-Coding-DSA-Tracker\84ff3c22-3793-4ee7-88f6-2a7694a79575\scratchpad\sess`

## The exam (this decides everything)
Sessional paper = **30 marks, 1.5 hours**:
- **6 × 1-mark** questions from the whole Unit I + II syllabus (one line to three lines each).
- **3 × 8-mark** questions. An 8-mark question comes EITHER as one 8-mark question OR as two 4-mark parts (4 + 4).
So every important question must be answerable in **8 marks** (about 1.5 to 2 handwritten pages, about 15 minutes to
write), and must also say what to write if only a **4-mark** part is asked.

The student asked for: "imp topics sb 8 marks mai explain layak ho" — every important topic explainable for 8 marks.
Important questions FIRST; the full notes are for later.

## Your output: ONE fragment file `SESS\frag\<key>-imp.html`
You write only that file. Never edit any other file in `SESS\frag\`.

Skeleton (copy exactly; ids must be unique and start with `iq`):
```html
<section class="unit" id="imp">
<h2><span class="uno">Important questions</span>8-mark answers</h2>
<p class="unit-sub">Paper: 6 × 1 mark + 3 × 8 marks (an 8 can come as 4 + 4). Each answer below is written to the 8-mark length.</p>

<section class="topic" id="iq1"><h3>Q1. <exact question text></h3>
<p class="hook">Unit I · 8 marks · <one line: what the examiner wants to see></p>
<div class="def"><b>Definition:</b> ...</div>
<figure class="fig">...</figure>                 <!-- the diagram to draw -->
<ul> 6-10 points, <mark> on each point's keyword </ul>
<div class="tw"><table>...</table></div>          <!-- when the question says differentiate / compare / types -->
<div class="ex">...</div> or a Java program      <!-- example / numerical / code when it fits -->
<div class="mn"><b>Mnemonic</b> ...</div>          <!-- only when there is a list to remember -->
<div class="note"><b>If it comes as 4 marks:</b> write the definition, <which figure>, and <which 3-4 points>.</div>
<div class="recall"><b>Quick recall</b> 1-2 lines.</div>
<a class="top" href="#top">↑ top</a></section>

... one section per important question, in the order given below ...

<section class="topic" id="iq-1m"><h3>1-mark questions</h3>
<dl class="sa"><dt>Q1. ...</dt><dd>one to three lines</dd> ... 20-25 pairs covering BOTH units ... </dl>
<a class="top" href="#top">↑ top</a></section>
</section>
```

## Where the content comes from (accuracy — non-negotiable)
- Build every answer FROM the subject's existing fragments `SESS\frag\<key>-u1.html` and `SESS\frag\<key>-u2.html`.
  Their facts, numbers, figures and programs were already verified (and the student's class notes are already
  merged into them). **Add no new facts, statistics, dates or company claims.** You are re-composing verified
  material into exam-length answers, not researching.
- Reuse figures by COPYING the whole `<figure class="fig">…</figure>` block verbatim, including its original
  "Fig N.M" number, so the student can find it in the full notes. Never put the same figure in the file twice.
  If no existing figure fits, you may draw a new simple one (CSS primitives or inline SVG, `CONTRACT.md` rules) and
  number it `Fig Q<n>` (for example `Fig Q3`).
- Numericals: copy a worked example from the fragment verbatim, or recompute in Python
  (`C:\Users\ankit\OneDrive\Desktop\Coding\DSA-Tracker\venv\Scripts\python.exe`) before writing any new number.
- Java programs: copy them from the fragments verbatim with their `data-file` and pasted output. Inside your file
  each `data-file` name must be unique.
- Maths (ML, Speech only): LaTeX in `$...$` / `$$...$$`, the same easy notation the fragments already use
  (`SESS\LATEX.md`). Use `\lt` / `\gt` inside maths.
- No `href="#..."` links except `#top` (other ids do not exist in this file).
- Markup and diagram rules: `SESS\CONTRACT.md`. No `style=`, no emoji except ✍ and ↑.

## Length discipline
- One 8-mark answer = what a student can write in about 15 minutes: roughly 250-450 words of text plus one diagram
  (plus a program or table when the question needs it). Points, never paragraphs. Cut anything a student would not write.
- The 1-mark list: 20-25 pairs across both units, each answer one to three lines.

## Self-check (must pass before you report)
1. `python SESS\build.py <key>` — no HARD error mentioning `<key>-imp.html`; it reports the important file it wrote.
2. Java only: `python SESS\check_java.py SESS\frag\java-imp.html` → FAILS: 0.
3. Every question in your list has its own `iq` section; count them.

## Report
The question list you used (and where each came from), figures reused / newly drawn, any question you judged too small
for 8 marks (and how you handled it), anything you could not answer from the fragments.
