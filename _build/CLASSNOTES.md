# Speech notes: align with the student's CLASS NOTES (read fully)

SESS = `C:\Users\ankit\AppData\Local\Temp\claude\c--Users-ankit-OneDrive-Desktop-Coding-DSA-Tracker\84ff3c22-3793-4ee7-88f6-2a7694a79575\scratchpad\sess`
NOTES = `C:\Users\ankit\OneDrive\Desktop\SEM5\Speech Audio\`

The student has given us the notes they actually studied from. The sessional notes must
(1) use THEIR notation and formula forms, (2) cover every topic in their notes that our file is missing,
(3) keep everything our file already has (never delete content), (4) never copy a mistake from their notes.

Also obey, in full: `SESS\CONTRACT.md` (fragment markup, diagrams, figure rules) and `SESS\LATEX.md` (maths is
LaTeX `$...$` / `$$...$$`, `\lt`/`\gt` inside maths, KaTeX-valid, easy forms). Where this file's notation table
differs from LATEX.md's Speech table, THIS file wins.

## Reference files (read them; the handwritten PDF is scanned images, read page by page)
- Unit I: `NOTES\Speech signal processing is.pdf` (27 pages, typed web-compiled notes).
- Unit II: `NOTES\speech and audio notes.pdf` (15 pages, the student's handwritten-style notes: linear prediction,
  prediction gain, Levinson-Durbin, LTP, short-term LPC, MA models) and `NOTES\unit2.pdf` pages 1-11
  (typed; page 12 is garbled OCR, ignore it).

## Notation (from the class notes; use exactly this)
| Topic | Write it as |
|---|---|
| Signal / prediction / error | signal `x[n]`; `\hat{x}[n] = \sum_{k=1}^{p} a_k\,x[n-k]`; `e[n] = x[n] - \hat{x}[n]`. Use x, not s, for all linear-prediction, autocorrelation, quantizer and DPCM formulas. (The source-filter speech output in Unit I may stay `s[n]`.) |
| Autocorrelation | parentheses: `R(i) = \frac{1}{N}\sum_{n=0}^{N-1-i} x[n]\,x[n+i]` (Unit II); Unit I estimators keep their 1/N and 1/(N−k) forms but also write `R(k)` with parentheses |
| Mean squared error | `E = \frac{1}{N}\sum_{n}\Big(x[n] - \sum_{k=1}^{p} a_k\,x[n-k]\Big)^2` |
| Yule-Walker | `\sum_{k=1}^{p} a_k\,R(i-k) = R(i), \quad i = 1, \dots, p` (plus the existing order-2 matrix) |
| Frame analysis | `x_m[n] = x[n]\,w[n - mL]`, w = window (Hamming/Hanning), m = frame index, L = frame shift (hop); frames 20-30 ms, about 50% overlap |
| Prediction gain | `G_p = 10\log_{10}\left(\frac{\sigma_x^2}{\sigma_e^2}\right)` dB, σ_x² = signal power, σ_e² = residual power; segmental `SPG = \frac{1}{M}\sum_{m=1}^{M} G_p(m)` (average of per-frame dB values) |
| Levinson-Durbin | `E_0 = R(0)`; for m = 1..p: `k_m = \frac{R(m) - \sum_{j=1}^{m-1} a_j^{(m-1)} R(m-j)}{E_{m-1}}`; `a_m^{(m)} = k_m`; `a_j^{(m)} = a_j^{(m-1)} - k_m\, a_{m-j}^{(m-1)}` for 1 ≤ j ≤ m−1; `E_m = (1 - k_m^2)\,E_{m-1}`; final `a_k = a_k^{(p)}`. Add ONE easy-reading line under it: "new $a_j$ = old $a_j$ − $k_m$ × old $a_{m-j}$ (the mirror coefficient)". Mnemonic from notes: R → E → K → a → E. Complexity O(p²) vs O(p³) matrix inversion; Toeplitz (symmetric) autocorrelation matrix. |
| Long-term prediction (LTP) | `e[n] \approx \beta\, e[n-T]`; final residual `r[n] = e[n] - \beta\, e[n-T]`; `\beta(T) = \frac{\sum_n e[n]\,e[n-T]}{\sum_n e^2[n-T]}`; `E(T) = \sum_n r^2[n]`, choose the T with minimum E(T); 3-tap `\hat{e}[n] = \beta_{-1} e[n-T-1] + \beta_0 e[n-T] + \beta_1 e[n-T+1]`; transfer form `P(z) = 1 - \beta z^{-T}` may stay |
| Two-stage gain | `G_{p,short} = 10\log_{10}\frac{\sigma_x^2}{\sigma_e^2}`, `G_{p,long} = 10\log_{10}\frac{\sigma_e^2}{\sigma_r^2}`, total = short + long (dB) |
| MA prediction / model | prediction from past errors `\hat{x}[n] = \sum_{k=1}^{q} b_k\, e[n-k]`; MA model `x[n] = \sum_{k=0}^{q} b_k\, u[n-k]` (u = input/excitation, white noise); impulse response `h[n] = b_n` for n = 0..q, 0 after (FIR, q+1 terms) |
| AR(1) / MA(1) contrast | `x[n] = a_1 x[n-1] + u[n]`, `h[n] = a_1^{\,n}` for n ≥ 0 (infinite, decays if \|a_1\| < 1); `x[n] = u[n] + b_1 u[n-1]`, `h[n] = \{1, b_1, 0, 0, \dots\}` (finite) |
| DPCM | `e[n] = x[n] - \hat{x}[n]`, `\tilde{x}[n] = \hat{x}[n] + \hat{e}[n]` |

## Numbers already verified in Python (use these values; do not re-derive differently)
- Levinson example from the notes, R(0)=10, R(1)=6, R(2)=4: k₁ = 0.6, a₁⁽¹⁾ = 0.6, E₁ = 6.4; k₂ = (4 − 0.6×6)/6.4 = 0.0625;
  a₁⁽²⁾ = 0.6 − 0.0625×0.6 = 0.5625; a₂⁽²⁾ = 0.0625; E₂ = (1 − 0.0625²)×6.4 = 6.375 (the notes print 6.374 only
  because they rounded k₂² to 0.0039; write 6.375). Direct 2×2 solve gives the same a₁, a₂.
- Levinson example from the notes, R(0)=96, R(1)=81, R(2)=50: exact k₁ = 0.8438, E₁ = 27.656, k₂ = −0.6633,
  a₁ = 1.4034, a₂ = −0.6633, E₂ = 15.489. The notes show 0.844 / 27.62 / −0.665 / 1.405 / 15.41 because they
  rounded k₁ to 0.844 first; if you include this example, give exact values and one line explaining the small difference.
- Our existing example R = 5, 3, 1 (a₁ = 0.75, a₂ = −0.25, E₂ = 3.0, G_p = 2.218 dB): keep it, rewrite in the notation above.
- Notes' simple gain example: σ_x² = 100, σ_e² = 10 → G_p = 10 log₁₀(10) = 10 dB.
- Frame A from the notes, x_A = [2, 4, 6, 5, 3, 1, −1, −2], p = 1: R(0) = 96, R(1) = 81, a₁ = 81/96 = 0.844,
  σ_x² = 96/8 = 12, residual e[n] = x[n] − a₁x[n−1] for n = 1..7, Σe² = 20.81, σ_e² = 20.81/7 = 2.97,
  G_p = 10 log₁₀(12/2.97) = 6.06 dB.
  **The notes contain a mistake here:** they write σ_e² = 12 × 2.97 / 8 = 4.455 and then 10 log₁₀(12/4.455) ≈ 6.06 dB,
  but 12/4.455 gives 4.30 dB. Use σ_e² = 2.97. Add a short `<div class="note"><b>Common mistake:</b>` saying
  σ_e² is the average squared error (2.97), not 12 × 2.97 / 8.
- Frame B in the notes is internally inconsistent (its R(0) and σ_x² cannot both be true for the listed samples).
  Do NOT copy it. Build your own 8-sample noise-like frame whose |R(1)/R(0)| is below 0.2, compute R(0), R(1), a₁,
  σ_x², σ_e², G_p in Python, and show that G_p is small (unvoiced-like) versus Frame A (voiced-like).
- Pitch lag range: the notes say "20-200 ms, 160-1600 samples", which is too large. Pitch periods are about 2.5-20 ms
  (F0 about 50-400 Hz), i.e. about 20-160 samples at 8 kHz. Write that, carefully worded ("about").

## Unit I: topics to ADD if missing (from the Unit I PDF), each in the right existing section or a new section
- What speech signal processing is + applications (voice assistants, ASR transcription, speech coding, TTS accessibility, IVR/customer service, speaker recognition, speech enhancement).
- Speech production process in 3 stages: conceptualization, formulation, articulation; key components lungs, vocal cords (larynx), vocal tract (pharynx, oral, nasal cavity), articulators (tongue, lips, jaw, velum).
- Types of speech production models: physiological, acoustic (source-filter), psycholinguistic, LPC.
- Auditory system detail: outer ear (pinna, ear canal, eardrum/tympanic membrane); middle ear (ossicles malleus, incus, stapes; Eustachian tube equalises pressure); inner ear (cochlea, organ of Corti, basilar membrane, hair cells, auditory nerve); pathway to brain (cochlear nucleus, superior olivary nucleus, lateral lemniscus, inferior colliculus, auditory cortex in temporal lobe); 5-step "how hearing works".
- Speech coder structure detail: encoder (input, analysis, coding), decoder (input, decoding, output); key considerations bit rate, quality, complexity, delay.
- Classification detail: waveform (PCM 64 kbps, ADPCM, sub-band coding), vocoders (LPC, formant coding; very low rates such as 1.2 and 2.4 kbps), hybrid (CELP, AMR, MBE); factors: bit rate, complexity, quality, robustness.
- Requirements detail: quality (intelligibility, naturalness, absence of artifacts; metrics MOS 1-5, PESQ, spectral distortion SD, SNR); coding delay per ITU-T G.114 (0-150 ms acceptable for most users, 150-400 ms acceptable depending on impact, above 400 ms unacceptable for general network planning; causes frame size and look-ahead); robustness (noise, reverberation, packet loss; VAD and comfort noise generation CNG); trade-offs.
- Pitch period: T₀ and F₀ = 1/T₀; methods autocorrelation (largest peak after lag 0), cepstrum (quefrency peak), SIFT (LP inverse filtering then autocorrelation of the residual), wavelet-based; 4-step general procedure (pre-processing, framing + windowing, pitch detection, post-processing/smoothing).
- All-pole / all-zero: definitions of poles and zeros; all-pole = IIR, needs poles inside unit circle; all-zero = FIR, always stable; examples Butterworth and Bessel (all-pole analog prototypes); key-differences table (poles vs zeros, stability, impulse response, frequency response peaks vs notches).
- Convolution: flip, shift, multiply, sum; commutative; convolution theorem (convolution in time = multiplication in frequency); applications (LTI filters, image blurring/edge detection, CNNs).
Keep the sections already present (PSD, periodogram, AR model, autocorrelation estimation stay: they are in the syllabus even though the class notes skip them).

## Unit II: topics to ADD if missing (from the Unit II PDFs)
- Section-1 style content: "Linear prediction kya hai", core idea with expanded form `\hat{x}[n] = a_1x[n-1] + a_2x[n-2] + \dots + a_px[n-p]`, small p = 3 numeric example from the notes (x[n−1]=10, x[n−2]=12, x[n−3]=14, a = 0.5, 0.3, 0.2 → x̂[n] = 5 + 3.6 + 2.8 = 11.4; residual example x[n]=20, x̂[n]=18 → e[n]=2), what a good predictor is (e[n] ≈ 0), prediction order p meaning.
- Comparison table: autocorrelation method vs covariance method vs Levinson-Durbin (key points, pros/cons) as in the notes.
- Key related concepts table (prediction order, residual, all-pole model, LPC, stability, adaptive prediction LMS/RLS) and "why it is useful" list (compression, signal modeling, spectral estimation, noise reduction/forecasting).
- Non-stationarity problem, frame-based solution steps, `x_m[n] = x[n]\,w[n-mL]`, stationary-LP vs short-time-LP comparison table, flow diagram Speech → Framing → Windowing → LP analysis → time-varying a_k(m) → error e[n] → G_p (draw as a figure).
- Prediction gain interpretation, SPG, Frame A (corrected) and your Frame B, relation to prediction order (gain rises with p then saturates; typical p ≈ 10-16 for 8-16 kHz), quality metric use.
- Short-term LPC section content from the notes (meaning, formants/vocal tract, all-pole, frame length 20-30 ms ≈ 160-240 samples at 8 kHz, overlap, windowing, re-analysed per frame) and "LPC = Local Prediction" mnemonic, LPC vs LTP quick compare.
- LTP: purpose (pitch periodicity), model formulas above, estimating T and β steps, 3-tap LTP with a small figure, short-term + long-term cascade figure x[n] → LPC → e[n] → LTP → r[n], two-stage prediction gain.
- MA: three model families AR / MA / ARMA table (predicts from, filter type), MA model, no feedback = FIR, h[n], AR vs MA comparison tables (impulse response, stability, spectral shape, solving), why AR is preferred for speech, where MA shows up (nasal anti-resonances, ARMA, FIR pre/de-emphasis), AR(1) vs MA(1) numerical contrast, mnemonic "AR = Apna past Result, MA = past input Mixture, ARMA = dono".
- Mnemonics from the notes: "Frame-Window-Analyze-Track", "Original/Error → Gain", "Linear Prediction = Past se Future ka Andaza".
Quantization sections (uniform, optimum, log, adaptive, differential, VQ) are not in the class notes: keep them, only switch notation to x.

## Rules
- Never delete existing content. Reorganising within a topic is fine if nothing is lost.
- New figures: find the highest existing `Fig N.k` number in YOUR file (grep the whole file) and continue from there;
  new figures may appear out of numeric order on the page, which is acceptable; never reuse a number.
- New short answers and long-answer frames for the added topics (append to the existing lists, continue numbering).
- Every number you add must be computed in Python (`C:\Users\ankit\OneDrive\Desktop\Coding\DSA-Tracker\venv\Scripts\python.exe`).
- Write edits with Python raw strings or the Edit/Write tools; keep the file's existing line endings.

## Self-check (all must pass)
1. `python SESS\check_math.py <speech-u1|speech-u2>` exits 0 (KaTeX renders, no control characters); review the plain-text-maths list.
2. `python SESS\check_numbers.py <speech-u1|speech-u2>` shows no LOST numbers (additions are expected). If an existing
   number is intentionally replaced (only allowed for a notation-only change), say which in your report.
3. `python SESS\build.py speech` runs with no HARD errors (both speech agents finish in parallel, so if the other unit
   is mid-edit and breaks the build, re-run after a minute; do not touch the other file).
4. Report: topics added (list), notation changes, new figure numbers, anything from the notes you chose not to use and why.
