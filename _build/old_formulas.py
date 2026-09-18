"""Dump formula-like snippets from the OLD SEM5 notes the owner studied, for notation matching."""
import re, html, io

OUT = io.open("old_formulas.txt", "w", encoding="utf-8")
FILES = {
    "ML": r"C:\Users\ankit\OneDrive\Desktop\SEM5\ML\ml-notes.html",
    "SPEECH": r"C:\Users\ankit\OneDrive\Desktop\SEM5\Speech Audio\speech-audio-notes.html",
}
KEYS = {
    "ML": ["Entropy", "Information Gain", "Gini", "Bayes", "sigmoid", "Sigmoid", "Euclidean", "Manhattan",
           "slope", "intercept", "least squares", "margin", "kernel", "Kernel", "cost", "Cost", "MSE", "hypothesis",
           "z-score", "min-max", "Min-Max", "cosine", "log loss", "gradient"],
    "SPEECH": ["autocorrelation", "Autocorrelation", "SQNR", "SNR", "law", "prediction gain", "Prediction Gain",
               "Levinson", "reflection", "convolution", "Convolution", "periodogram", "Periodogram", "PSD",
               "autoregressive", "AR model", "all-pole", "all-zero", "step size", "Lloyd", "centroid", "LBG",
               "Itakura", "DPCM", "pitch", "Pitch", "predictor", "normal equation", "Yule"],
}
for name, path in FILES.items():
    s = open(path, encoding="utf-8").read()
    # keep formula-bearing blocks: formula boxes, code-ish spans, list items with = sign
    blocks = re.findall(r"<(?:div|p|li|td|span)[^>]*class=\"[^\"]*(?:formula|eq|math|fx)[^\"]*\"[^>]*>(.*?)</(?:div|p|li|td|span)>", s, flags=re.S)
    OUT.write(f"===== {name}: {len(blocks)} formula-class blocks =====\n")
    for b in blocks:
        t = html.unescape(re.sub(r"<[^>]+>", "", b))
        t = re.sub(r"\s+", " ", t).strip()
        if t:
            OUT.write("F: " + t[:220] + "\n")
    text = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<(style|script)\b.*?</\1>", " ", s, flags=re.S)))
    text = re.sub(r"\s+", " ", text)
    OUT.write(f"===== {name}: keyword windows with '=' =====\n")
    seen = set()
    for k in KEYS[name]:
        for m in re.finditer(re.escape(k), text):
            w = text[max(0, m.start() - 60): m.start() + 200]
            if "=" in w and w not in seen:
                seen.add(w)
                OUT.write(f"[{k}] {w}\n")
OUT.close()
print("done")
