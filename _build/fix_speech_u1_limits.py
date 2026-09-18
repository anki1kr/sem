from pathlib import Path

p = Path("frag/speech-u1.html")
b = p.read_bytes()
s = b.decode("utf-8")


def swap(old, new):
    global s
    assert s.count(old) == 1, (old, s.count(old))
    s = s.replace(old, new)


swap(r"$$\hat{R}_b[k] = \frac{1}{N}\sum x[n]\,x[n+k]$$",
     r"$$\hat{R}_b[k] = \frac{1}{N}\sum_{n=0}^{N-1-k} x[n]\,x[n+k]$$")
swap(r"$$\hat{R}_u[k] = \frac{1}{N-k}\sum x[n]\,x[n+k]$$",
     r"$$\hat{R}_u[k] = \frac{1}{N-k}\sum_{n=0}^{N-1-k} x[n]\,x[n+k]$$ (the sum has only $N-k$ terms, so dividing by $N-k$ gives a true average)")
line = [l for l in s.split("\n") if r"\hat{S}(\omega) = \frac{1}{N}\left|X(\omega)\right|^2" in l]
assert len(line) == 1
swap(line[0], line[0].rstrip("\r") + r" where $\omega = 2\pi f$ (angular frequency)" + ("\r" if line[0].endswith("\r") else ""))
p.write_bytes(s.encode("utf-8"))
print("ok")
