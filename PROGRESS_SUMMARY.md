# SEM 5 Sessional & Important Questions · Progress Summary

Short summary of all updates and work completed across the workspace.

---

## 1. Core Visual & Theme Fixes
- **Light Theme Only:** Maintained clean, high-contrast light theme across all pages; removed conflicting dark mode elements.
- **Figure Integrity ("Fig no. likha to fig bhi hona chahiye"):** Verified that every in-text figure reference (e.g. `Fig 1.1`, `Fig 2.27`) has a matching `<figure>`, clear SVG/CSS diagram, and descriptive `<figcaption>`.
- **Responsive Mobile Layout:** Tuned card padding, horizontal scrolling for tables, code blocks, and canvas diagrams so they render cleanly on mobile screens.

---

## 2. 1-Mark Visual Flashcards
- Redesigned and corrected the compulsory 1-mark section into visual flashcards (`.qa-card`).
- Each card includes:
  - Concise definition/formula in plain English.
  - Supporting micro-SVG diagram for rapid visual memory.
  - Highlighting the exact exam scoring keyword or mnemonic.

---

## 3. Humanized & Easy-to-Understand English (DAAV, Java, SAP)
Replaced dry, academic, telegraphic lecture notes with conversational, student-friendly explanations with real-world intuition:

### A. DAAV (`daav-important.html` · ~10,150 words · 14 Figures)
- **What is Big Data & Why RDBMS Fails:** Explained vertical scaling ceilings, rigid schema lock-in, and why *Data Locality* (sending 50 KB code to data) beats moving petabytes across networks.
- **5 V's of Big Data:** Volume, Velocity, Variety, Veracity, Value + Variability & Visualization with relatable real-world analogies.
- **Sources & Types:** Human vs Machine vs Organisational data; Structured, Semi-structured (JSON), and Unstructured media explained through a single e-commerce order.
- **Hadoop Architecture:** NameNode (RAM metadata) + DataNodes (128 MB blocks, 3× replication) + YARN (ResourceManager/NodeManager) + MapReduce.
- **NoSQL & Aggregate Model:** Horizontal scale-out, BASE vs ACID, and Martin Fowler's Aggregate model bundling customer/order data to eliminate distributed joins.
- **Data Science Process & 5 P's:** Purpose, People, Process, Platforms, Programmability; 5-step APARA (Acquire, Prepare, Analyze, Report, Act) mapped to CRISP-DM; worked IPL bowler selection case study.
- **Case Study & Recommenders:** 10 GB/day customer management plan; Netflix recommendation engine with step-by-step Cosine Similarity calculations.

### B. Java Programming (`java-important.html` · ~8,890 words · 18 Figures · 15 Code Snippets)
- **JVM Internals & WORA:** Class Loader (Load, Link [Verify, Prepare, Resolve], Initialize), 5 Runtime Data Areas (Method, Heap, Stack frames, PC, Native), Execution Engine (Interpreter, JIT hotspot compiler, Garbage Collector).
- **Overloading vs Overriding:** Compile-time static binding in the same class vs Run-time dynamic dispatch across parent-child inheritance.
- **12 Buzzwords:** SOPS, RAPD, IHMD broken down with plain English explanations.
- **Language Fundamentals:** `public static void main(String[] args)` keyword breakdown; Primitive types, Widening (automatic cup-into-bucket) vs Narrowing (explicit bucket-into-cup cast); Operators and precedence.
- **OOP Architecture:** 
  - Abstract Class (half-built house) vs Interface (pure contract enabling Multiple Inheritance without the Diamond Problem).
  - Array of Objects: Addressed the two-step allocation trap (`new Student[3]` allocates null pointers; requires `new Student()` per slot to prevent `NullPointerException`).
  - Class vs Object (cookie cutter vs cookie; State, Behavior, Identity; Stack reference pointing to Heap object).
  - Packages: Namespace folders, `javac -d .`, and import mechanics.

### C. Speech & Audio Processing / SAP (`speech-important.html` · ~21,620 words · 15 Figures · 969 Math Formulas)
- **Speech Production & Hearing:** Voiced (periodic glottal pulses, pitch $T_0$) vs Unvoiced (turbulent white noise); Middle ear ossicles (Malleus, Incus, Stapes) matching air-fluid impedance (22× pressure gain); Cochlea tonotopic frequency mapping.
- **Speech Coders:** Waveform (PCM 64k, high quality) vs Parametric (LPC-10 2.4k, robotic) vs Hybrid (CELP 8k, toll quality).
- **Codec Requirements:** Quality (MOS $\ge 4.0$ toll), Delay (ITU-T G.114: $\le 150$ ms acceptable, $> 400$ ms unacceptable), Robustness (VAD, CNG, packet concealment).
- **Pitch Estimation & DSP:** Autocorrelation curve $R(k)$ secondary peak at lag $P_0$; AMDF minimum dips; Poles (resonant formants) vs Zeros (nasal nulls); FIR always stable vs IIR feedback; 4 steps of Convolution (Flip, Shift, Multiply, Sum).
- **Linear Prediction & Levinson-Durbin:** Derivation of Yule-Walker normal equations; Prediction Gain ($G_p = 10\log_{10}(\sigma_x^2/\sigma_e^2)$); Levinson-Durbin solving Toeplitz matrices in $O(p^2)$ instead of $O(p^3)$; Reflection coefficients stability condition ($|k_m| < 1$).
- **Quantization:** Uniform SQNR ($6.02B + 1.76$ dB rule); Lloyd-Max conditions; $\mu$-law/A-law logarithmic companding; Vector Quantization with LBG clustering.

---

## 4. Build System & Current Status
- **Build Engine:** Fully compiled and validated with `_build/build.py`:
  - 0 syntax/closing tag errors.
  - 0 dead anchor links.
  - All figure numbers cross-checked and verified.
  - 969 KaTeX mathematical expressions rendered cleanly.
- **Local Dev Server:** Active on `http://localhost:8124/`.
