# ML notes: align with the student's CLASS NOTES (read fully)

SESS = `C:\Users\ankit\AppData\Local\Temp\claude\c--Users-ankit-OneDrive-Desktop-Coding-DSA-Tracker\84ff3c22-3793-4ee7-88f6-2a7694a79575\scratchpad\sess`
ML = `C:\Users\ankit\OneDrive\Desktop\SEM5\ML\`

The student gave us the notes they studied for Machine Learning-1. The sessional notes must (1) cover every topic,
formula and numerical in those notes, (2) use the formula forms and notation of those notes where they are
consistent and correct, (3) keep everything our fragment already has (never delete), (4) never copy a mistake.

Also obey in full: `SESS\CONTRACT.md` (markup, diagrams, figures) and `SESS\LATEX.md` (maths in `$...$`/`$$...$$`,
`\lt`/`\gt` inside maths, KaTeX-valid, EASY forms). The student explicitly asked: formulas from their notes, written
in an easy way.

## References (read every page; some PDFs are image-heavy, read them page by page with the Read tool)
- Unit I: `ML\uni1.pdf`
- Unit II (converted from the student's Word notes): `ML\Unit2\`
  - `LINEAR REGRESSION.pdf`, `ML_Numericals_Point_1_Linear_Regression_Mathematical_Format.pdf`,
    `ML_Numericals_Point_2_Multiple_Linear_Regression_Mathematical_Format.pdf`
  - `LOGISTIC REGRESSION.pdf`, `LOGISTIC REGRESSION numericals.pdf`
  - `KNN NUMERICALS.pdf`, `DECISION TREE NUMERICALS.pdf`, `NAIVE BAYES IN MACHINE LEARNING.pdf`

## Notation
- Current fragments use β₀, β₁ for linear and logistic regression (`\hat{y} = \beta_0 + \beta_1 x`), matching the
  student's older notes. If the class notes use a different but equivalent notation (for example b₀/b₁, m and c,
  θ), keep β₀/β₁ as the main form and add ONE line "(in class notes: $y = mx + c$, where $m = \beta_1$, $c = \beta_0$)"
  so the student can map it. Multiple linear regression: `\hat{y} = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \dots + \beta_n x_n`.
- For any formula the notes state that our file lacks, use the notes' form written simply in LaTeX.

## Numericals: the most important part
- Every numerical in the class notes must appear in our file as a worked example (unless an identical one already
  exists), step by step, in the file's `<div class="ex">` format with `.step` lines and a boxed `.ans`.
- **Recompute every one in Python first** (`C:\Users\ankit\OneDrive\Desktop\Coding\DSA-Tracker\venv\Scripts\python.exe`,
  numpy available; write your own scripts under `SESS\tmp\`). If the notes contain an arithmetic or method mistake,
  show the CORRECT working and value, then add `<div class="note"><b>Common mistake:</b> ...</div>` naming what the
  notes did and why it is wrong. If the notes round early, say the exact value and that rounding explains the gap.
- If a numerical in the notes is ambiguous or incomplete (missing data), use the most sensible reading, state the
  assumption in one line, and report it.
- Keep every existing number of our file unchanged (a checker compares before/after).

## Ownership (several agents work at the same time; never touch anything you do not own)
- **Agent U1** owns the whole file `SESS\frag\ml-u1.html` and edits it in place.
- **Agents A and B share `SESS\frag\ml-u2.html`, so they must NOT edit that file.** Each writes replacement
  sections into its own folder; the coordinator merges them.
  - **Agent A** (regression) owns topic sections `u2-linreg`, `u2-logreg`, `u2-cost`.
    It may add NEW sections (e.g. multiple linear regression) placed after one of its sections.
    Output folder: `SESS\tmp\merge\A\`. New figure numbers: Fig 2.30 to Fig 2.49 only.
  - **Agent B** (classification) owns topic sections `u2-knn`, `u2-dt`, `u2-nb`.
    Output folder: `SESS\tmp\merge\B\`. New figure numbers: Fig 2.50 to Fig 2.69 only.
  - Existing figure numbers inside an owned section stay as they are. The coordinator renumbers all figures in
    document order after merging, so references like "draw Fig 2.31" must use your own numbers consistently.
- Output files for A and B:
  - `replace--<section-id>.html`: the COMPLETE new `<section class="topic" id="<section-id>">...</section>` for a
    section you own (start from the current section text in `SESS\frag\ml-u2.html`, keep all of it, add to it).
  - `new--after-<existing-id>--<new-id>.html`: a complete new topic section (id must start with `u2-`) inserted after
    `<existing-id>`. Keep the numbering "2.x" in the h3 as "2.x"; the coordinator renumbers headings.
  - `short.html`: extra `<dt>...</dt><dd>...</dd>` pairs for the Short answers list (no numbering, the coordinator numbers them).
  - `long.html`: extra long-answer frames, each `<h4>Question</h4><ol>...</ol>` (no Q numbers).
  - Every output file must be valid HTML fragments (balanced tags) and valid KaTeX.
- To self-check A/B output, run `python SESS\check_merge.py A` (or B): it assembles a temporary copy of ml-u2 with
  your files merged, KaTeX-renders it, checks tags and figure-number ranges, and compares numbers against the
  current fragment (no LOST allowed).
- Agent U1 self-check: `python SESS\check_math.py ml-u1` (exit 0) and
  `python SESS\check_numbers.py --base=backup_pre_notes ml-u1` (no LOST).

## Report
Topics added, numericals added (with final answers), every mistake found in the class notes (quote it, give the
correction), notation mapping lines added, assumptions made, figure numbers used.
