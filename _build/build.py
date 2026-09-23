"""Assemble sessional (Unit I + II) notes: shell + per-unit fragments -> one offline HTML per subject.
Usage: python build.py [subject ...]   (no args = all). Prints checks; exits 1 on any hard failure."""
import re, sys, html, subprocess
from html.parser import HTMLParser
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
FRAG = HERE / "frag"
SEM5 = Path(r"C:\Users\ankit\OneDrive\Desktop\SEM5")

SUBJECTS = {
    "java": dict(title="Java Programming", code="BCG-301-V", exam="Thu 24 Sep 2026, 2:00&ndash;3:30 PM", folder="java", brand="#b4561b", brand2="#7a3510",
                 units=["Java Language Basics", "Classes, Inheritance and Polymorphism"],
                 kw=[["JVM", "bytecode", "class loader", "JIT", "garbage", "platform independent", "byte", "short",
                      "long", "float", "double", "char", "boolean", "arithmetic", "relational", "logical", "bitwise",
                      "ternary", "increment", "expression", "precedence", "if", "switch", "for", "while",
                      "do-while", "break", "continue", "array", "2D"],
                     ["class", "object", "new", "array of objects", "method", "overloading", "overriding", "polymorphism",
                      "binding", "extends", "abstract", "interface", "implements", "multiple", "package", "import",
                      "subpackage", "classpath"]]),
    "daav": dict(title="Data Acquisition, Analysis &amp; Visualization", code="BCD-301-V", exam="Thu 24 Sep 2026, 9:30&ndash;11:00 AM", folder="DAAV",
                 brand="#0f6b64", brand2="#0a4843",
                 units=["Introduction: Big Data, Hadoop, NoSQL", "Big Data Modeling and Management"],
                 kw=[["volume", "velocity", "variety", "veracity", "value", "structured", "semi-structured",
                      "unstructured", "sources", "integrat", "Hadoop", "HDFS", "MapReduce", "YARN", "open source",
                      "NoSQL", "key-value", "document", "column", "graph", "aggregate"],
                     ["getting value", "strategy", "five components", "five P", "purpose", "people", "process",
                      "platform", "programmab", "acquire", "prepare", "analy", "report", "act", "ingestion",
                      "storage", "quality", "operations", "scalability", "security", "application"]]),
    "ml": dict(title="Machine Learning-1", code="BCG-321-V", exam="Tue 22 Sep 2026, 9:30&ndash;11:00 AM", folder="ML", brand="#5b2bb5", brand2="#3c1c7a",
               units=["Introduction of Machine Learning", "Supervised Learning (Regression / Classification)"],
               kw=[["machine learning", "perspective", "issues", "supervised", "unsupervised", "reinforcement",
                    "numerical representation", "feature vector", "graph representation", "adjacency",
                    "application"],
                   ["nearest", "KNN", "Euclidean", "decision tree", "entropy", "information gain", "Gini",
                    "naive bayes", "Bayes", "linear regression", "least squares", "logistic regression", "sigmoid",
                    "support vector", "margin", "hyperplane", "nonlinear", "kernel"]]),
    "se": dict(title="Software Engineering", code="CEU-314-V", exam="Tue 22 Sep 2026, 2:00&ndash;3:30 PM", folder="SE", brand="#1f4299", brand2="#142c66",
               units=["Introduction", "Software Requirements Analysis &amp; Specifications"],
               kw=[["software crisis", "software process", "characteristics", "life cycle", "waterfall",
                    "prototyp", "evolutionary", "incremental", "spiral", "risk"],
                   ["requirement engineering", "elicitation", "FAST", "QFD", "DFD", "context diagram",
                    "data dictionar", "ER diagram", "entity", "relationship", "cardinality", "documentation",
                    "SRS", "nature of SRS", "characteristics", "correct", "unambiguous", "complete", "consistent",
                    "verifiable", "traceable", "organization", "IEEE"]]),
    "speech": dict(title="Speech and Audio Processing", code="BCG-307-V", exam="Sat 26 Sep 2026, 9:30&ndash;11:00 AM", folder="Speech Audio",
                   brand="#9b1740", brand2="#650e29",
                   units=["Introduction and Speech Signal Processing",
                          "Linear Prediction of Speech and Speech Quantization"],
                   kw=[["speech production", "vocal", "auditory", "cochlea", "speech coder", "encoder", "decoder",
                        "parametric", "waveform", "hybrid", "quality", "delay", "robust", "pitch",
                        "all-pole", "all-zero", "convolution", "power spectral density", "periodogram",
                        "autoregressive", "autocorrelation"],
                       ["linear prediction", "prediction error", "non-stationary", "prediction gain",
                        "Levinson", "Durbin", "reflection coefficient", "long-term", "short-term",
                        "moving average", "scalar quantization", "uniform quantizer", "optimum", "Lloyd",
                        "logarithmic", "law", "adaptive", "differential", "vector quantization", "distortion",
                        "codebook", "LBG"]]),
}

ROMAN = ["I", "II"]
MATH_SUBJECTS = {"ml", "speech"}

CSS = r"""
:root{--brand:%(brand)s;--brand2:%(brand2)s;--paper:#faf8f4;--card:#ffffff;--ink:#1d1b18;
--muted:#5f5a52;--rule:#e2ddd3;--soft:color-mix(in srgb,var(--brand) 8%%,#fff);
--boxfill:#fffdf9;--hifill:color-mix(in srgb,var(--brand) 16%%,#fff);--mark:#fde68a;--good:#1f7a4d;--bad:#b3203a;
--body:"Segoe UI",system-ui,-apple-system,Roboto,"Noto Sans",sans-serif;--disp:Georgia,"Times New Roman",serif;
--mono:"Cascadia Mono",Consolas,"Courier New",monospace;--maxw:900px}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--paper);color:var(--ink);font:17px/1.6 var(--body);-webkit-text-size-adjust:100%%}
main{max-width:var(--maxw);margin:0 auto;padding:0 16px 80px}
a{color:var(--brand2)}
.cover{background:linear-gradient(135deg,var(--brand2),var(--brand));color:#fff;padding:44px 16px 34px}
.cover .in{max-width:var(--maxw);margin:0 auto}
.cover .code{font:600 13px var(--mono);letter-spacing:.08em;opacity:.85}
.cover h1{font:700 clamp(30px,6vw,46px)/1.12 var(--disp);margin:8px 0 10px}
.cover p{margin:0;opacity:.92}
.cover .chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}
.cover .chips a{color:#fff;text-decoration:none;border:1px solid rgba(255,255,255,.5);border-radius:99px;padding:3px 12px;font-size:14px}
nav.toc{background:var(--card);border:1px solid var(--rule);border-radius:12px;margin:24px 0;padding:6px 18px}
nav.toc summary{cursor:pointer;font-weight:700;padding:8px 0}
nav.toc ol{margin:4px 0 12px;padding-left:22px}nav.toc li{margin:3px 0}
nav.toc .tu{font-weight:700;margin-top:10px;color:var(--brand2)}
.unit>h2{font:700 clamp(25px,4.5vw,34px)/1.2 var(--disp);margin:56px 0 6px;padding-top:10px;border-top:3px solid var(--brand)}
.unit>h2 .uno{display:block;font:700 13px var(--mono);letter-spacing:.12em;color:var(--brand);text-transform:uppercase}
.unit-sub{color:var(--muted);margin:0 0 10px}
.topic{background:var(--card);border:1px solid var(--rule);border-radius:14px;padding:6px 22px 18px;margin:26px 0;scroll-margin-top:12px}
.topic>h3{font:700 23px/1.3 var(--disp);margin:18px 0 8px;color:var(--brand2)}
h4{font-size:18px;margin:26px 0 6px}
.hook{font-size:18px;background:var(--soft);border-left:4px solid var(--brand);padding:10px 14px;border-radius:0 8px 8px 0}
.def{border:1.5px solid var(--brand);border-radius:10px;padding:10px 14px;margin:14px 0}
.def>b:first-child{color:var(--brand2)}
ul,ol{padding-left:24px}li{margin:6px 0}
mark{background:var(--mark);padding:0 3px;border-radius:3px;color:inherit;-webkit-box-decoration-break:clone;box-decoration-break:clone}
.hg{color:var(--muted);font-style:italic;font-size:.93em}
.mn{background:#fff7d6;border:1px dashed #d4a514;border-radius:10px;padding:10px 14px;margin:14px 0}
.mn>b:first-child{display:block;font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:#8a6500}
.recall{background:#eef6f1;border:1px solid #b8dcc6;border-radius:10px;padding:10px 14px;margin:16px 0 4px}
.recall>b:first-child{display:block;font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:var(--good)}
.note{background:#fdf0f2;border:1px solid #f1c3cc;border-radius:10px;padding:10px 14px;margin:14px 0}
.note>b:first-child{color:var(--bad)}
table{border-collapse:collapse;width:100%%;font-size:15.5px;margin:14px 0;background:var(--card)}
.tw{overflow-x:auto;margin:14px 0}.tw table{margin:0;min-width:520px}
th,td{border:1px solid var(--rule);padding:7px 10px;text-align:left;vertical-align:top}
th{background:var(--soft);color:var(--brand2)}
pre{font:14.5px/1.6 var(--mono);font-variant-ligatures:none;overflow-x:auto;border-radius:10px;padding:12px 14px;margin:12px 0}
pre.code{background:#fbf6ee;border:1px solid #eadfcd}
pre.code[data-file]::before{content:attr(data-file);display:block;font:600 12px var(--body);color:var(--muted);margin-bottom:6px}
pre.out{background:#1f2328;color:#e6edf3}pre.out::before{content:"Output";display:block;font:600 12px var(--body);color:#9aa4ae;margin-bottom:4px}
.code .c{color:#7a7266;font-style:italic}.code .k{color:var(--brand2);font-weight:600}
code{font-family:var(--mono);font-size:.92em;background:#f1ece3;padding:1px 5px;border-radius:4px}pre code{background:none;padding:0}
.ex{border:1px solid var(--rule);border-radius:10px;padding:10px 16px;margin:14px 0;background:#fcfbf9}
.ex>b:first-child{color:var(--brand2)}.ex .step{margin:7px 0;font-size:16px;overflow-x:auto;overflow-y:hidden}
.ans{display:inline-block;border:2px solid var(--good);border-radius:8px;padding:2px 10px;font-weight:700;margin:6px 0}
/* ---------- figures ---------- */
figure.fig{margin:18px 0;border:1px solid var(--rule);border-radius:12px;background:#fff;padding:14px 12px 10px;cursor:zoom-in}
figure.fig .canvas{overflow-x:auto;padding:4px}
figcaption{font-size:14.5px;color:var(--muted);text-align:center;margin-top:8px}
figcaption b{color:var(--ink)}
.draw{font-size:14.5px;background:var(--soft);border-radius:8px;padding:6px 10px;margin:8px 0 0}
.n{border:1.8px solid var(--ink);background:var(--boxfill);border-radius:6px;padding:6px 12px;text-align:center;font-size:15px;line-height:1.35}
.n.t{border-radius:999px;background:var(--hifill)}
.n.hi{background:var(--hifill);border-color:var(--brand2)}
.n.io,.n.d{border:0;border-radius:0;background:no-repeat center/100%% 100%%}
.n.io{padding:6px 26px;background-image:url("data:image/svg+xml,%%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 40' preserveAspectRatio='none'%%3E%%3Cpolygon points='10,1 99,1 90,39 1,39' fill='%%23fffdf9' stroke='%%231d1b18' stroke-width='1.8' vector-effect='non-scaling-stroke'/%%3E%%3C/svg%%3E")}
.n.d{padding:10px 34px;background-image:url("data:image/svg+xml,%%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 40' preserveAspectRatio='none'%%3E%%3Cpolygon points='50,1 99,20 50,39 1,20' fill='%%23fbe9d8' stroke='%%231d1b18' stroke-width='1.8' vector-effect='non-scaling-stroke'/%%3E%%3C/svg%%3E")}
.n small{display:block;color:var(--muted);font-size:12.5px}
.flow{display:flex;flex-direction:column;align-items:center;gap:26px;margin:4px auto;width:max-content;max-width:100%%}
.flow>.n{position:relative;min-width:180px;max-width:360px}
.flow>.n+.n::before{content:"";position:absolute;left:calc(50%% - 1px);top:-25px;height:20px;border-left:2px solid var(--ink)}
.flow>.n+.n::after{content:"";position:absolute;left:calc(50%% - 5px);top:-8px;border:5px solid transparent;border-top:7px solid var(--ink)}
.flow>.ar{margin:-22px 0;font-size:13px;color:var(--muted)}
.chain{display:flex;align-items:center;gap:0;width:max-content;min-width:100%%;justify-content:center}
.chain>.n{flex:0 0 auto;max-width:190px}
.chain>.n+.n{margin-left:40px;position:relative}
.chain>.n+.n::before{content:"";position:absolute;left:-36px;top:50%%;width:28px;border-top:2px solid var(--ink)}
.chain>.n+.n::after{content:"";position:absolute;left:-10px;top:calc(50%% - 5px);border:5px solid transparent;border-left:7px solid var(--ink)}
.chain>.ar{flex:0 0 auto;min-width:56px;text-align:center;font-size:12.5px;color:var(--muted);position:relative;padding:0 6px 14px}
.chain>.ar::after{content:"";position:absolute;left:4px;right:10px;bottom:6px;border-top:2px solid var(--ink)}
.chain>.ar::before{content:"";position:absolute;right:2px;bottom:1px;border:5px solid transparent;border-left:8px solid var(--ink)}
.tree{overflow-x:auto;text-align:center}
.tree ul{display:flex;justify-content:center;padding:18px 0 0;margin:0;position:relative;list-style:none}
.tree>ul{padding-top:0}
.tree li{position:relative;padding:18px 6px 0;margin:0;display:flex;flex-direction:column;align-items:center}
.tree li::before,.tree li::after{content:"";position:absolute;top:0;right:50%%;width:50%%;height:18px;border-top:2px solid var(--ink)}
.tree li::after{right:auto;left:50%%;border-left:2px solid var(--ink)}
.tree li:only-child::before,.tree li:only-child::after{border-top:0}
.tree li:first-child::before,.tree li:last-child::after{border-top:0}
.tree li:last-child::before{border-right:2px solid var(--ink);border-radius:0 6px 0 0}
.tree li:first-child::after{border-radius:6px 0 0 0}
.tree>ul>li{padding-top:0}.tree>ul>li::before,.tree>ul>li::after{display:none}
.tree ul ul::before{content:"";position:absolute;top:0;left:50%%;height:18px;border-left:2px solid var(--ink)}
.tree li>span{display:inline-block;border:1.8px solid var(--ink);background:var(--boxfill);border-radius:6px;padding:5px 10px;font-size:14.5px;line-height:1.3;max-width:180px}
.tree li>span.hi{background:var(--hifill)}
.stack{display:flex;flex-direction:column;gap:6px;max-width:560px;margin:0 auto}
.stack>.l{border:1.8px solid var(--ink);border-radius:6px;padding:8px 12px;text-align:center;background:var(--boxfill)}
.stack>.l.hi{background:var(--hifill)}.stack>.l small{display:block;color:var(--muted);font-size:13px}
.stack .row{display:flex;gap:6px}.stack .row>.l{flex:1;border:1.8px solid var(--ink);border-radius:6px;padding:8px;text-align:center;background:var(--boxfill)}
.boxes{display:grid;gap:10px;grid-template-columns:repeat(var(--c,2),minmax(0,1fr))}
.boxes.c3{--c:3}.boxes.c4{--c:4}.boxes.c5{--c:5}
.boxes>.b{border:1.8px solid var(--ink);border-radius:8px;padding:8px 10px;background:var(--boxfill);font-size:14.5px;line-height:1.45}
.boxes>.b>b:first-child{display:block;color:var(--brand2);font-size:15.5px;margin-bottom:2px}
.boxes>.b.hi{background:var(--hifill)}
svg.sv{display:block;margin:0 auto;max-width:100%%;height:auto;font-family:var(--body)}
.sv rect,.sv circle,.sv ellipse,.sv polygon{fill:var(--boxfill);stroke:var(--ink);stroke-width:1.8}
.sv line,.sv path,.sv polyline{fill:none;stroke:var(--ink);stroke-width:1.8}
.sv .arr{marker-end:url(#ah)}.sv .arr2{marker-start:url(#ahs);marker-end:url(#ah)}
.sv .hi{fill:var(--hifill)}.sv .acc{stroke:var(--brand)}.sv .dash{stroke-dasharray:6 5}
.sv .dot{fill:var(--ink);stroke:none}.sv .dot.acc{fill:var(--brand)}.sv .none{fill:none}
.sv text{font-size:14px;fill:var(--ink);stroke:none;text-anchor:middle;dominant-baseline:middle}
.sv text.l{text-anchor:start}.sv text.r{text-anchor:end}.sv text.s{font-size:12px;fill:var(--muted)}.sv text.b{font-weight:700}
.sa dt{font-weight:700;margin-top:14px}.sa dd{margin:4px 0 0 0;padding-left:14px;border-left:3px solid var(--rule)}
.top{display:block;text-align:right;font-size:13px;margin-top:6px}
#zoom{position:fixed;inset:0;background:rgba(20,18,15,.92);display:none;z-index:9;overflow:auto;padding:54px 12px 20px}
#zoom.on{display:block}#zoom .zb{position:fixed;top:10px;right:12px;display:flex;gap:8px;z-index:10}
#zoom button{font:600 16px var(--body);border:0;border-radius:8px;padding:6px 14px;cursor:pointer}
#zoom .zc{background:#fff;border-radius:12px;padding:16px;margin:0 auto;transform-origin:top center}
@media (max-width:640px){.boxes.c3,.boxes.c4,.boxes.c5{--c:2}
body{font-size:16px;line-height:1.65}
main{padding:0 14px 60px}
.topic{background:none;border:0;border-top:1px solid var(--rule);border-radius:0;padding:2px 0 20px;margin:28px 0 0}
.topic>h3{margin:16px 0 10px;font-size:21px}
svg.sv{max-width:none}
figure.fig{border:0;border-radius:0;background:none;padding:8px 0 4px}
figure.fig .canvas{overscroll-behavior-x:contain;padding:2px 0}
.def,.mn,.note,.recall,.ex,.hook,.draw{border:0;border-left:3px solid var(--rule);border-radius:0;background:none;padding:6px 0 6px 12px}
.def{border-left-color:var(--brand)}.mn{border-left-color:#d4a514}.note{border-left-color:#e2919f}
.recall{border-left-color:#7fbd9a}.hook{border-left-color:var(--brand);font-size:16px}
li{margin:9px 0}ul,ol{padding-left:20px}
.chain{flex-direction:column;width:auto;min-width:0}
.chain>.n{max-width:100%%;width:100%%}
.chain>.n+.n{margin-left:0;margin-top:30px}
.chain>.n+.n::before{left:50%%;top:-26px;width:0;height:18px;border-top:0;border-left:2px solid var(--ink)}
.chain>.n+.n::after{left:calc(50%% - 5px);top:-10px;border:5px solid transparent;border-top:7px solid var(--ink)}
.chain>.ar{min-width:0;width:100%%;padding:18px 0 6px}
.chain>.ar::after{left:50%%;right:auto;top:0;bottom:auto;width:0;height:11px;border-top:0;border-left:2px solid var(--ink)}
.chain>.ar::before{left:calc(50%% - 5px);right:auto;top:9px;bottom:auto;border:5px solid transparent;border-top:8px solid var(--ink)}
.top{padding:8px 0;font-size:14px}
.sa dd{padding-left:10px}}
@media print{.cover{background:none;color:#000;padding:0}.cover .chips,nav.toc,.top,#zoom{display:none}
.topic,figure.fig{break-inside:avoid-page;box-shadow:none}body{background:#fff;font-size:12pt}}
"""

JS = r"""
(function(){var z=document.getElementById('zoom'),c=z.querySelector('.zc'),s=1;
function set(){c.style.transform='scale('+s+')';}
document.querySelectorAll('figure.fig').forEach(function(f){f.addEventListener('click',function(){
c.innerHTML='';var k=f.cloneNode(true);k.style.cursor='default';c.appendChild(k);s=1;
c.style.width=Math.max(f.scrollWidth,Math.min(window.innerWidth-40,1100))+'px';set();z.classList.add('on');});});
z.querySelector('.zin').onclick=function(e){e.stopPropagation();s=Math.min(s+.25,3);set();};
z.querySelector('.zout').onclick=function(e){e.stopPropagation();s=Math.max(s-.25,.5);set();};
z.querySelector('.zx').onclick=function(){z.classList.remove('on');};
z.addEventListener('click',function(e){if(e.target===z)z.classList.remove('on');});
document.addEventListener('keydown',function(e){if(e.key==='Escape')z.classList.remove('on');});})();
"""

DEFS = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'
        '<marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10 z" style="fill:#1d1b18;stroke:none"/></marker>'
        '<marker id="ahs" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10 z" style="fill:#1d1b18;stroke:none"/></marker></defs></svg>')

DEFS_MODERN = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'
        '<marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10 z" style="fill:var(--ink);stroke:none"/></marker>'
        '<marker id="ahs" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10 z" style="fill:var(--ink);stroke:none"/></marker></defs></svg>')

CSS_MODERN = r"""
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,600&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
  --brand: %(brand)s;
  --brand2: %(brand2)s;
  --brand-glow: color-mix(in srgb, var(--brand) 25%%, transparent);
  --paper: #f8fafc;
  --card: #ffffff;
  --card-subtle: #f1f5f9;
  --ink: #0f172a;
  --muted: #475569;
  --rule: #e2e8f0;
  --soft: color-mix(in srgb, var(--brand) 7%%, #ffffff);
  --boxfill: #ffffff;
  --hifill: color-mix(in srgb, var(--brand) 12%%, #ffffff);
  --mark: #fef08a;
  --good: #15803d;
  --good-bg: #f0fdf4;
  --good-border: #bbf7d0;
  --bad: #be123c;
  --bad-bg: #fff1f2;
  --bad-border: #fecdd3;
  --warn: #b45309;
  --warn-bg: #fffbeb;
  --warn-border: #fde68a;
  --shadow-xs: 0 1px 2px rgba(15, 23, 42, 0.05);
  --shadow-sm: 0 1px 3px rgba(15, 23, 42, 0.06), 0 1px 2px rgba(15, 23, 42, 0.04);
  --shadow-md: 0 4px 14px -2px rgba(15, 23, 42, 0.08), 0 2px 6px -2px rgba(15, 23, 42, 0.04);
  --shadow-lg: 0 12px 28px -4px rgba(15, 23, 42, 0.12), 0 4px 10px -2px rgba(15, 23, 42, 0.05);
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 14px;
  --radius-xl: 18px;
  --body: "Plus Jakarta Sans", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --disp: "Outfit", "Plus Jakarta Sans", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --mono: "JetBrains Mono", "Cascadia Code", "Fira Code", Menlo, Consolas, monospace;
  --maxw: 960px;
}


* { box-sizing: border-box; }
html { scroll-behavior: auto; }
body {
  margin: 0;
  background: var(--paper);
  color: var(--ink);
  font: 16.5px/1.65 var(--body);
  letter-spacing: -0.01em;
  -webkit-text-size-adjust: 100%%;
  transition: background-color 0.25s ease, color 0.25s ease;
}
main {
  max-width: var(--maxw);
  margin: 0 auto;
  padding: 0 20px 90px;
}
a {
  color: var(--brand);
  text-decoration: underline;
  text-decoration-thickness: 1.5px;
  text-underline-offset: 3px;
  transition: color 0.15s ease;
}
a:hover {
  color: var(--brand2);
}

/* Cover / Header */
.cover {
  position: relative;
  background: radial-gradient(circle at 85%% 15%%, color-mix(in srgb, var(--brand) 40%%, transparent) 0%%, transparent 60%%),
              radial-gradient(circle at 15%% 90%%, color-mix(in srgb, var(--brand2) 50%%, transparent) 0%%, transparent 50%%),
              linear-gradient(135deg, var(--brand2) 0%%, #090d16 100%%);
  color: #ffffff;
  padding: 52px 20px 42px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  overflow: hidden;
}
.cover::after {
  content: "";
  position: absolute;
  inset: 0;
  background-image: radial-gradient(rgba(255, 255, 255, 0.08) 1px, transparent 1px);
  background-size: 24px 24px;
  pointer-events: none;
  opacity: 0.6;
}
.cover .in {
  position: relative;
  z-index: 1;
  max-width: var(--maxw);
  margin: 0 auto;
}
.cover .code {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font: 600 12px/1 var(--mono);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(8px);
  border-radius: 9999px;
  padding: 6px 14px;
  margin-bottom: 14px;
  color: #f1f5f9;
}
.cover .code::before {
  content: "";
  width: 7px;
  height: 7px;
  border-radius: 50%%;
  background: #34d399;
  box-shadow: 0 0 8px #34d399;
}
.cover h1 {
  font: 800 clamp(30px, 5.2vw, 44px)/1.15 var(--disp);
  letter-spacing: -0.03em;
  margin: 4px 0 12px;
  color: #ffffff;
  text-wrap: balance;
}
.cover p {
  margin: 0;
  font-size: 16px;
  line-height: 1.6;
  opacity: 0.92;
  max-width: 65ch;
  color: #e2e8f0;
}
.cover .chips {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 20px;
}
.cover .chips a {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #ffffff;
  text-decoration: none;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.22);
  backdrop-filter: blur(6px);
  border-radius: 9999px;
  padding: 6px 16px;
  font-size: 13.5px;
  font-weight: 600;
  letter-spacing: -0.01em;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}
.cover .chips a:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}
.cover .chips a:active {
  transform: translateY(0) scale(0.98);
}

/* Table of contents */
nav.toc {
  background: var(--card);
  border: 1px solid var(--rule);
  border-radius: var(--radius-lg);
  margin: 28px 0;
  padding: 8px 20px;
  box-shadow: var(--shadow-sm);
  transition: all 0.2s ease;
}
nav.toc summary {
  cursor: pointer;
  font-weight: 700;
  font-size: 16px;
  letter-spacing: -0.01em;
  padding: 10px 0;
  list-style: none;
  display: flex;
  align-items: center;
  justify-content: space-between;
  user-select: none;
}
nav.toc summary::-webkit-details-marker { display: none; }
nav.toc summary::after {
  content: "▾";
  font-size: 16px;
  transition: transform 0.2s;
  color: var(--muted);
}
nav.toc[open] summary::after {
  transform: rotate(180deg);
}
.toc-filter {
  width: 100%%;
  box-sizing: border-box;
  padding: 8px 12px 8px 34px;
  margin: 4px 0 12px;
  font: 500 14px var(--body);
  color: var(--ink);
  background: var(--paper);
  border: 1px solid var(--rule);
  border-radius: var(--radius-sm);
  outline: none;
  background-image: url("data:image/svg+xml,%%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%%2364748b' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%%3E%%3Ccircle cx='11' cy='11' r='8'%%3E%%3C/circle%%3E%%3Cline x1='21' y1='21' x2='16.65' y2='16.65'%%3E%%3C/line%%3E%%3C/svg%%3E");
  background-repeat: no-repeat;
  background-position: 10px center;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.toc-filter:focus {
  border-color: var(--brand);
  box-shadow: 0 0 0 3px var(--brand-glow);
}
nav.toc ol {
  margin: 6px 0 16px;
  padding-left: 20px;
}
nav.toc li {
  margin: 5px 0;
  font-size: 15px;
  line-height: 1.5;
}
nav.toc li a {
  color: var(--ink);
  text-decoration: none;
  transition: color 0.15s;
}
nav.toc li a:hover {
  color: var(--brand);
  text-decoration: underline;
}
nav.toc .tu {
  font-weight: 700;
  font-size: 15.5px;
  margin-top: 14px;
  color: var(--brand);
}

/* Units & Topics */
.unit > h2 {
  font: 800 clamp(25px, 4.2vw, 32px)/1.2 var(--disp);
  letter-spacing: -0.03em;
  margin: 64px 0 8px;
  padding-top: 20px;
  border-top: 3px solid var(--brand);
  color: var(--ink);
}
.unit > h2 .uno {
  display: block;
  font: 700 12px/1.2 var(--mono);
  letter-spacing: 0.14em;
  color: var(--brand);
  text-transform: uppercase;
  margin-bottom: 6px;
}
.unit-sub {
  color: var(--muted);
  font-size: 15px;
  margin: 0 0 16px;
}
.topic {
  background: var(--card);
  border: 1px solid var(--rule);
  border-radius: var(--radius-lg);
  padding: 24px 28px;
  margin: 28px 0;
  scroll-margin-top: 24px;
  box-shadow: var(--shadow-sm);
  transition: border-color 0.2s, box-shadow 0.2s;
}
.topic:hover {
  border-color: color-mix(in srgb, var(--brand) 30%%, var(--rule));
  box-shadow: var(--shadow-md);
}
.topic > h3 {
  font: 700 clamp(20px, 3.2vw, 23px)/1.3 var(--disp);
  letter-spacing: -0.02em;
  margin: 0 0 16px;
  color: var(--ink);
}
h4 {
  font: 700 17.5px/1.4 var(--disp);
  letter-spacing: -0.01em;
  margin: 26px 0 8px;
  color: var(--ink);
}

/* Callouts */
.hook {
  font-size: 16px;
  line-height: 1.6;
  background: var(--soft);
  border: 1px solid color-mix(in srgb, var(--brand) 20%%, transparent);
  border-left: 4px solid var(--brand);
  padding: 12px 16px;
  border-radius: 0 var(--radius-md) var(--radius-md) 0;
  margin: 16px 0;
  color: var(--ink);
}
.def {
  background: var(--soft);
  border: 1px solid color-mix(in srgb, var(--brand) 25%%, var(--rule));
  border-left: 4px solid var(--brand);
  border-radius: var(--radius-md);
  padding: 14px 18px;
  margin: 18px 0;
  line-height: 1.65;
  box-shadow: var(--shadow-xs);
}
.def > b:first-child {
  display: inline-block;
  color: var(--brand);
  font-weight: 700;
  letter-spacing: -0.01em;
  margin-right: 4px;
}
ul, ol { padding-left: 24px; }
li { margin: 6px 0; }
mark {
  background: var(--mark);
  padding: 1px 4px;
  border-radius: 3px;
  color: inherit;
  -webkit-box-decoration-break: clone;
  box-decoration-break: clone;
}
.hg {
  color: var(--muted);
  font-style: italic;
  font-size: 0.93em;
}
.mn {
  background: var(--warn-bg);
  border: 1.5px dashed var(--warn-border);
  border-radius: var(--radius-md);
  padding: 14px 18px;
  margin: 18px 0;
  line-height: 1.65;
}
.mn > b:first-child {
  display: block;
  font: 700 12px/1 var(--mono);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--warn);
  margin-bottom: 6px;
}
.recall {
  background: var(--good-bg);
  border: 1px solid var(--good-border);
  border-left: 4px solid var(--good);
  border-radius: var(--radius-md);
  padding: 14px 18px;
  margin: 18px 0;
  line-height: 1.65;
}
.recall > b:first-child {
  display: block;
  font: 700 12px/1 var(--mono);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--good);
  margin-bottom: 6px;
}
.note {
  background: var(--bad-bg);
  border: 1px solid var(--bad-border);
  border-left: 4px solid var(--bad);
  border-radius: var(--radius-md);
  padding: 14px 18px;
  margin: 18px 0;
  line-height: 1.65;
}
.note > b:first-child {
  color: var(--bad);
  font-weight: 700;
}

/* Tables */
.tw {
  overflow-x: auto;
  margin: 18px 0;
  border: 1px solid var(--rule);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-xs);
  background: var(--card);
}
table {
  border-collapse: collapse;
  width: 100%%;
  font-size: 15px;
  line-height: 1.5;
  background: transparent;
  min-width: 520px;
}
th, td {
  border: 1px solid var(--rule);
  padding: 10px 14px;
  text-align: left;
  vertical-align: top;
}
th {
  background: var(--soft);
  color: var(--brand);
  font-weight: 700;
  font-size: 13.5px;
  letter-spacing: 0.03em;
  text-transform: uppercase;
}
tr:nth-child(even) td {
  background: color-mix(in srgb, var(--card-subtle) 40%%, transparent);
}
tr:hover td {
  background: color-mix(in srgb, var(--brand) 4%%, transparent);
}

/* Code Blocks */
pre {
  font: 14px/1.6 var(--mono);
  font-variant-ligatures: none;
  overflow-x: auto;
  border-radius: var(--radius-md);
  padding: 14px 16px;
  margin: 16px 0;
}
pre.code {
  position: relative;
  background: #0f172a;
  color: #e2e8f0;
  border: 1px solid #1e293b;
  padding: 38px 16px 14px;
  box-shadow: var(--shadow-md);
}
pre.code[data-file]::before {
  content: attr(data-file);
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 28px;
  background: #1e293b;
  color: #94a3b8;
  font: 600 12px/28px var(--mono);
  padding: 0 14px;
  border-bottom: 1px solid #334155;
  border-radius: var(--radius-md) var(--radius-md) 0 0;
}
pre.out {
  background: #090d16;
  color: #4ade80;
  border: 1px solid #1e293b;
  padding: 34px 16px 14px;
  position: relative;
  box-shadow: var(--shadow-sm);
}
pre.out::before {
  content: "terminal output";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 26px;
  background: #141c2e;
  color: #64748b;
  font: 600 11px/26px var(--mono);
  letter-spacing: 0.06em;
  text-transform: uppercase;
  padding: 0 14px;
  border-bottom: 1px solid #1e293b;
}
.code .c { color: #94a3b8; font-style: italic; }
.code .k { color: #38bdf8; font-weight: 600; }
code {
  font-family: var(--mono);
  font-size: 0.9em;
  background: var(--card-subtle);
  border: 1px solid var(--rule);
  color: var(--brand);
  padding: 1px 6px;
  border-radius: 4px;
}
pre code {
  background: none;
  border: none;
  color: inherit;
  padding: 0;
}
.copy-btn {
  position: absolute;
  top: 4px;
  right: 8px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: #cbd5e1;
  border-radius: 4px;
  padding: 2px 8px;
  font: 600 11px var(--mono);
  cursor: pointer;
  transition: all 0.15s;
  z-index: 2;
}
.copy-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  color: #ffffff;
}

.ex {
  border: 1px solid var(--rule);
  border-radius: var(--radius-md);
  padding: 14px 18px;
  margin: 18px 0;
  background: var(--card-subtle);
  box-shadow: var(--shadow-xs);
}
.ex > b:first-child {
  display: block;
  color: var(--brand);
  font-weight: 700;
  margin-bottom: 8px;
}
.ex .step {
  margin: 8px 0;
  font-size: 15.5px;
  overflow-x: auto;
  overflow-y: hidden;
}
.ans {
  display: inline-flex;
  align-items: center;
  border: 2px solid var(--good);
  background: var(--good-bg);
  color: var(--good);
  border-radius: var(--radius-sm);
  padding: 2px 10px;
  font-weight: 700;
  font-size: 14.5px;
  margin: 6px 0;
}

/* Figures & Diagrams */
figure.fig {
  margin: 22px 0;
  border: 1px solid var(--rule);
  border-radius: var(--radius-lg);
  background: var(--card);
  padding: 18px 16px 14px;
  cursor: zoom-in;
  box-shadow: var(--shadow-xs);
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}
figure.fig:hover {
  border-color: color-mix(in srgb, var(--brand) 30%%, var(--rule));
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}
figure.fig .canvas {
  overflow-x: auto;
  padding: 8px 4px;
}
figcaption {
  font-size: 14px;
  color: var(--muted);
  text-align: center;
  margin-top: 10px;
}
figcaption b {
  color: var(--ink);
  font-weight: 700;
}
.draw {
  font-size: 13.5px;
  font-weight: 500;
  background: var(--soft);
  border: 1px solid color-mix(in srgb, var(--brand) 20%%, transparent);
  border-radius: var(--radius-sm);
  padding: 6px 12px;
  margin: 10px 0 0;
  color: var(--ink);
}
.n {
  border: 1.5px solid var(--ink);
  background: var(--boxfill);
  border-radius: 8px;
  padding: 8px 14px;
  text-align: center;
  font-size: 14.5px;
  font-weight: 500;
  line-height: 1.35;
  box-shadow: var(--shadow-xs);
}
.n.t {
  border-radius: 9999px;
  background: var(--hifill);
}
.n.hi {
  background: var(--hifill);
  border-color: var(--brand);
}
.n.io, .n.d {
  border: 0;
  border-radius: 0;
  background: no-repeat center/100%% 100%%;
  box-shadow: none;
}
.n.io {
  padding: 6px 26px;
  background-image: url("data:image/svg+xml,%%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 40' preserveAspectRatio='none'%%3E%%3Cpolygon points='10,1 99,1 90,39 1,39' fill='%%23ffffff' stroke='%%230f172a' stroke-width='1.5' vector-effect='non-scaling-stroke'/%%3E%%3C/svg%%3E");
}
.n.d {
  padding: 10px 34px;
  background-image: url("data:image/svg+xml,%%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 40' preserveAspectRatio='none'%%3E%%3Cpolygon points='50,1 99,20 50,39 1,20' fill='%%23fff7ed' stroke='%%230f172a' stroke-width='1.5' vector-effect='non-scaling-stroke'/%%3E%%3C/svg%%3E");
}
.n small {
  display: block;
  color: var(--muted);
  font-size: 12px;
}
.flow {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 26px;
  margin: 6px auto;
  width: max-content;
  max-width: 100%%;
}
.flow > .n {
  position: relative;
  min-width: 180px;
  max-width: 360px;
}
.flow > .n + .n::before {
  content: "";
  position: absolute;
  left: calc(50%% - 1px);
  top: -25px;
  height: 20px;
  border-left: 2px solid var(--ink);
}
.flow > .n + .n::after {
  content: "";
  position: absolute;
  left: calc(50%% - 5px);
  top: -8px;
  border: 5px solid transparent;
  border-top: 7px solid var(--ink);
}
.flow > .ar {
  margin: -22px 0;
  font-size: 12.5px;
  color: var(--muted);
}
.chain {
  display: flex;
  align-items: center;
  gap: 0;
  width: max-content;
  min-width: 100%%;
  justify-content: center;
}
.chain > .n {
  flex: 0 0 auto;
  max-width: 190px;
}
.chain > .n + .n {
  margin-left: 40px;
  position: relative;
}
.chain > .n + .n::before {
  content: "";
  position: absolute;
  left: -36px;
  top: 50%%;
  width: 28px;
  border-top: 2px solid var(--ink);
}
.chain > .n + .n::after {
  content: "";
  position: absolute;
  left: -10px;
  top: calc(50%% - 5px);
  border: 5px solid transparent;
  border-left: 7px solid var(--ink);
}
.chain > .ar {
  flex: 0 0 auto;
  min-width: 56px;
  text-align: center;
  font-size: 12px;
  color: var(--muted);
  position: relative;
  padding: 0 6px 14px;
}
.chain > .ar::after {
  content: "";
  position: absolute;
  left: 4px;
  right: 10px;
  bottom: 6px;
  border-top: 2px solid var(--ink);
}
.chain > .ar::before {
  content: "";
  position: absolute;
  right: 2px;
  bottom: 1px;
  border: 5px solid transparent;
  border-left: 8px solid var(--ink);
}
.tree {
  overflow-x: auto;
  text-align: center;
}
.tree ul {
  display: flex;
  justify-content: center;
  padding: 18px 0 0;
  margin: 0;
  position: relative;
  list-style: none;
}
.tree > ul { padding-top: 0; }
.tree li {
  position: relative;
  padding: 18px 6px 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.tree li::before, .tree li::after {
  content: "";
  position: absolute;
  top: 0;
  right: 50%%;
  width: 50%%;
  height: 18px;
  border-top: 2px solid var(--ink);
}
.tree li::after {
  right: auto;
  left: 50%%;
  border-left: 2px solid var(--ink);
}
.tree li:only-child::before, .tree li:only-child::after { border-top: 0; }
.tree li:first-child::before, .tree li:last-child::after { border-top: 0; }
.tree li:last-child::before {
  border-right: 2px solid var(--ink);
  border-radius: 0 6px 0 0;
}
.tree li:first-child::after {
  border-radius: 6px 0 0 0;
}
.tree > ul > li { padding-top: 0; }
.tree > ul > li::before, .tree > ul > li::after { display: none; }
.tree ul ul::before {
  content: "";
  position: absolute;
  top: 0;
  left: 50%%;
  height: 18px;
  border-left: 2px solid var(--ink);
}
.tree li > span {
  display: inline-block;
  border: 1.5px solid var(--ink);
  background: var(--boxfill);
  border-radius: 8px;
  padding: 6px 12px;
  font-size: 14px;
  font-weight: 500;
  line-height: 1.3;
  max-width: 180px;
  box-shadow: var(--shadow-xs);
}
.tree li > span.hi { background: var(--hifill); border-color: var(--brand); }
.stack {
  display: flex;
  flex-direction: column;
  gap: 6px;
  max-width: 560px;
  margin: 0 auto;
}
.stack > .l {
  border: 1.5px solid var(--ink);
  border-radius: 8px;
  padding: 8px 12px;
  text-align: center;
  background: var(--boxfill);
  box-shadow: var(--shadow-xs);
}
.stack > .l.hi { background: var(--hifill); border-color: var(--brand); }
.stack > .l small { display: block; color: var(--muted); font-size: 12px; }
.stack .row { display: flex; gap: 6px; }
.stack .row > .l {
  flex: 1;
  border: 1.5px solid var(--ink);
  border-radius: 8px;
  padding: 8px;
  text-align: center;
  background: var(--boxfill);
}
.boxes {
  display: grid;
  gap: 12px;
  grid-template-columns: repeat(var(--c, 2), minmax(0, 1fr));
}
.boxes.c3 { --c: 3; } .boxes.c4 { --c: 4; } .boxes.c5 { --c: 5; }
.boxes > .b {
  border: 1.5px solid var(--rule);
  border-radius: var(--radius-md);
  padding: 12px 14px;
  background: var(--card-subtle);
  font-size: 14.5px;
  line-height: 1.45;
  box-shadow: var(--shadow-xs);
  transition: all 0.15s;
}
.boxes > .b:hover {
  border-color: var(--brand);
}
.boxes > .b > b:first-child {
  display: block;
  color: var(--brand);
  font-size: 15px;
  margin-bottom: 4px;
}
.boxes > .b.hi {
  background: var(--hifill);
  border-color: var(--brand);
}
svg.sv {
  display: block;
  margin: 0 auto;
  max-width: 100%%;
  height: auto;
  font-family: var(--body);
}
.sv rect, .sv circle, .sv ellipse, .sv polygon {
  fill: var(--boxfill);
  stroke: var(--ink);
  stroke-width: 1.5;
}
.sv line, .sv path, .sv polyline {
  fill: none;
  stroke: var(--ink);
  stroke-width: 1.5;
}
.sv .arr { marker-end: url(#ah); }
.sv .arr2 { marker-start: url(#ahs); marker-end: url(#ah); }
.sv .hi { fill: var(--hifill); }
.sv .acc { stroke: var(--brand); }
.sv .dash { stroke-dasharray: 6 5; }
.sv .dot { fill: var(--ink); stroke: none; }
.sv .dot.acc { fill: var(--brand); }
.sv .none { fill: none; }
.sv text {
  font-size: 13.5px;
  fill: var(--ink);
  stroke: none;
  text-anchor: middle;
  dominant-baseline: middle;
  font-weight: 500;
}
.sv text.l { text-anchor: start; }
.sv text.r { text-anchor: end; }
.sv text.s { font-size: 11.5px; fill: var(--muted); }
.sv text.b { font-weight: 700; }
.sa {
  margin: 16px 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.sa dt {
  font-family: var(--disp);
  font-weight: 700;
  font-size: 15px;
  color: var(--ink);
  margin-top: 0;
}
.sa dd {
  margin: 4px 0 0 0;
  padding: 8px 14px;
  border-left: 3px solid var(--brand);
  background: var(--card-subtle);
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  font-size: 14.5px;
  line-height: 1.55;
  color: var(--ink);
}

/* 1-Mark Fast-Reading Cards & Supporting Micro-Diagrams */
.qa-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
  gap: 16px;
  margin: 20px 0;
}
.qa-card {
  background: var(--card);
  border: 1px solid var(--rule);
  border-radius: var(--radius-lg);
  padding: 16px 18px;
  box-shadow: var(--shadow-xs);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}
.qa-card:hover {
  border-color: var(--brand);
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}
.qa-header {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 8px;
}
.qa-badge {
  flex-shrink: 0;
  background: var(--soft);
  color: var(--brand);
  font: 700 12px/1.4 var(--mono);
  padding: 2px 7px;
  border-radius: 6px;
  border: 1px solid color-mix(in srgb, var(--brand) 25%%, transparent);
}
.qa-q {
  font-family: var(--disp);
  font-weight: 700;
  font-size: 15px;
  line-height: 1.35;
  color: var(--ink);
  margin: 0;
}
.qa-ans {
  font-size: 14px;
  line-height: 1.6;
  color: var(--ink);
  margin: 0 0 8px;
  flex-grow: 1;
}
.qa-diag {
  background: var(--card-subtle);
  border: 1px solid var(--rule);
  border-radius: var(--radius-md);
  padding: 8px 10px;
  margin: 8px 0;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow-x: auto;
}
.qa-diag svg {
  max-width: 100%%;
  height: auto;
}
.qa-key {
  font-size: 12.5px;
  font-weight: 600;
  background: color-mix(in srgb, var(--brand) 10%%, var(--card));
  border-left: 3px solid var(--brand);
  padding: 5px 10px;
  border-radius: 4px;
  color: var(--ink);
  margin-top: 6px;
}
.top {
  display: inline-block;
  text-align: right;
  font-size: 13px;
  font-weight: 600;
  margin-top: 10px;
  color: var(--muted);
  text-decoration: none;
}
.top:hover { color: var(--brand); text-decoration: underline; }

/* Zoom Lightbox */
#zoom {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.85);
  backdrop-filter: blur(12px);
  display: none;
  z-index: 999;
  overflow: auto;
  padding: 60px 16px 24px;
}
#zoom.on { display: block; }
#zoom .zb {
  position: fixed;
  top: 14px;
  right: 18px;
  display: flex;
  gap: 8px;
  z-index: 1000;
}
#zoom button {
  font: 600 14px var(--body);
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.12);
  color: #ffffff;
  backdrop-filter: blur(8px);
  border-radius: var(--radius-sm);
  padding: 6px 14px;
  cursor: pointer;
  transition: all 0.15s;
}
#zoom button:hover {
  background: rgba(255, 255, 255, 0.25);
}
#zoom .zc {
  background: var(--card);
  border-radius: var(--radius-xl);
  padding: 24px;
  margin: 0 auto;
  transform-origin: top center;
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--rule);
}

/* Floating Tools */
.back-top {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 44px;
  height: 44px;
  border-radius: 50%%;
  background: var(--brand);
  color: #ffffff;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.2);
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  opacity: 0;
  visibility: hidden;
  transform: translateY(12px);
  z-index: 99;
}
.back-top.show {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}
.back-top:hover {
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
}
#progress-bar {
  position: fixed;
  top: 0;
  left: 0;
  height: 3.5px;
  background: linear-gradient(90deg, var(--brand), #38bdf8);
  width: 0%%;
  z-index: 9999;
  transition: width 0.1s linear;
}

@media (max-width: 640px) {
  .boxes.c3, .boxes.c4, .boxes.c5 { --c: 1; }
  body { font-size: 16px; line-height: 1.6; }
  main { padding: 0 12px 60px; }
  .cover { padding: 36px 14px 28px; }
  .cover h1 { font-size: 28px; }
  .topic { padding: 18px 16px; margin: 20px 0; border-radius: var(--radius-md); }
  .chain { flex-direction: column; width: 100%%; min-width: 0; }
  .chain > .n { max-width: 100%%; width: 100%%; }
  .chain > .n + .n { margin-left: 0; margin-top: 26px; }
  .chain > .n + .n::before { left: 50%%; top: -22px; width: 0; height: 16px; border-top: 0; border-left: 2px solid var(--ink); }
  .chain > .n + .n::after { left: calc(50%% - 5px); top: -8px; border: 5px solid transparent; border-top: 7px solid var(--ink); }
  .chain > .ar { min-width: 0; width: 100%%; padding: 16px 0 6px; }
  .chain > .ar::after { left: 50%%; right: auto; top: 0; bottom: auto; width: 0; height: 11px; border-top: 0; border-left: 2px solid var(--ink); }
  .chain > .ar::before { left: calc(50%% - 5px); right: auto; top: 9px; bottom: auto; border: 5px solid transparent; border-top: 8px solid var(--ink); }
  .def, .mn, .note, .recall, .ex, .hook, .draw { padding: 12px 14px; }
  .back-top { bottom: 16px; right: 16px; }
}
@media print {
  #progress-bar, .back-top, #zoom, .copy-btn, .toc-filter, .theme-toggle-btn { display: none !important; }
  .cover { background: none; color: #000; padding: 0; border: none; }
  .cover .chips, nav.toc, .top { display: none; }
  .topic, figure.fig { break-inside: avoid-page; box-shadow: none; border-color: #ccc; }
  body { background: #fff; color: #000; font-size: 11pt; }
}
"""

JS_MODERN = r"""
(function(){
  // 1. Zoom Modal
  var z = document.getElementById('zoom'), c = z ? z.querySelector('.zc') : null, s = 1;
  function set(){ if(c) c.style.transform = 'scale(' + s + ')'; }
  if(z && c) {
    document.querySelectorAll('figure.fig').forEach(function(f){
      f.addEventListener('click', function(){
        c.innerHTML = '';
        var k = f.cloneNode(true);
        k.style.cursor = 'default';
        c.appendChild(k);
        s = 1;
        c.style.width = Math.max(f.scrollWidth, Math.min(window.innerWidth - 40, 1100)) + 'px';
        set();
        z.classList.add('on');
      });
    });
    var zin = z.querySelector('.zin'), zout = z.querySelector('.zout'), zx = z.querySelector('.zx');
    if(zin) zin.onclick = function(e){ e.stopPropagation(); s = Math.min(s + 0.25, 3); set(); };
    if(zout) zout.onclick = function(e){ e.stopPropagation(); s = Math.max(s - 0.25, 0.5); set(); };
    if(zx) zx.onclick = function(){ z.classList.remove('on'); };
    z.addEventListener('click', function(e){ if(e.target === z) z.classList.remove('on'); });
    document.addEventListener('keydown', function(e){ if(e.key === 'Escape') z.classList.remove('on'); });
  }

  // 2. Reading Progress Bar
  var prog = document.createElement('div');
  prog.id = 'progress-bar';
  document.body.appendChild(prog);
  window.addEventListener('scroll', function(){
    var h = document.documentElement.scrollHeight - window.innerHeight;
    var p = h > 0 ? (window.scrollY / h) * 100 : 0;
    prog.style.width = Math.min(100, Math.max(0, p)) + '%';
  }, { passive: true });

  // 3. Back to Top Button
  var btt = document.createElement('button');
  btt.className = 'back-top';
  btt.setAttribute('aria-label', 'Back to top');
  btt.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="18 15 12 9 6 15"></polyline></svg>';
  document.body.appendChild(btt);
  btt.addEventListener('click', function(){
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
  window.addEventListener('scroll', function(){
    if(window.scrollY > 300) {
      btt.classList.add('show');
    } else {
      btt.classList.remove('show');
    }
  }, { passive: true });

  // 4. Code Block Copy Buttons
  document.querySelectorAll('pre.code').forEach(function(block){
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'copy-btn';
    btn.textContent = 'Copy';
    btn.addEventListener('click', function(){
      var code = block.querySelector('code') || block;
      var text = code.innerText || code.textContent;
      navigator.clipboard.writeText(text.trim()).then(function(){
        btn.textContent = 'Copied!';
        btn.style.color = '#4ade80';
        setTimeout(function(){
          btn.textContent = 'Copy';
          btn.style.color = '';
        }, 2000);
      }).catch(function(){
        btn.textContent = 'Failed';
      });
    });
    block.style.position = 'relative';
    block.appendChild(btn);
  });

  // 5. TOC Quick Filter
  var toc = document.querySelector('nav.toc');
  if(toc) {
    var details = toc.querySelector('details');
    var list = toc.querySelector('ol');
    if(details && list) {
      var filter = document.createElement('input');
      filter.type = 'search';
      filter.className = 'toc-filter';
      filter.placeholder = 'Filter topics & questions...';
      filter.setAttribute('aria-label', 'Filter topics');
      details.insertBefore(filter, list);
      filter.addEventListener('input', function(){
        var q = this.value.toLowerCase().trim();
        var items = list.querySelectorAll('li');
        items.forEach(function(li){
          if(li.classList.contains('tu')) return;
          var txt = li.textContent.toLowerCase();
          if(!q || txt.indexOf(q) !== -1) {
            li.style.display = '';
          } else {
            li.style.display = 'none';
          }
        });
      });
    }
  }

  // 6. Theme Switcher (Dark / Light)
  // 6. Enforce Light Theme Only
  try {
    localStorage.removeItem('study_theme');
    document.documentElement.removeAttribute('data-theme');
  } catch(e) {}
})();
"""

VOID = {"br", "img", "hr", "meta", "link", "input", "col", "wbr", "source", "area", "base", "embed", "param", "track"}
SVG_SELF = {"rect", "circle", "ellipse", "line", "path", "polyline", "polygon", "use", "stop"}


class Balance(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.errors, self.ids = [], [], []

    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if k == "id":
                self.ids.append(v)
        if tag not in VOID:
            self.stack.append((tag, self.getpos()))

    def handle_startendtag(self, tag, attrs):
        for k, v in attrs:
            if k == "id":
                self.ids.append(v)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()
            return
        # implicit close of <p>/<li> is tolerated only for those tags
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                bad = [t for t, _ in self.stack[i + 1:]]
                self.errors.append(f"</{tag}> at {self.getpos()} closes unclosed {bad}")
                del self.stack[i:]
                return
        self.errors.append(f"stray </{tag}> at {self.getpos()}")


def text_of(s):
    t = re.sub(r"<(style|script)\b.*?</\1>", " ", s, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t))


KEEP_WHOLE = ("-short", "-long", "-important", "-ready")        # exam-answer sections stay complete
KEEP_BLOCKS = re.compile(r'<(figure) class="fig"|<(div) class="(?:def|tw|mn|note|recall)"')


def _block_end(s, i, tag):
    """End index of the element opening at s[i], counting nested tags of the same name."""
    depth, pat = 0, re.compile(rf"<{tag}\b|</{tag}>")
    for m in pat.finditer(s, i):
        depth += 1 if m.group().startswith(f"<{tag}") else -1
        if depth == 0:
            return m.end()
    raise ValueError(f"unclosed <{tag}> at {i}")


def revision(body):
    """Keep what gets written in the exam: definition, diagrams, difference tables, mnemonics, mistakes,
    recall lines; plus the short-answer / long-frame / important-question sections in full."""
    def topic(m):
        sec, sid = m.group(0), m.group(1)
        if sid.endswith(KEEP_WHOLE):
            return sec
        head = re.search(r"<h3>.*?</h3>", sec, flags=re.S).group(0)
        keep, i = [], 0
        while (b := KEEP_BLOCKS.search(sec, i)):
            end = _block_end(sec, b.start(), b.group(1) or b.group(2))
            keep.append(sec[b.start():end])
            i = end
        return f'<section class="topic" id="{sid}">{head}\n' + "\n".join(keep) + '\n<a class="top" href="#top">↑ top</a></section>'
    return re.sub(r'<section class="topic" id="([^"]+)">.*?</section>', topic, body, flags=re.S)


def cue_sheet(s):
    """Last-minute revision block: one line per question, assembled from the answers' own
    Quick-recall text + figure numbers + mnemonic. Adds no new facts, only re-surfaces them."""
    rows = []
    for m in re.finditer(r'<section class="topic" id="(iq\d+)">\s*<h3>(.*?)</h3>(.*?)</section>', s, flags=re.S):
        qid, head, blk = m.group(1), m.group(2), m.group(3)
        head = re.sub(r"<[^>]+>", "", head).strip()
        rec = re.search(r'<div class="recall">(.*?)</div>', blk, flags=re.S)
        rec = re.sub(r"<b>Quick recall</b>\s*", "", rec.group(1)).strip() if rec else ""
        figs = " &middot; ".join(dict.fromkeys(re.findall(r"<b>(Fig[\w.\s]+?)</b>", blk)))
        mn = re.search(r'<div class="mn">(.*?)</div>', blk, flags=re.S)
        mn = re.sub(r"<b>Mnemonic</b>\s*", "", mn.group(1)).strip() if mn else ""
        bits = [b for b in (rec, f"<b>Draw:</b> {figs}" if figs else "", f"<b>Mnemonic</b> {mn}" if mn else "") if b]
        rows.append(f"<dt>{head}</dt><dd>{' &middot; '.join(bits)}</dd>")
    if not rows:
        return s
    cue = ('<section class="topic" id="cue"><h3>Cue sheet &mdash; every answer in one screen</h3>\n'
           '<p class="hook">Revise from this first: each line is the skeleton of that answer &mdash; '
           'the recall points, the figure to draw, and the mnemonic. Expand it into sentences in the exam.</p>\n'
           f'<dl class="sa">{"".join(rows)}</dl>\n<a class="top" href="#top">&uarr; top</a></section>\n\n')
    return s.replace('<section class="topic" id="iq1">', cue + '<section class="topic" id="iq1">', 1)


def build_imp(key, cfg, page, body, full_out):
    """frag/<key>-imp.html (important-question 8-mark answers) -> sessional/<key>-important.html, same shell."""
    f = FRAG / f"{key}-imp.html"
    if not f.exists():
        return
    s = f.read_text(encoding="utf-8")
    errs = []
    p = Balance(); p.feed(s); p.close()
    errs += p.errors[:8] + ([f"unclosed {[t for t, _ in p.stack[:6]]}"] if p.stack else [])
    figs_raw = re.findall(r"<figcaption><b>Fig\.?\s*([^<]+)</b>", s)
    nums = [m.split()[0] for m in figs_raw if "(reused)" not in m.lower() and "(repeated)" not in m.lower()]
    errs += [f"duplicate figure {n}" for n in sorted({n for n in nums if nums.count(n) > 1})]
    errs += [f"duplicate id {i}" for i in sorted({i for i in p.ids if p.ids.count(i) > 1})]
    errs += [f"dead anchor #{a}" for a in set(re.findall(r'href="#([^"]+)"', s)) if a not in p.ids and a != "top"]
    if key in MATH_SUBJECTS and not errs:
        tin, tout = HERE / "tmp" / f"{key}-imp-in.html", HERE / "tmp" / f"{key}-imp-math.html"
        tin.write_text(s, encoding="utf-8")
        r = subprocess.run(["node", str(HERE / "render_math.mjs"), str(tin), str(tout)], capture_output=True, text=True)
        if r.returncode:
            errs.append("math: " + (r.stderr.strip().splitlines() or ["?"])[0][:400])
        else:
            s = tout.read_text(encoding="utf-8")
    if errs:
        for e in errs:
            print(f"  HARD: {f.name}: {e}")
        return
    s = cue_sheet(s)
    toc = "".join(f'<li><a href="#{m.group(1)}">{re.sub("<[^>]+>", "", m.group(2))}</a></li>'
                  for m in re.finditer(r'<section class="topic" id="([^"]+)">\s*<h3>(.*?)</h3>', s, flags=re.S))
    ipage = re.sub(r'<nav class="toc">.*?</nav>',
                   f'<nav class="toc"><details open><summary>Questions</summary><ol>{toc}</ol></details></nav>',
                   page.replace(body, s, 1), count=1, flags=re.S)
    ipage = ipage.replace(
        "Sessional notes &middot; Unit I &amp; Unit II &middot; every syllabus topic, with diagrams you can draw in the exam",
        f"Important questions &middot; exam {cfg['exam']} &middot; 30 marks = 6 &times; 1 + 3 &times; 8 "
        f"&middot; Full notes: <a style=\"color:#fff\" href=\"{full_out.name}\">{full_out.name}</a>", 1).replace(
        "Sessional Notes (Unit I &amp; II)</title>", "Important Questions</title>", 1)
    ipage = re.sub(r'<div class="chips">.*?</div>', "", ipage, count=1, flags=re.S)
    out = SEM5 / "sessional" / f"{key}-important.html"
    out.write_bytes(ipage.encode("utf-8"))
    print(f"   important: WROTE {out.name} | questions={s.count('id=\"iq') - s.count('id=\"iq-1m')} "
          f"figures={s.count('<figure class=')} code={s.count('<pre class=\"code\"')} words={len(text_of(s).split())}")


def build(key):
    cfg = SUBJECTS[key]
    hard, soft = [], []
    parts, toc = [], []
    for u in (1, 2):
        f = FRAG / f"{key}-u{u}.html"
        if not f.exists():
            hard.append(f"missing fragment {f.name}")
            continue
        raw = f.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            hard.append(f"{f.name}: BOM")
        if b"\x00" in raw:
            hard.append(f"{f.name}: NUL byte")
        s = raw.decode("utf-8")
        p = Balance()
        p.feed(s)
        p.close()
        hard += [f"{f.name}: {e}" for e in p.errors[:8]]
        if p.stack:
            hard.append(f"{f.name}: unclosed {[(t, pos) for t, pos in p.stack[:6]]}")
        if re.search(r"[\u2500-\u257f]", s):
            hard.append(f"{f.name}: box-drawing characters (ASCII art banned)")
        if '<section class="unit"' not in s:
            hard.append(f"{f.name}: no <section class=\"unit\">")
        toc.append(f'<li class="tu"><a href="#u{u}">Unit {ROMAN[u-1]} &middot; {cfg["units"][u-1]}</a><ol>')
        for m in re.finditer(r'<section class="topic[^"]*" id="([^"]+)">\s*<h3>(.*?)</h3>', s, flags=re.S):
            toc.append(f'<li><a href="#{m.group(1)}">{re.sub("<[^>]+>", "", m.group(2))}</a></li>')
        toc.append("</ol></li>")
        parts.append(s)
    body = "\n".join(parts)

    # figures
    nfig = len(re.findall(r'<figure class="fig"', body))
    ncap = len(re.findall(r"<figcaption", body))
    if nfig != ncap:
        hard.append(f"figures {nfig} != figcaptions {ncap}")
    nums = re.findall(r"<figcaption><b>Fig\.?\s*(\d+\.\d+)</b>", body)
    dups = sorted({n for n in nums if nums.count(n) > 1})
    if dups:
        hard.append(f"duplicate figure numbers {dups}")
    p = Balance(); p.feed(body); p.close()
    idd = sorted({i for i in p.ids if p.ids.count(i) > 1})
    if idd:
        hard.append(f"duplicate ids {idd}")
    for a in set(re.findall(r'href="#([^"]+)"', body)):
        if a not in p.ids and a != "top":
            hard.append(f"dead anchor #{a}")
    # code blocks: size
    for m in re.finditer(r'<pre class="code"[^>]*>(.*?)</pre>', body, flags=re.S):
        lines = m.group(1).strip("\n").count("\n") + 1
        if lines > 30:
            soft.append(f"code block {lines} lines (>30)")
    # coverage
    txt = text_of(body).lower()
    for u in (0, 1):
        missing = [k for k in cfg["kw"][u] if k.lower() not in txt]
        if missing:
            soft.append(f"Unit {ROMAN[u]} keywords not found: {missing}")

    math_css = ""
    if key in MATH_SUBJECTS and not hard:
        css_file = HERE / "tmp" / "katex-inline.css"
        if not css_file.exists():
            subprocess.run(["node", str(HERE / "render_math.mjs"), "--css", str(css_file)], check=True)
        math_css = css_file.read_text(encoding="utf-8") + ".math-display{display:block;overflow-x:auto;overflow-y:hidden;margin:10px 0;padding:2px 0}.katex{font-size:1.06em}"
        tin, tout = HERE / "tmp" / f"{key}-body.html", HERE / "tmp" / f"{key}-body-math.html"
        tin.write_text(body, encoding="utf-8")
        r = subprocess.run(["node", str(HERE / "render_math.mjs"), str(tin), str(tout)], capture_output=True, text=True)
        if r.returncode:
            hard.append("math: " + (r.stderr.strip().splitlines() or ["?"])[0][:400])
        else:
            body = tout.read_text(encoding="utf-8")
            print("  " + r.stdout.strip())
    elif "$" in body and key not in MATH_SUBJECTS:
        soft.append("contains $ but math rendering is off for this subject")
    chips = "".join(f'<a href="#u{u}">Unit {ROMAN[u-1]} &middot; {cfg["units"][u-1]}</a>' for u in (1, 2))
    active_css = CSS_MODERN if key in ("daav", "java", "speech") else CSS
    active_js = JS_MODERN if key in ("daav", "java", "speech") else JS
    active_defs = DEFS_MODERN if key in ("daav", "java", "speech") else DEFS
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{cfg['title']} &middot; Sessional Notes (Unit I &amp; II)</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>%F0%9F%8E%93</text></svg>">
<style>{active_css % cfg}{math_css}</style>
</head>
<body>
{active_defs}
<header class="cover" id="top"><div class="in">
<div class="code">{cfg['code']} &middot; BCA SEMESTER V</div>
<h1>{cfg['title']}</h1>
<p>Sessional notes &middot; Unit I &amp; Unit II &middot; every syllabus topic, with diagrams you can draw in the exam</p>
<div class="chips">{chips}</div>
</div></header>
<main>
<nav class="toc"><details open><summary>Contents</summary><ol>{''.join(toc)}</ol></details></nav>
{body}
</main>
<div id="zoom"><div class="zb"><button class="zout" type="button">&minus;</button><button class="zin" type="button">+</button><button class="zx" type="button">Close</button></div><div class="zc"></div></div>
<script>{active_js}</script>
</body>
</html>
"""
    out = SEM5 / "sessional" / f"{key}-sessional-u1-u2.html"
    if not hard:
        out.write_bytes(page.encode("utf-8"))
        rev = revision(body)
        rpage = page.replace(body, rev, 1).replace(
            "Sessional notes &middot; Unit I &amp; Unit II &middot; every syllabus topic, with diagrams you can draw in the exam",
            f"Quick revision &middot; exam {cfg['exam']} &middot; definitions, diagrams, differences, mnemonics, "
            f"short answers. Full notes: <a style=\"color:#fff\" href=\"{out.name}\">{out.name}</a>", 1).replace(
            "Sessional Notes (Unit I &amp; II)</title>", "Quick Revision</title>", 1)
        (SEM5 / "sessional" / f"{key}-revision.html").write_bytes(rpage.encode("utf-8"))
        print(f"   revision: {len(text_of(rev).split())} words, {rev.count('<figure class=')} figures")
        build_imp(key, cfg, page, body, out)
    print(f"== {key}: {'WROTE ' + str(out) if not hard else 'NOT WRITTEN'} | figures={nfig} "
          f"topics={body.count('class=\"topic')} code={body.count('<pre class=\"code\"')} words={len(txt.split())}")
    for h in hard:
        print("  HARD:", h)
    for w in soft:
        print("  soft:", w)
    return not hard


if __name__ == "__main__":
    keys = sys.argv[1:] or list(SUBJECTS)
    ok = all([build(k) for k in keys])
    sys.exit(0 if ok else 1)
