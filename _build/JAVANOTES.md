# Java: align with the student's CLASS NOTES (read them fully)

SESS = `C:\Users\ankit\AppData\Local\Temp\claude\c--Users-ankit-OneDrive-Desktop-Coding-DSA-Tracker\84ff3c22-3793-4ee7-88f6-2a7694a79575\scratchpad\sess`
NOTES = `C:\Users\ankit\OneDrive\Desktop\SEM5\java\u1.pdf` (39 scanned handwritten pages) and
`C:\Users\ankit\OneDrive\Desktop\SEM5\java\u2.pdf` (50 scanned handwritten pages).
Read YOUR pages with the Read tool, `pages` parameter, max 20 pages per call. They are images — read them slowly.

The student studied from these notes. Our fragments must (1) contain every in-syllabus topic, definition, syntax,
rule, table, diagram and program the notes carry, (2) keep everything they already have (NEVER delete), (3) follow
the notes' framing and wording where it is correct, (4) never copy a mistake.
Also obey `SESS\CONTRACT.md` in full (markup, figures, Java program rules). No LaTeX needed in Java.

## SCOPE — hard rule: nothing out of syllabus
Syllabus (this is the whole of it; anything else is OUT):
- **Unit I** — Java as an OO language, features, JVM / bytecode / class loader / JIT, platform independence,
  first program, data types (byte, short, int, long, float, double, char, boolean), variables, type casting,
  operators (arithmetic, relational, logical, bitwise, ternary, increment/decrement, precedence), expressions,
  selection statements (if, if-else, nested if, else-if ladder, switch), loops (for, while, do-while, nested),
  jump statements (break, continue, return), arrays (1D, 2D).
- **Unit II** — classes and objects, `new`, array of objects, objects as arguments / returning objects, scope and
  lifetime of variables, `this`, `static` (variables, methods, blocks), constructors (default, parameterized,
  copy), constructor overloading, method overloading, inheritance (single, multilevel, hierarchical, multiple,
  hybrid) and `extends`, access modifiers, `super`, `final`, containership (has-a), polymorphism, method
  overriding, static vs dynamic binding, abstract classes, interfaces and `implements`, packages and `import`.

The notes contain material that is NOT in this syllabus: **the Scanner class, the String class and its methods,
the string constant pool, garbage collection / `finalize()` / `System.gc()`, and the `Object` class.**
**Do NOT add any of it as a topic.** (Exception: `u1-jvm` may keep the one line it already has about the garbage
collector as a part of JVM memory management — that is the JVM topic, not a GC topic.) If a program in the notes
reads keyboard input, rewrite it with hard-coded values instead of adding a Scanner section.
If a notes page is entirely out of syllabus, skip it and say so in your report.

## The student's own IMPORTANT list (this decides depth)
- The WHOLE of Unit I.
- Difference between method overloading and method overriding, with a suitable example.
- Explain abstract class and interface in Java.
- Short notes on (a) array of objects (b) class and objects.
- The package syllabus (packages, creating/compiling/running them, `import`, subpackage, access across packages).
These already have sections; the class notes must make them deeper, not replace them.

## Programs (the most important part of Java notes)
- Every in-syllabus program in your pages must appear in our file, written cleanly, COMPILED AND RUN with the JDK
  at `...\scratchpad\jdk\jdk-21.0.12.1+1\bin\javac.exe` / `java.exe`, with the REAL output pasted.
- Keep the notes' class names, variable names and values (Student 521 "Madhu", Programmer salary 4000, Bike speed
  100/50, etc.) so the student recognises them. Fix only what is broken, and say what you fixed.
- Class names of `data-file` programs must be unique across the WHOLE fragment — check the existing `data-file`
  names in the fragment first and rename yours if a clash exists.
- Programs meant to FAIL (private access, final variable/method/class, default access across packages): write them
  as `<pre class="code">` WITHOUT `data-file`, compile them yourself, and paste the real javac error lines (trimmed
  to the essential message) in a `<pre class="out">` under `<p><b>Compile error (real javac message):</b></p>`.
- Multi-file package programs: `<pre class="code">` without data-file, one block per file with its file name in a
  `<p>` above it, then the commands and the real output. Verify them in `SESS\tmp\<group>\` with `javac -d .`.
- Self-check your programs: `python SESS\check_java.py <your output .html files>` → FAILS: 0.

## Mistakes in the notes that were VERIFIED — correct them with a `<div class="note"><b>Common mistake:</b>`
1. MaxNumber program: calls `MaxFunction(a,b)` but defines `maxFunction`; Java is case-sensitive, so it does not
   compile. It also mixes the variables `man` and `max`.
2. Private-access example: `System.out.println(" obj.data);` has an unterminated string. The real errors are
   "data has private access in A" and "msg() has private access in A".
3. Default-access example imports `pack.*` but the package is `pack1`. The real error is that `Adef` is not public
   in `pack1` and cannot be accessed from outside the package.
4. "In Java there can be only one public class in a package" is WRONG: only one public class per SOURCE FILE, and
   the file must be named after it. A package can hold many public classes in separate files — which is exactly
   what the notes' own A.java / B.java example does.
5. "When two or more classes are in one file, the file is named after the class that contains main": the precise
   rule is that if a class is `public` the file must be named after that public class; with no public class any
   file name works, and you run the class that has `main`.
6. "static or final methods cannot be overridden": also `private` methods; and a static method with the same
   signature in the child HIDES the parent method, it does not override it.
7. Constructors: the notes say two types, default (no parameters) and parameterized — use that as the main
   framing. Add ONE line: strictly, the no-argument constructor the COMPILER inserts when you write none is the
   "default constructor"; a no-argument constructor you write yourself is also commonly called default. Keep the
   copy-constructor content already in the file, labelled as a third type some textbooks list.
Anything else you find, verify with a real compile/run before calling it a mistake, and report the evidence.

## Ownership — five agents work at the same time
**The fragment files `SESS\frag\java-u1.html` and `SESS\frag\java-u2.html` must NOT be edited by any agent.**
Each agent writes into its own folder; the coordinator merges.

Unit I section ids, in order: u1-important, u1-intro, u1-jvm, u1-first, u1-types, u1-operators, u1-expr,
u1-select, u1-loops, u1-array, u1-short, u1-long.
Unit II section ids, in order: u2-class, u2-arrobj, u2-objarg, u2-scope, u2-static, u2-cons, u2-inherit, u2-types,
u2-contain, u2-poly, u2-abstract, u2-interface, u2-pkg, u2-ready, u2-short, u2-long.

| Group | Fragment | Notes pages | Owns (may replace) | New sections allowed | New figures |
|---|---|---|---|---|---|
| K | java-u1 | u1.pdf 1-20 | u1-intro, u1-jvm, u1-first, u1-types | — | Fig 1.30-1.49 |
| L | java-u1 | u1.pdf 21-39 | u1-operators, u1-expr, u1-select, u1-loops, u1-array | — | Fig 1.50-1.69 |
| C | java-u2 | u2.pdf 1-13 | u2-class, u2-cons, u2-static | `new--after-u2-static--u2-methods` (methods + method overloading) if it does not fit inside a section you own | Fig 2.30-2.49 |
| E | java-u2 | u2.pdf 21-36 | u2-inherit, u2-types, u2-contain | `new--after-u2-types--u2-access` (access modifiers + table), `new--after-u2-access--u2-super`, `new--after-u2-super--u2-final` | Fig 2.50-2.69 |
| F | java-u2 | u2.pdf 37-50 | u2-poly, u2-abstract, u2-interface, u2-pkg | `new--after-u2-poly--u2-binding` (static vs dynamic binding) if it does not fit inside u2-poly | Fig 2.70-2.89 |

u2.pdf pages 14-20 (garbage collection, `finalize`, String class) are OUT OF SYLLABUS — nobody covers them.

## Output files — go in `SESS\tmp\merge\<GROUP>\`
- `replace--<id>.html` — the COMPLETE new `<section class="topic" id="<id>">...</section>` for a section you own.
  Start from that section's CURRENT text in the fragment, keep ALL of it and every program in it, and add to it.
- `new--after-<anchor>--<newid>.html` / `new--before-<anchor>--<newid>.html` — a complete new topic section; the
  anchor must be an ORIGINAL section id.
- `short.html` — extra `<dt>...</dt><dd>...</dd>` pairs (unnumbered). `long.html` — extra `<h4>Q</h4><ol>...</ol>`
  frames (unnumbered). The coordinator numbers both.
- Keep the h3 number as it is; the coordinator renumbers headings. Balanced tags, figures only from YOUR range,
  no `style=`, no emoji except ✍ and ↑.

## Self-check before you report (all must pass)
1. `python SESS\check_merge.py <GROUP> --frag=java-u1` (or `--frag=java-u2`) exits 0.
2. `python SESS\check_java.py <your .html files>` shows FAILS: 0.
3. Report: topics added/deepened, programs added (class names), notes mistakes corrected with evidence, figure
   numbers used, what you skipped as out of syllabus, anything you could not confirm.
