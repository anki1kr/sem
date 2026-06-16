# Polished matplotlib plots for the PREDICTED-section answers (probstats guide).
# House style: crimson brand (#9f1239) + gold accents + paper bg. Data verified exact.
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from math import comb, erf, exp, factorial, sqrt
import os

OUT = r"c:\Users\ankit\OneDrive\Desktop\sem\ps-images"
os.makedirs(OUT, exist_ok=True)

BRAND="#9f1239"; BRAND_D="#5a081e"; BRAND_L="#f7d4dc"
GOLD="#aa6400"; GOLD_L="#ffe9a8"
INK="#12121c"; GRAY="#5f6c78"; BG="#fffcf9"; RULE="#e3d5cd"

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG,
    "savefig.facecolor": BG, "font.size": 12,
    "axes.edgecolor": GRAY, "axes.labelcolor": INK,
    "xtick.color": GRAY, "ytick.color": GRAY,
    "axes.titlecolor": BRAND_D, "axes.titleweight": "bold",
    "font.family": "DejaVu Sans",
})

def finish(fig, ax, name, title, xl, yl):
    ax.set_title(title, fontsize=13, pad=12)
    if xl: ax.set_xlabel(xl, fontsize=12)
    if yl: ax.set_ylabel(yl, fontsize=12)
    ax.grid(True, ls=":", lw=0.7, color=RULE, alpha=0.9)
    ax.set_axisbelow(True)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    fig.tight_layout()
    p = os.path.join(OUT, name)
    fig.savefig(p, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("DONE", name)

def Phi(z): return 0.5*(1+erf(z/sqrt(2)))
def npdf(x, mu=0, sd=1): return np.exp(-((x-mu)**2)/(2*sd*sd))/(sd*sqrt(2*np.pi))

# ---------- 1. Binomial PMF n=10 p=0.5 ----------
n, p = 10, 0.5
k = np.arange(0, n+1)
pmf = np.array([comb(n, int(i))*p**i*(1-p)**(n-i) for i in k])
fig, ax = plt.subplots(figsize=(7.2, 4.0))
cols = [BRAND if i == 5 else BRAND_L for i in k]
ax.bar(k, pmf, color=cols, edgecolor=BRAND, linewidth=1.1, width=0.72)
ax.annotate("mode = np = 5", xy=(5, pmf[5]), xytext=(7.1, pmf[5]*0.92),
            fontsize=11, color=BRAND_D,
            arrowprops=dict(arrowstyle="->", color=BRAND_D))
ax.set_xticks(k)
finish(fig, ax, "pred-binomial-pmf.png",
       "Binomial PMF  n = 10, p = 0.5  (symmetric, peak at k = 5)",
       "k  (number of successes)", "P(X = k)")

# ---------- 2. Standard Normal area  z in [-0.5, 1.5] ----------
x = np.linspace(-4, 4, 600)
y = npdf(x)
fig, ax = plt.subplots(figsize=(7.2, 4.0))
ax.plot(x, y, color=BRAND, lw=2.2)
m = (x >= -0.5) & (x <= 1.5)
ax.fill_between(x[m], y[m], color=BRAND, alpha=0.28)
for z in (-0.5, 1.5):
    ax.vlines(z, 0, npdf(z), color=BRAND_D, ls="--", lw=1.3)
area = Phi(1.5)-Phi(-0.5)
ax.text(0.5, 0.13, f"area\n= {area:.4f}", ha="center", fontsize=12,
        color=BRAND_D, fontweight="bold")
ax.set_xticks([-3,-2,-0.5,0,1.5,3])
ax.set_ylim(0, 0.45)
finish(fig, ax, "pred-normal-area.png",
       "P(−0.5 < Z < 1.5) = Φ(1.5) − Φ(−0.5) = 0.6247",
       "Z = (X − μ)/σ", "f(z)")

# ---------- 3. pdf f(x) = (3/4)x(2-x) on [0,2] ----------
x = np.linspace(0, 2, 400)
y = 0.75*x*(2-x)
sd = sqrt(0.2)
fig, ax = plt.subplots(figsize=(7.2, 4.0))
ax.plot(x, y, color=BRAND, lw=2.4)
ax.fill_between(x, y, color=BRAND_L, alpha=0.6)
band = (x >= 1-sd) & (x <= 1+sd)
ax.fill_between(x[band], y[band], color=GOLD, alpha=0.30)
ax.vlines(1, 0, 0.75, color=GOLD, ls="--", lw=1.6)
ax.text(1, 0.78, "mean μ = 1", ha="center", color=GOLD, fontweight="bold", fontsize=11)
ax.text(1, 0.18, f"μ ± σ\n(σ ≈ 0.447)", ha="center", color=GOLD, fontsize=10)
ax.set_ylim(0, 0.9)
finish(fig, ax, "pred-pdf-parabola.png",
       "Density f(x) = (3/4)·x(2 − x) on [0, 2]   (area = 1)",
       "x", "f(x)")

# ---------- 4. Normal reverse: 31% below 45, 8% above 64 -> N(50,10) ----------
mu, sd = 50, 10
x = np.linspace(10, 90, 600)
y = npdf(x, mu, sd)
fig, ax = plt.subplots(figsize=(7.2, 4.0))
ax.plot(x, y, color=BRAND, lw=2.2)
lt = x <= 45
rt = x >= 64
ax.fill_between(x[lt], y[lt], color=BRAND, alpha=0.30)
ax.fill_between(x[rt], y[rt], color=GOLD, alpha=0.40)
ax.vlines(45, 0, npdf(45, mu, sd), color=BRAND_D, ls="--", lw=1.2)
ax.vlines(64, 0, npdf(64, mu, sd), color=GOLD, ls="--", lw=1.2)
ax.vlines(mu, 0, npdf(mu, mu, sd), color=GRAY, ls=":", lw=1.2)
ax.text(38, 0.006, "31%\n(z=−0.5)", ha="center", color=BRAND_D, fontsize=10, fontweight="bold")
ax.text(70, 0.006, "8%\n(z=+1.4)", ha="center", color=GOLD, fontsize=10, fontweight="bold")
ax.text(mu, npdf(mu, mu, sd)+0.0015, "μ = 50", ha="center", color=GRAY, fontsize=10)
finish(fig, ax, "pred-normal-tails.png",
       "Reverse Normal: 31% below 45, 8% above 64  ⇒  μ = 50, σ = 10",
       "X", "f(x)")

# ---------- 5. Dice difference D = |X - Y| ----------
d = np.arange(0, 6)
P = np.array([6, 10, 8, 6, 4, 2])/36
ED = 35/18
fig, ax = plt.subplots(figsize=(7.2, 4.0))
cols = [BRAND if i == 1 else BRAND_L for i in d]
ax.bar(d, P, color=cols, edgecolor=BRAND, linewidth=1.1, width=0.7)
ax.vlines(ED, 0, max(P)*1.05, color=GOLD, ls="--", lw=1.8)
ax.text(ED+0.1, max(P)*0.9, f"E(D) = 35/18 ≈ {ED:.2f}", color=GOLD, fontweight="bold", fontsize=11)
for i, pr in zip(d, P):
    ax.text(i, pr+0.004, f"{int(round(pr*36))}/36", ha="center", fontsize=9, color=GRAY)
ax.set_xticks(d)
finish(fig, ax, "pred-dice-diff.png",
       "Distribution of D = |X − Y| for two fair dice  (ΣP = 1)",
       "d", "P(D = d)")

# ---------- 6. Poisson fit: deaths by horse-kick (observed vs theoretical) ----------
k = np.arange(0, 5)
obs = np.array([109, 65, 22, 3, 1]); N = obs.sum()
lam = (k*obs).sum()/N  # 0.61
theo = np.array([N*exp(-lam)*lam**i/factorial(int(i)) for i in k])
fig, ax = plt.subplots(figsize=(7.6, 4.2))
w = 0.38
ax.bar(k-w/2, obs, width=w, color=BRAND, edgecolor=BRAND_D, label="Observed")
ax.bar(k+w/2, theo, width=w, color=GOLD, edgecolor="#7a4600", label="Theoretical (Poisson)")
for i in k:
    ax.text(i-w/2, obs[i]+1.5, str(obs[i]), ha="center", fontsize=9, color=BRAND_D)
    ax.text(i+w/2, theo[i]+1.5, f"{theo[i]:.1f}", ha="center", fontsize=9, color="#7a4600")
ax.set_xticks(k)
ax.legend(frameon=False, fontsize=10)
finish(fig, ax, "pred-poisson-fit.png",
       f"Poisson Fit — deaths by horse-kick  (λ = Σfx/N = {lam:.2f})",
       "number of deaths k", "frequency (out of 200)")

# ---------- 7. Poisson fit: accidents (observed vs theoretical, lambda=0.5) ----------
k = np.arange(0, 5)
obs = np.array([122, 60, 15, 2, 1]); N = obs.sum()
lam = (k*obs).sum()/N  # 0.5
theo = np.array([N*exp(-lam)*lam**i/factorial(int(i)) for i in k])
fig, ax = plt.subplots(figsize=(7.6, 4.2))
w = 0.38
ax.bar(k-w/2, obs, width=w, color=BRAND, edgecolor=BRAND_D, label="Observed")
ax.bar(k+w/2, theo, width=w, color=GOLD, edgecolor="#7a4600", label="Theoretical (Poisson)")
for i in k:
    ax.text(i-w/2, obs[i]+1.5, str(obs[i]), ha="center", fontsize=9, color=BRAND_D)
    ax.text(i+w/2, theo[i]+1.5, f"{theo[i]:.1f}", ha="center", fontsize=9, color="#7a4600")
ax.set_xticks(k)
ax.legend(frameon=False, fontsize=10)
finish(fig, ax, "pred-poisson-accidents.png",
       f"Poisson Fit — accidents  (lambda = Sum f*x / N = {lam:.1f})  observed vs theoretical",
       "number of accidents k", "frequency (out of 200)")

# ---------- 8. Two regression lines meet at (13,17), r=0.6 ----------
X = np.linspace(6, 20, 100)
Yyx = 0.8*X + 6.6            # Y on X  (8X - 10Y + 66 = 0)
Yxy = (X - 5.35)/0.45        # X on Y  (40X - 18Y = 214) solved for Y
fig, ax = plt.subplots(figsize=(7.2, 4.4))
ax.plot(X, Yyx, color=BRAND, lw=2.4, label="Y on X:  Y = 0.8X + 6.6  (b$_{yx}$=0.8)")
ax.plot(X, Yxy, color=GOLD, lw=2.4, label="X on Y:  X = 0.45Y + 5.35  (b$_{xy}$=0.45)")
ax.plot(13, 17, "o", color=BRAND_D, ms=10, zorder=5)
ax.annotate("(X̄, Ȳ) = (13, 17)", xy=(13, 17), xytext=(13.6, 12.5),
            fontsize=11, color=BRAND_D, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=BRAND_D))
ax.text(0.03, 0.94, "r = √(0.8 × 0.45) = 0.6", transform=ax.transAxes,
        fontsize=11, color=INK, fontweight="bold")
ax.legend(frameon=False, fontsize=9.5, loc="lower right")
finish(fig, ax, "pred-two-regression.png",
       "Two regression lines intersect at the mean point (X̄, Ȳ)",
       "X", "Y")

# ---------- 9. Parabola fit Y = 1.42 - 1.07X + 0.55X^2 ----------
Xd = np.array([0, 1, 2, 3, 4]); Yd = np.array([1.0, 1.8, 1.3, 2.5, 6.3])
xx = np.linspace(-0.2, 4.2, 200); yy = 1.42 - 1.07*xx + 0.55*xx**2
fig, ax = plt.subplots(figsize=(7.2, 4.2))
ax.plot(xx, yy, color=BRAND, lw=2.4, label="fit: Y = 1.42 − 1.07X + 0.55X²")
ax.plot(Xd, Yd, "o", color=GOLD, ms=11, markeredgecolor="#7a4600", zorder=5, label="data points")
for xv, yv in zip(Xd, Yd):
    ax.text(xv, yv+0.25, f"({xv}, {yv})", ha="center", fontsize=8.5, color="#7a4600")
ax.set_xticks(Xd)
ax.legend(frameon=False, fontsize=9.5, loc="upper center")
finish(fig, ax, "pred-parabola-fit.png",
       "Second-degree parabola fit by least squares  (opens upward, c > 0)",
       "X", "Y")

# ---------- 10. Grouped marks histogram, median class 20-30, M=24 ----------
edges = [0, 10, 20, 30, 40]; freq = [5, 25, 25, 18, 7]
fig, ax = plt.subplots(figsize=(7.4, 4.2))
cols = [BRAND if e == 20 else BRAND_L for e in edges]
ax.bar(edges, freq, width=10, align="edge", color=cols,
       edgecolor=BRAND, linewidth=1.2)
# gold partial fill = (N/2 - cf) = 10 within the median class (20-30)
ax.add_patch(plt.Rectangle((20, 0), 10, 10, facecolor=GOLD, alpha=0.45, edgecolor="none"))
ax.vlines(24, 0, 25, color=GOLD, ls="--", lw=2.0)
ax.text(24.4, 28.2, "Median = 24", color="#7a4600", fontweight="bold", fontsize=11.5)
ax.text(25, 17, "median\nclass", ha="center", fontsize=9.5, color="white", fontweight="bold")
ax.text(25, 4.4, "N/2 − cf = 10", ha="center", fontsize=9, color="white", fontweight="bold")
for e, f in zip(edges, freq):
    ax.text(e+5, f+0.7, str(f), ha="center", fontsize=10, color=GRAY, fontweight="bold")
ax.set_xticks([0, 10, 20, 30, 40, 50])
ax.set_ylim(0, 31)
finish(fig, ax, "pred-marks-histogram.png",
       "Grouped marks histogram — median class 20–30 ⇒ Median = 24",
       "Marks", "Frequency (No. of students)")

print("ALL PREDICTED PLOTS GENERATED")
