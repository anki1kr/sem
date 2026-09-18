# DAAV: align with the student's CLASS NOTES (read them fully)

SESS = `C:\Users\ankit\AppData\Local\Temp\claude\c--Users-ankit-OneDrive-Desktop-Coding-DSA-Tracker\84ff3c22-3793-4ee7-88f6-2a7694a79575\scratchpad\sess`
DAAV = `C:\Users\ankit\OneDrive\Desktop\SEM5\DAAV\`

The student studied from these notes and will be examined on them. Our fragments `SESS\frag\daav-u1.html` and
`SESS\frag\daav-u2.html` must (1) contain every in-syllabus topic, definition, list, table and diagram the notes
carry, (2) keep everything they already have (NEVER delete a line), (3) follow the notes' framing, ordering and
wording where it is correct, (4) never copy a mistake.
Also obey `SESS\CONTRACT.md` in full (markup, figure rules, accuracy rules). No LaTeX in DAAV; no Java code.

## SCOPE — hard rule: nothing out of syllabus
Syllabus (this is the whole of it; anything else is OUT and must not be added):
- **Unit I** — Big Data: characteristics (5 V's: volume, velocity, variety, veracity, value), structured /
  semi-structured / unstructured data, sources of big data, integrating diverse data, big data technologies,
  Hadoop (HDFS, MapReduce, YARN, ecosystem), NoSQL (types, advantages, disadvantages), aggregate data model.
- **Unit II** — Getting value out of big data, building a big data strategy, data science: five components and the
  5 P's (purpose, people, process, platform, programmability), the complete data science process, big data modeling
  and management: ingestion, storage, quality, operations, scalability, security, applications, case study.

The class notes contain material that is NOT in this syllabus (for example, in unit 2 daav.pdf: DevOps-vs-DataOps
team-role tables, vendor product catalogues, marketing copy for paid courses, "sign up for this course" lines).
**Do not add any of that.** If a notes page is entirely out of syllabus, skip it and say so in your report.

## The student's own IMPORTANT-QUESTION list (this decides depth)
Everything below must be answerable, at 15-mark depth, from our file. These sections already exist
(`u1-important`, `u2-important`) and link to the topics — keep those links working.
Unit I: 1. What is Big Data? 2. Sources of big data. 3. Types of big data. 4. Big data technologies.
5. Hadoop architecture. 6. The 5 V's. 7. Advantages and disadvantages of NoSQL. 8. Integrating diverse data +
the aggregate data model.
Unit II: 1. Components of data science + the 5 P's. 2. The complete data science process. 3. Big data modeling
and management. 4. Case study: a management plan for a company's customer data. 5. A real-world data-science
example using advanced techniques.
If the class notes make one of these richer (an extra factor, a real table, a real example), that is exactly what
you add.

## What "align" means, concretely
- Any in-syllabus item present in the notes and missing from our file → ADD it, in the file's own style.
- Any list the notes give (7 steps, 6 DQAF dimensions, 4 NoSQL types, features of YARN …) → our file must carry
  the SAME list with the same count and the same item names, plus a mnemonic when it is a list worth memorising.
- Any table in the notes (SQL vs NoSQL, structured vs semi-structured vs unstructured, batch vs streaming …) →
  a `<div class="tw"><table>` with the same rows.
- Any diagram the notes draw (HDFS master/slave, MapReduce flow, YARN, ingestion pipeline, DS process cycle …) →
  a redrawable `figure` using the CSS primitives or inline SVG. Never copy an image.
- Keep our file's existing wording where both are correct; do not rewrite a good section just to reword it.
- Factual claims (company names, product names, numbers) must be true. If the notes state a figure you cannot
  confirm, either drop it or write it as "the notes quote …" only when it is clearly an illustration. Never invent.

## Mistakes: correct them, with a note
Where the notes are wrong, write the CORRECT version and add
`<div class="note"><b>Common mistake:</b> ...</div>` naming what the notes say and why it is wrong. Verify before
you call something a mistake (WebSearch is allowed). Report every such correction with your evidence.
Known things to check carefully: the default HDFS block size and replication factor (the notes state values —
check them against Apache Hadoop's own documentation and say which version they hold for), which NoSQL types
exist (four: key-value, document, column-family, graph), and whether a claim about ACID in NoSQL is stated as an
absolute ("NoSQL has no ACID") when modern NoSQL databases do offer it.

## Ownership — four agents work at the same time
**The fragment files `SESS\frag\daav-u1.html` and `SESS\frag\daav-u2.html` must NOT be edited by any agent.**
Each agent writes its output into its own folder and the coordinator merges.

Unit I section ids, in order: u1-important, u1-intro, u1-char, u1-types, u1-sources, u1-examples, u1-tech,
u1-integ, u1-hadoop, u1-hdfs, u1-mapreduce, u1-yarn, u1-ecosystem, u1-nosql, u1-nosqltypes, u1-aggregate,
u1-short, u1-long.
Unit II section ids, in order: u2-important, u2-value, u2-strategy, u2-components, u2-5p, u2-process, u2-mgmt,
u2-ingestion, u2-storage, u2-quality, u2-operations, u2-scale-sec, u2-apps, u2-case, u2-realworld, u2-short,
u2-long.

| Group | Fragment | Notes to read | Owns (may replace) | New figures |
|---|---|---|---|---|
| G | daav-u1 | `unit 1 daav.pdf` pages 1-13 | u1-intro, u1-char, u1-types, u1-sources, u1-examples, u1-tech, u1-integ | Fig 1.30-1.49 |
| H | daav-u1 | `unit 1 daav.pdf` pages 14-33 + `unit 1_nosql.pdf` (2 pages) | u1-hadoop, u1-hdfs, u1-mapreduce, u1-yarn, u1-ecosystem, u1-nosql, u1-nosqltypes, u1-aggregate | Fig 1.50-1.69 |
| I | daav-u2 | `unit 2 daav.pdf` pages 1-13 + `data science unit 2[1].pdf` (all 17 pages) | u2-value, u2-strategy, u2-components, u2-5p, u2-process, u2-case, u2-realworld | Fig 2.30-2.49 |
| J | daav-u2 | `unit 2 daav.pdf` pages 14-35 | u2-mgmt, u2-ingestion, u2-storage, u2-quality, u2-operations, u2-scale-sec, u2-apps | Fig 2.50-2.69 |

Read the PDFs with the Read tool, `pages` parameter, max 20 pages per call. `unit 1 daav.pdf` and
`unit 2 daav.pdf` have selectable text; `data science unit 2[1].pdf` is image-only, so read it page by page.

## Output files — go in `SESS\tmp\merge\<GROUP>\`
- `replace--<id>.html` — the COMPLETE new `<section class="topic" id="<id>">...</section>` for a section you own.
  Start from that section's CURRENT text in the fragment, keep ALL of it, and add to it.
- `new--after-<anchor>--<newid>.html` / `new--before-<anchor>--<newid>.html` — a complete new topic section.
  `<anchor>` must be an ORIGINAL section id (from the lists above). Only add a new section when the material is a
  syllabus sub-topic that genuinely has no home in a section you own.
- `short.html` — extra `<dt>...</dt><dd>...</dd>` pairs (do NOT number them; the coordinator does).
- `long.html` — extra `<h4>Question</h4><ol>...</ol>` frames (no Q numbers).
- Every file: balanced tags, ids unique, figures only from YOUR number range, no `style=`, no emoji except ✍ and ↑.
- Keep the h3 heading number as it is (e.g. `<h3>1.7 ...`); the coordinator renumbers headings after merging.

## Self-check before you report (both must pass)
1. `python SESS\check_merge.py <GROUP> --frag=daav-u1` (or `--frag=daav-u2`) exits 0 — tags balanced, figure
   numbers in range, no duplicate figures, no LOST numbers.
2. Re-read your own output once against the notes pages you were given: every list count matches, every table row
   matches, no out-of-syllabus material crept in.

## Report
Topics added or deepened, lists/tables carried over, figure numbers used, every mistake found in the class notes
(quote it + the correction + how you verified), anything in the notes you deliberately SKIPPED as out of syllabus,
and anything you could not confirm.
