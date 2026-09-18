# LaTeX conversion contract (read fully before editing)

SESS = `C:\Users\ankit\AppData\Local\Temp\claude\c--Users-ankit-OneDrive-Desktop-Coding-DSA-Tracker\84ff3c22-3793-4ee7-88f6-2a7694a79575\scratchpad\sess`

You edit exactly ONE existing file: `SESS\frag\<file>.html`. It is a finished study-notes fragment for a
BCA student. Your job is ONLY to rewrite the maths so it renders as proper maths, in an EASY form, using the
notation the student already learned. Do not change anything else.

## How maths is rendered
- `build.py` renders LaTeX with KaTeX at build time. Inline: `$...$`. Display (its own centred line): `$$...$$`.
- The build FAILS on any invalid LaTeX or unpaired `$`. There must be no `$` anywhere except as math delimiters.
- Inside maths use `\lt`, `\gt`, `\le`, `\ge`, `\ne` instead of `<` / `>` characters (they would break the HTML).
- Maths is NOT rendered inside `<svg>`, `<pre>`, `<code>`. Leave SVG labels as Unicode text (you may change a
  letter such as b to β in an SVG label to match the notation table). Never put `$` inside those tags.
- Plain words stay plain text. Only mathematical expressions become LaTeX.

## What to convert
- Every formula, equation, inequality, set of symbols and every calculation line in worked examples
  (`<div class="step">`, `<span class="ans">`, table cells with formulas, formula inside `<li>`/`<p>`/`.def`/`.recall`).
- The main formula of a topic (the one a student must write in the exam) goes on its own display line `$$...$$`.
  Short symbols inside a sentence stay inline `$...$` (e.g. "where $p_i$ is the probability").
- Example: `b₁ = Σ(x − x̄)(y − ȳ) / Σ(x − x̄)²` becomes `$$\beta_1 = \frac{\sum (x_i-\bar{x})(y_i-\bar{y})}{\sum (x_i-\bar{x})^2}$$`
- Example step: `J(0, 0) = 86 / (2 × 5) = 8.6` becomes `$J(0,0) = \dfrac{86}{2 \times 5} = 8.6$`.

## Keep it EASY (the student asked for this)
- Prefer the simplest correct form. `\sum` without limits when the range is obvious ("over all i"); add limits
  only where they matter (e.g. `\sum_{k=1}^{p}` in linear prediction).
- No heavy notation the unit does not need (no vectors in bold unless already used, no expectation operators,
  no matrix calculus). Short fractions inline may be `a/b`; display fractions use `\frac`.
- Use `\cdot` or `\times` for multiplication consistently; `\log_2`, `\log_{10}`, `\ln` for logs.
- Do not add new formulas or new theory. Do not delete formulas. Same content, better typeset.

## Notation table: use EXACTLY this (it is what the student studied in the older notes)

### ML
| Topic | Write it as |
|---|---|
| Linear regression | `\hat{y} = \beta_0 + \beta_1 x` (coefficients β₀, β₁ everywhere; replace b₀/b₁, θ₀/θ₁, w₀/w₁ used for linear/logistic regression) |
| Error, SSE | `e_i = y_i - \hat{y}_i`, `SSE = \sum e_i^2` |
| Least squares | `\beta_1 = \frac{\sum (x_i-\bar{x})(y_i-\bar{y})}{\sum (x_i-\bar{x})^2}`, `\beta_0 = \bar{y} - \beta_1 \bar{x}` |
| Cost function | `J(\beta_0,\beta_1) = \frac{1}{2m}\sum (\hat{y}_i - y_i)^2`; hypothesis `h(x) = \beta_0 + \beta_1 x` |
| Gradient descent | `\beta_j := \beta_j - \alpha \frac{\partial J}{\partial \beta_j}` |
| R² | `R^2 = 1 - \frac{SS_{res}}{SS_{tot}}` |
| Logistic | `z = \beta_0 + \beta_1 x`, `\sigma(z) = \frac{1}{1+e^{-z}}`, log loss `L = -\frac{1}{n}\sum [y_i \log \hat{y}_i + (1-y_i)\log(1-\hat{y}_i)]` |
| Entropy | `H(S) = -\sum p_i \log_2 p_i` |
| Information gain | `IG(S,A) = H(S) - \sum_v \frac{|S_v|}{|S|} H(S_v)` |
| Gini | `Gini = 1 - \sum p_i^2` |
| Bayes | `P(C \mid X) = \frac{P(X \mid C)\,P(C)}{P(X)}`, naive: `P(C \mid X) \propto P(C)\prod P(x_i \mid C)` |
| Distances | `d = \sqrt{\sum (x_i - y_i)^2}` (Euclidean), `d = \sum |x_i - y_i|` (Manhattan) |
| SVM | `w^T x + b = 0`, margin `\frac{2}{\lVert w \rVert}` (keep w and b for SVM only) |
| Kernels | `K(x,z) = (x \cdot z + c)^d`, `K(x,z) = e^{-\gamma \lVert x-z \rVert^2}` |
| Scaling | `x' = \frac{x - x_{min}}{x_{max} - x_{min}}`, `z = \frac{x - \mu}{\sigma}` |
| Mitchell learning system (Unit I) | keep Mitchell's own `\hat{V}(b) = w_0 + w_1 x_1 + ...` weights w (that is his notation) |

### Speech (sign convention: predictor has a PLUS sum, error is s minus prediction)
| Topic | Write it as |
|---|---|
| Autocorrelation | `R[k] = \sum_n x[n]\,x[n+k]`; biased `\hat{R}_b[k] = \frac{1}{N}\sum x[n]x[n+k]`; unbiased `\hat{R}_u[k] = \frac{1}{N-k}\sum x[n]x[n+k]` |
| AMDF | `AMDF[k] = \frac{1}{N}\sum |x[n]-x[n+k]|` |
| All-pole | `H(z) = \frac{G}{A(z)}`, `A(z) = 1 - \sum_{k=1}^{p} a_k z^{-k}` |
| All-zero | `H(z) = B(z) = \sum_{k=0}^{q} b_k z^{-k}` (keep whatever coefficients the file already uses) |
| Convolution | `y[n] = \sum_k x[k]\,h[n-k]`, output length `M + N - 1` |
| PSD / periodogram | `S(\omega) = \sum_k R[k] e^{-j\omega k}`, `\hat{S}(\omega) = \frac{1}{N}|X(\omega)|^2` |
| AR model | `x[n] = \sum_{k=1}^{p} a_k x[n-k] + e[n]`, `S(\omega) = \frac{\sigma^2}{|A(e^{j\omega})|^2}` |
| Linear prediction | `\hat{s}[n] = \sum_{k=1}^{p} a_k s[n-k]`, `e[n] = s[n] - \hat{s}[n]` |
| Normal equations | `\sum_{k=1}^{p} a_k R[|i-k|] = R[i]`, i = 1..p (order-2 matrix with `\begin{bmatrix}...\end{bmatrix}` is fine) |
| Prediction gain | `G_p = 10\log_{10}\frac{\sigma_s^2}{\sigma_e^2}` dB |
| Levinson-Durbin | `E_0 = R[0]`; `k_i = \frac{R[i] - \sum_{j=1}^{i-1} a_j R[i-j]}{E_{i-1}}`; `a_i = k_i`; `a_j^{new} = a_j^{old} - k_i\, a_{i-j}^{old}`; `E_i = (1-k_i^2)E_{i-1}`; stable if `|k_i| \lt 1` (use this simple "old/new" form, not nested superscripts) |
| Long-term predictor | `P(z) = 1 - \beta z^{-T}` |
| Uniform quantizer | `\Delta = \frac{x_{max} - x_{min}}{L}`, `L = 2^B`, `SQNR \approx 6.02B + 1.76` dB |
| Lloyd-Max | `d_k = \frac{y_k + y_{k+1}}{2}`, `y_k` = centroid of its region |
| μ-law | `C(x) = \frac{\ln(1+\mu|x|)}{\ln(1+\mu)}\,\text{sgn}(x)`, μ = 255 |
| A-law | two-part form with A = 87.6 (keep the file's pieces) |
| DPCM | `e[n] = s[n] - \hat{s}[n]`, `\tilde{s}[n] = \hat{s}[n] + \hat{e}[n]` |
| VQ distortion | `d(x,y) = \sum (x_i - y_i)^2`; weighted `d = (x-y)^T W (x-y)` |
| LBG split / stop | `c^{+} = c(1+\epsilon)`, `c^{-} = c(1-\epsilon)`; stop when `\frac{D_{old}-D_{new}}{D_{old}} \lt \epsilon` |

If the file already states a different but equivalent convention, switch it to this table and make sure every
worked example still gives the SAME numbers (re-check with Python:
`C:\Users\ankit\OneDrive\Desktop\Coding\DSA-Tracker\venv\Scripts\python.exe`, numpy available).

## Hard rules
- **Every number in the file must survive unchanged.** A checker compares all decimals and 2+ digit integers
  before/after. Do not reformat numbers (no `5{,}000{,}000`, keep `5,000,000` as written; `0.75` stays `0.75`).
- Do not touch: figure structure, captions, `✍ Draw it` lines (except a notation letter), code blocks, ids,
  headings text, Hinglish glosses, tables' non-math cells.
- No `<style>`, `<script>`, no inline `style=`.
- Write the file with a script or careful edits. **Backslashes are dangerous in shell heredocs and Python
  non-raw strings (`\f`, `\b`, `\t`, `\n` get eaten).** Use the Write/Edit tools or Python raw strings.

## Self-check before you finish (all must pass)
1. `python SESS\build.py <ml|speech>` → no HARD errors, and it prints "math rendered: N" with N > 0.
2. `python SESS\check_numbers.py <file-stem>` (e.g. `ml-u2`) → no "LOST" line.
3. `grep -P "[\x00-\x08\x0b\x0c\x0e-\x1f]" SESS\frag\<file>.html` finds nothing (no eaten backslashes).
4. Search your file for leftover plain-text formulas (`Σ`, `√`, `²`, `/` fractions in formula context, `x̄`,
   subscript digits like `₀₁`) outside SVG: convert them.
5. Reply with: how many inline and display formulas, notation changes made, anything you were unsure about.
