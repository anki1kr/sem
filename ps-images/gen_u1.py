from PIL import Image, ImageDraw, ImageFont
import os

OUT = r"c:\Users\ankit\OneDrive\Desktop\sem\ps-images"
os.makedirs(OUT, exist_ok=True)

BRAND=(159,18,57); BRAND_D=(90,8,30); BRAND_L=(255,235,238)
GOLD=(170,100,0); GOLD_L=(255,248,210)
DARK=(18,18,28); GRAY=(95,108,120); GRAY_L=(242,244,247)
WHITE=(255,255,255); BG=(255,252,249)
BLUE=(28,56,140); BLUE_L=(218,230,255)
GREEN=(21,90,50); GREEN_L=(220,252,231)
W=1400; PAD=40

def F(sz,bold=False):
    for p in [f"C:/Windows/Fonts/{'arialbd' if bold else 'arial'}.ttf",
              f"C:/Windows/Fonts/{'calibrib' if bold else 'calibri'}.ttf"]:
        try: return ImageFont.truetype(p,sz)
        except: pass
    return ImageFont.load_default()

def FM(sz):
    for p in ["C:/Windows/Fonts/consola.ttf","C:/Windows/Fonts/cour.ttf","C:/Windows/Fonts/lucon.ttf"]:
        try: return ImageFont.truetype(p,sz)
        except: pass
    return F(sz)

def tw(d,t,f): return d.textbbox((0,0),t,font=f)[2]
def th(d,t,f): return d.textbbox((0,0),t,font=f)[3]-d.textbbox((0,0),t,font=f)[1]

def dtxt(d,x,y,t,f,col=None,cx=0):
    col=col or DARK
    if cx: x=x+(cx-tw(d,t,f))//2
    d.text((x,y),t,font=f,fill=col)
    return th(d,t,f)+4

def dwrap(d,x,y,t,f,mw,col=None,gap=5):
    col=col or DARK
    words=t.split(); lines=[]; cur=[]
    for w in words:
        test=' '.join(cur+[w])
        if tw(d,test,f)<=mw: cur.append(w)
        else:
            if cur: lines.append(' '.join(cur))
            cur=[w]
    if cur: lines.append(' '.join(cur))
    cy=y
    for line in lines:
        d.text((x,cy),line,font=f,fill=col); cy+=th(d,line,f)+gap
    return cy-y

def rr(d,x,y,w,h,fill,stroke=None,r=8,sw=2):
    d.rounded_rectangle([x,y,x+w,y+h],radius=r,fill=fill,outline=stroke,width=sw if stroke else 0)

img=Image.new("RGB",(W,2600),BG)
d=ImageDraw.Draw(img)

FT=F(36,True); FU=F(26,True); FH=F(20,True); FS=F(17,True); FB=F(16); FSM=F(14); FFM=FM(15); FTG=F(13,True)

# HEADER
rr(d,0,0,W,95,BRAND_D,r=0)
dtxt(d,PAD,12,"Unit I · Random Variables & Probability Distributions",FT,WHITE)
dtxt(d,PAD,60,"BCD-202-V  |  ~25/75 Marks  |  6 Distributions to master",FS,GOLD_L)
y=110

# Root
rr(d,PAD,y,W-2*PAD,64,BRAND_L,BRAND,r=10)
dtxt(d,0,y+8,"RANDOM VARIABLE (RV)",FH,BRAND,cx=W)
dtxt(d,0,y+36,"A variable whose value is a numerical outcome of a random experiment",FSM,GRAY,cx=W)
y+=80

# Arrow down
d.line([(W//2,y),(W//2,y+20)],fill=BRAND,width=3)
d.polygon([(W//2-8,y+15),(W//2+8,y+15),(W//2,y+24)],fill=BRAND)
y+=28

# Two columns
CW=(W-3*PAD)//2; LX=PAD; RX=PAD+CW+PAD

# Column headers
rr(d,LX,y,CW,56,BLUE_L,BLUE,r=8)
dtxt(d,LX,y+8,"DISCRETE RV",FH,BLUE,cx=CW)
dtxt(d,LX,y+34,"Countable outcomes: 0, 1, 2, 3 …",FSM,BLUE,cx=CW)

rr(d,RX,y,CW,56,GREEN_L,GREEN,r=8)
dtxt(d,RX,y+8,"CONTINUOUS RV",FH,GREEN,cx=CW)
dtxt(d,RX,y+34,"Uncountable: any real value in a range",FSM,GREEN,cx=CW)
y+=66

# PMF/PDF basics
rr(d,LX,y,CW,88,GRAY_L,None,r=6)
d.text((LX+12,y+8),"PMF:  P(X = x) >= 0",font=FFM,fill=DARK)
d.text((LX+12,y+28),"      Sum P(X = x) = 1  (sum of all probs = 1)",font=FFM,fill=DARK)
d.text((LX+12,y+48),"CDF:  F(x) = P(X <= x) = Sum P(X=k) for k <= x",font=FFM,fill=DARK)
d.text((LX+12,y+68),"      P(a < X <= b) = F(b) - F(a)",font=FFM,fill=DARK)

rr(d,RX,y,CW,88,GRAY_L,None,r=6)
d.text((RX+12,y+8),"PDF:  f(x) >= 0",font=FFM,fill=DARK)
d.text((RX+12,y+28),"      Integral f(x) dx = 1  (from -inf to +inf)",font=FFM,fill=DARK)
d.text((RX+12,y+48),"CDF:  F(x) = Integral f(t) dt  (from -inf to x)",font=FFM,fill=DARK)
d.text((RX+12,y+68),"      P(X=any single pt) = 0 (key diff!)",font=FFM,fill=DARK)
y+=100

d.text((LX,y),"v  DISCRETE DISTRIBUTIONS",font=FS,fill=BLUE)
d.text((RX,y),"v  CONTINUOUS DISTRIBUTIONS",font=FS,fill=GREEN)
y+=28

def dist_card(d,x,y,cw,name,tag,lines,stats,when_txt,nc,nl,sc):
    H=30+len(lines)*24+54+44
    rr(d,x,y,cw,H,WHITE,sc,r=8)
    rr(d,x,y,cw,28,nl,None,r=8)
    d.text((x+10,y+6),name,font=FS,fill=nc)
    tw_tag=d.textbbox((0,0),tag,font=FTG)[2]+14
    rr(d,x+cw-tw_tag-8,y+5,tw_tag,18,nc,None,r=4)
    d.text((x+cw-tw_tag-8+7,y+7),tag,font=FTG,fill=WHITE)
    fy=y+34
    for ln in lines:
        d.text((x+10,fy),ln,font=FFM,fill=DARK); fy+=24
    rr(d,x+8,fy+4,cw-16,26,nl,None,r=4)
    d.text((x+14,fy+8),stats,font=FSM,fill=nc)
    fy+=34
    dwrap(d,x+10,fy+4,"WHEN: "+when_txt,FSM,cw-20,GRAY)
    return H+14

# Binomial vs Uniform
h1=dist_card(d,LX,y,CW,"Binomial  B(n, p)","DISCRETE",[
    "P(X=k) = C(n,k) * p^k * (1-p)^(n-k)",
    "k = 0, 1, 2, ... , n"
],"Mean = np     Var = np(1-p) = npq",
"Fixed n trials. Each has 2 outcomes. P(success)=p constant. Count successes.",
BLUE,BLUE_L,BLUE)

h2=dist_card(d,RX,y,CW,"Uniform  U(a, b)","CONTINUOUS",[
    "f(x) = 1/(b-a)   for a <= x <= b",
    "F(x) = (x-a)/(b-a)"
],"Mean = (a+b)/2     Var = (b-a)^2/12",
"All values in [a,b] equally likely. Flat/rectangular PDF.",
GREEN,GREEN_L,GREEN)
y+=max(h1,h2)

# Geometric vs Exponential
h1=dist_card(d,LX,y,CW,"Geometric  G(p)","DISCRETE",[
    "P(X=k) = (1-p)^(k-1) * p",
    "k = 1, 2, 3, ... (trials until 1st success)"
],"Mean = 1/p     Var = (1-p)/p^2",
"How many trials until FIRST success? Memoryless: P(X>m+n|X>m) = P(X>n).",
BLUE,BLUE_L,BLUE)

h2=dist_card(d,RX,y,CW,"Exponential  Exp(lambda)","CONTINUOUS",[
    "f(x) = lambda * e^(-lambda*x)   for x >= 0",
    "F(x) = 1 - e^(-lambda*x)"
],"Mean = 1/lambda     Var = 1/lambda^2",
"Waiting TIME between events. Only memoryless continuous dist. Pair with Poisson.",
GREEN,GREEN_L,GREEN)
y+=max(h1,h2)

# Poisson vs Normal
h1=dist_card(d,LX,y,CW,"Poisson  P(lambda)","DISCRETE",[
    "P(X=k) = e^(-lambda) * lambda^k / k!",
    "lambda = avg events per unit time/area"
],"Mean = lambda     Var = lambda     (MEAN = VARIANCE)",
"Rare events per unit time/area/space. Approx of Bin(n,p) when n large, p small.",
BLUE,BLUE_L,BLUE)

h2=dist_card(d,RX,y,CW,"Normal  N(mu, sigma^2)","CONTINUOUS",[
    "f(x)=(1/sigma*sqrt(2*pi))*exp(-(x-mu)^2/2*sigma^2)",
    "Std: Z = (X - mu) / sigma   ~   N(0,1)"
],"Mean = mu     Var = sigma^2     Mode = Median = Mean",
"Natural phenomena, CLT. Bell-shaped, symmetric. Use Z-table for probabilities.",
GREEN,GREEN_L,GREEN)
y+=max(h1,h2)+12

# Comparison table
rr(d,PAD,y,W-2*PAD,32,BRAND,None,r=6)
dtxt(d,0,y+7,"TRIGGER WORDS -- Identify distribution from exam question",FS,WHITE,cx=W-2*PAD)
y+=38

rows=[
    ("Distribution","Type","Trigger phrase in question","Key formula to write first"),
    ("Binomial B(n,p)","Discrete","n trials * success/fail * each trial independent","P(X=k)=C(n,k)p^k*q^(n-k)"),
    ("Geometric G(p)","Discrete","FIRST success * until success * number of attempts","P(X=k)=q^(k-1)*p"),
    ("Poisson P(lambda)","Discrete","per hour/km/page * rare event * rate lambda","P(X=k)=e^(-l)*l^k/k!"),
    ("Uniform U(a,b)","Continuous","equally likely * random in range [a,b]","f(x)=1/(b-a)"),
    ("Exponential","Continuous","waiting time * time between * lifetime","f(x)=lambda*e^(-lambda*x)"),
    ("Normal N(mu,s^2)","Continuous","heights/weights * natural * standardise","Z=(X-mu)/sigma"),
]
cws=[220,100,420,W-2*PAD-220-100-420-40]
cxs=[PAD+sum(cws[:i])+i*13 for i in range(4)]
rh=30
for ri,row in enumerate(rows):
    bg=BRAND_L if ri==0 else(GRAY_L if ri%2==0 else WHITE)
    fc=BRAND if ri==0 else DARK
    ff=FS if ri==0 else FSM
    rr(d,PAD,y,W-2*PAD,rh,bg,None,r=0)
    for ci,(cx2,cw2,cell) in enumerate(zip(cxs,cws,row)):
        col=fc
        if ri>0:
            if ci==1: col=BLUE if "Discrete" in cell else GREEN
        d.text((cx2+6,y+7),cell,font=ff,fill=col)
    y+=rh
    d.line([(PAD,y),(W-PAD,y)],fill=(210,210,215),width=1)

y+=20
img=img.crop((0,0,W,y+30))
img.save(os.path.join(OUT,"mindmap-unit1.png"))
print(f"DONE: mindmap-unit1.png  {W}x{y+30}")
