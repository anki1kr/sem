"""Insert hypothesis/cost, outliers, ensemble sections into ml-u2; renumber; add Q&A;
add an 'Important topics' index at the top of ml-u1. Backs up both files first."""
import io, shutil
from pathlib import Path

F = Path("frag")
Path("backup").mkdir(exist_ok=True)
shutil.copy(F / "ml-u1.html", "backup/ml-u1.html")
shutil.copy(F / "ml-u2.html", "backup/ml-u2.html")

u2 = (F / "ml-u2.html").read_text(encoding="utf-8")
extra = Path("ml_extra.html").read_text(encoding="utf-8")


def swap(s, old, new, count=1):
    assert s.count(old) == count, (old, s.count(old))
    return s.replace(old, new)


marker = "<!-- ============ 2.9 COMPARISON ============ -->"
u2 = swap(u2, marker, extra + marker.replace("2.9", "2.12"))
u2 = swap(u2, "<h3>2.9 Comparison of all algorithms</h3>", "<h3>2.12 Comparison of all algorithms</h3>")
u2 = swap(u2, "<h3>2.10 Short answers (1.5 marks)</h3>", "<h3>2.13 Short answers (1.5 marks)</h3>")
u2 = swap(u2, "<h3>2.11 Long-answer frames (15 marks)</h3>", "<h3>2.14 Long-answer frames (15 marks)</h3>")
# the comparison figure was 2.18; the new sections now own 2.18-2.24
u2 = swap(u2, "<figcaption><b>Fig 2.18</b> · Family tree of the Unit II algorithms",
          "<figcaption><b>Fig 2.25</b> · Family tree of the Unit II algorithms")

short = """<dt>Q19. What is a hypothesis function?</dt><dd>The function h<sub>θ</sub>(x) a model uses to map input to predicted output; for linear regression h<sub>θ</sub>(x) = θ₀ + θ₁x.</dd>
<dt>Q20. Define cost function. Write it for linear regression.</dt><dd>A function J(θ) measuring the average prediction error over all training examples; J(θ₀, θ₁) = (1/2m) Σ (h<sub>θ</sub>(x) − y)². Training minimises it.</dd>
<dt>Q21. Why is MSE not used as the cost for logistic regression?</dt><dd>With a sigmoid hypothesis the squared-error cost is non-convex (many local minima); log loss is convex, so gradient descent reaches the global minimum.</dd>
<dt>Q22. What is an outlier? Name its types.</dt><dd>A data point far from the other observations. Types: global (point), contextual, collective.</dd>
<dt>Q23. State the IQR rule for outliers.</dt><dd>IQR = Q3 − Q1; a value below Q1 − 1.5·IQR or above Q3 + 1.5·IQR is an outlier.</dd>
<dt>Q24. What is ensemble learning?</dt><dd>Combining predictions of several base models (by voting, averaging or a meta-learner) to get better accuracy and stability than any single model.</dd>
<dt>Q25. Differentiate bagging and boosting.</dt><dd>Bagging trains models in parallel on bootstrap samples with equal votes and reduces variance (Random Forest). Boosting trains sequentially, re-weighting misclassified points, and reduces bias (AdaBoost).</dd>
</dl>"""
u2 = swap(u2, "</dl>", short)

long_frames = """<h4>Q8. Define hypothesis function and cost function. Derive the least-squares formulas for linear regression.</h4>
<ol>
<li>Define hypothesis h<sub>θ</sub>(x) = θ₀ + θ₁x and hypothesis space.</li>
<li>Define cost J(θ₀, θ₁) = (1/2m) Σ (h − y)²; why square, why 1/2, convex bowl.</li>
<li>Draw Fig 2.18 (hypothesis → cost → gradient) and Fig 2.19 (bowl with descent steps).</li>
<li>Derivation: ∂J/∂θ₀ and ∂J/∂θ₁, set to 0, get θ₀ = ȳ − θ₁x̄ and θ₁ = Σ(x−x̄)(y−ȳ)/Σ(x−x̄)².</li>
<li>Gradient descent update rule and role of α.</li>
<li>Numerical: J(0,0) = 8.6, one step (α = 0.05) gives θ = (0.2, 0.66), J = 1.90; minimum J = 0.24.</li>
<li>Logistic regression cost (log loss) and why not MSE; conclusion.</li>
</ol>
<h4>Q9. What are outliers? Explain their types, detection and handling with an example.</h4>
<ol>
<li>Definition with a real example; causes.</li>
<li>Types: global, contextual, collective; draw Fig 2.21.</li>
<li>Effects on mean, variance, regression slope (0.6 → 2.63), KNN.</li>
<li>Detection: IQR rule, z-score rule, box plot (draw Fig 2.20).</li>
<li>Numerical: 12 … 62 ⇒ Q1 = 15, Q3 = 19, IQR = 4, fences 9 and 25 ⇒ 62 is an outlier; z = 2.96 misses it (masking).</li>
<li>Handling table: remove, cap, transform, impute, robust model, keep; conclusion.</li>
</ol>
<h4>Q10. Explain ensemble learning. Compare bagging and boosting.</h4>
<ol>
<li>Definition, weak learner, why combining works; draw Fig 2.22.</li>
<li>Numerical: three 70% classifiers ⇒ majority vote 78.4%.</li>
<li>Bagging: bootstrap samples, parallel models, vote/average, 63.2% unique rows, Random Forest; draw Fig 2.23.</li>
<li>Boosting: sequential, re-weight errors, AdaBoost, gradient boosting; draw Fig 2.24.</li>
<li>Stacking and hard/soft voting.</li>
<li>Bagging vs boosting table; advantages, disadvantages, applications; conclusion.</li>
</ol>
<a class="top" href="#top">↑ top</a>
</section>
</section>"""
tail = '<a class="top" href="#top">↑ top</a>\n</section>\n</section>'
assert u2.rstrip().endswith(tail), "unexpected end of ml-u2"
u2 = u2.rstrip()[: -len(tail)] + long_frames + "\n"
(F / "ml-u2.html").write_text(u2, encoding="utf-8")

u1 = (F / "ml-u1.html").read_text(encoding="utf-8")
index = """<section class="topic" id="u1-important">
<h3>Important topics</h3>
<ol>
<li><a href="#u1-types">Different types of ML</a> (supervised, <a href="#u1-unsup">unsupervised</a>, <a href="#u1-rl">reinforcement</a>)</li>
<li><a href="#u1-apps">Applications of ML</a></li>
<li><a href="#u1-issues">Various issues in ML</a></li>
<li>Data representations: <a href="#u1-numrep">numerical</a>, <a href="#u1-graphrep">graph</a></li>
<li><a href="#u2-linreg">Linear regression with example and basic numerical</a></li>
<li><a href="#u2-cost">Hypothesis function; cost function definition and derivation</a></li>
<li><a href="#u2-logreg">Logistic regression</a></li>
<li><a href="#u2-ensemble">Ensemble learning</a></li>
<li><a href="#u2-intro">Classification and regression</a></li>
<li><a href="#u2-outliers">Outliers</a></li>
<li><a href="#u2-knn">KNN: find the class (numerical)</a></li>
</ol>
</section>
"""
first = '<section class="topic" id="u1-basics">'
u1 = swap(u1, first, index + first)
(F / "ml-u1.html").write_text(u1, encoding="utf-8")
print("ok")
