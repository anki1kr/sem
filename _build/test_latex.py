import io
from pylatexenc.latex2text import LatexNodes2Text

conv = LatexNodes2Text()
tests = [
    r"R[k] = \sum x[n] x[n+k]",
    r"H(z) = \frac{1}{A(z)}",
    r"PG = 10 \log_{10} \left( \frac{5.0}{3.0} \right) = 10 \log_{10}(1.6667) = 10 \times (0.22185) = 2.2185 \text{ dB}",
    r"\begin{bmatrix} R[0] & R[1] \\ R[1] & R[0] \end{bmatrix} \begin{bmatrix} a_1 \\ a_2 \end{bmatrix} = \begin{bmatrix} R[1] \\ R[2] \end{bmatrix}",
    r"y = \frac{\ln(1 + 255 \times 0.5)}{\ln(1 + 255)} = \frac{\ln(128.5)}{\ln(256)} = \frac{4.8559}{5.5452} = 0.8757",
    r"a_1^{(1)} = k_1 = 0.6",
    r"R_{biased}[0] = 34/5 = 6.8",
    r"E_2 = (1 - k_2^2) E_1 = (1 - (-0.25)^2) \times 3.2",
]
out = io.open("latex_test_out.txt", "w", encoding="utf-8")
for t in tests:
    out.write("IN : " + t + "\n")
    out.write("OUT: " + conv.latex_to_text(t) + "\n\n")
out.close()
