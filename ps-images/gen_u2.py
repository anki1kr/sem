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
TEAL=(14,116,108); TEAL_L=(200,252,242)
PURPLE=(88,28,135); PURPLE_L=(243,232,255)
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
def th(d,t,f): return max(d.textbbox((0,0),t,font=f)[3]-d.textbbox((0,0),t,font=f)[1],1)

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

FT=F(34,True); FU=F(24,True); FH=F(20,True); FS=F(17,True)
FB=F(16); FSM=F(14); FFM=FM(15); FTG=F(13,True)

# HEADER
rr(d,0,0,W,95,BRAND_D,r=0)
dtxt(d,PAD,12,"Unit II · Expectation, MGF, PGF & 2D Random Variables",FT,WHITE)
dtxt(d,PAD,58,"BCD-202-V  |  ~18/75 Marks  |  Formulas + 2D Joint/Marginal/Conditional",FS,GOLD_L)
y=110

# ── SECTION 1: EXPECTATION ──
rr(d,PAD,y,W-2*PAD,34,BLUE,None,r=6)
dtxt(d,0,y+8,"EXPECTATION  E(X) — Theoretical average of a random variable",FH,WHITE,cx=W-2*PAD)
y+=40

CW=(W-3*PAD)//2; LX=PAD; RX=PAD+CW+PAD

rr(d,LX,y,CW,115,GRAY_L,BLUE,r=6)
d.text((LX+12,y+8),"DISCRETE E(X):",font=FS,fill=BLUE)
d.text((LX+12,y+32),"E(X) = Σ x · P(X = x)",font=FFM,fill=DARK)
d.text((LX+12,y+54),"E(X²) = Σ x² · P(X = x)",font=FFM,fill=DARK)
d.text((LX+12,y+76),"Var(X) = E(X²) - [E(X)]²",font=FFM,fill=DARK)
d.text((LX+12,y+96),"E(aX+b) = a·E(X) + b  (linearity)",font=FSM,fill=GRAY)

rr(d,RX,y,CW,115,GRAY_L,GREEN,r=6)
d.text((RX+12,y+8),"CONTINUOUS E(X):",font=FS,fill=GREEN)
d.text((RX+12,y+32),"E(X) = ∫ x · f(x) dx",font=FFM,fill=DARK)
d.text((RX+12,y+54),"E(X²) = ∫ x² · f(x) dx",font=FFM,fill=DARK)
d.text((RX+12,y+76),"Var(X) = E(X²) - [E(X)]²",font=FFM,fill=DARK)
d.text((RX+12,y+96),"E[g(X)] = ∫ g(x)·f(x) dx  (general)",font=FSM,fill=GRAY)
y+=125

# ── SECTION 2: MGF ──
rr(d,PAD,y,W-2*PAD,34,TEAL,None,r=6)
dtxt(d,0,y+8,"MGF — Moment Generating Function  M(t) = E(eᵗˣ)",FH,WHITE,cx=W-2*PAD)
y+=40

rr(d,LX,y,CW,140,GRAY_L,TEAL,r=6)
d.text((LX+12,y+8),"DEFINITION & MOMENTS:",font=FS,fill=TEAL)
d.text((LX+12,y+32),"M(t) = E(eᵗˣ) = Σ eᵗˣ·P(x)  [discrete]",font=FFM,fill=DARK)
d.text((LX+12,y+54),"M(t) = ∫ eᵗˣ·f(x) dx        [continuous]",font=FFM,fill=DARK)
d.text((LX+12,y+76),"M'(0)  = E(X)          → mean (1st moment)",font=FFM,fill=DARK)
d.text((LX+12,y+98),"M''(0) = E(X²)         → 2nd moment",font=FFM,fill=DARK)
d.text((LX+12,y+118),"Mⁿ(0) = E(Xⁿ) = nth raw moment",font=FFM,fill=DARK)

rr(d,RX,y,CW,140,GRAY_L,TEAL,r=6)
d.text((RX+12,y+8),"STANDARD MGFs TO KNOW:",font=FS,fill=TEAL)
d.text((RX+12,y+30),"Binomial:    M(t) = (q + p·eᵗ)ⁿ",font=FFM,fill=DARK)
d.text((RX+12,y+52),"Poisson:     M(t) = e^(λ(eᵗ-1))",font=FFM,fill=DARK)
d.text((RX+12,y+74),"Geometric:   M(t) = p·eᵗ/(1-q·eᵗ)",font=FFM,fill=DARK)
d.text((RX+12,y+96),"Normal:      M(t) = e^(μt + σ²t²/2)",font=FFM,fill=DARK)
d.text((RX+12,y+118),"Exponential: M(t) = λ/(λ-t),  t < λ",font=FFM,fill=DARK)
y+=152

# ── SECTION 3: PGF ──
rr(d,PAD,y,W-2*PAD,34,PURPLE,None,r=6)
dtxt(d,0,y+8,"PGF — Probability Generating Function  P(s) = E(sˣ)  [DISCRETE only]",FH,WHITE,cx=W-2*PAD)
y+=40

rr(d,PAD,y,W-2*PAD,100,GRAY_L,PURPLE,r=6)
d.text((PAD+12,y+8),"P(s) = Σ pₖ · sᵏ  =  p₀ + p₁s + p₂s² + …",font=FFM,fill=DARK)
d.text((PAD+12,y+30),"MEAN:     P'(1) = E(X)  =  Σ k·pₖ",font=FFM,fill=DARK)
d.text((PAD+12,y+52),"VARIANCE: Var(X) = P''(1) + P'(1) - [P'(1)]²",font=FFM,fill=DARK)
d.text((PAD+12,y+74),"USE: Discrete RVs only. Differentiate at s=1 to get mean. Binomial: P(s)=(q+ps)ⁿ. Poisson: P(s)=e^(λ(s-1)).",font=FSM,fill=GRAY)
y+=112

# ── SECTION 4: 2D RANDOM VARIABLES ──
rr(d,PAD,y,W-2*PAD,34,GREEN,None,r=6)
dtxt(d,0,y+8,"2D RANDOM VARIABLES  (X, Y) — Joint, Marginal, Conditional",FH,WHITE,cx=W-2*PAD)
y+=40

# 4 boxes in 2x2 grid
BW=(W-4*PAD)//3

rr(d,LX,y,BW,150,GOLD_L,GOLD,r=8)
d.text((LX+10,y+8),"JOINT",font=FS,fill=GOLD)
d.line([(LX,y+32),(LX+BW,y+32)],fill=GOLD,width=1)
d.text((LX+10,y+38),"f(x,y) = P(X=x, Y=y)",font=FFM,fill=DARK)
d.text((LX+10,y+60),"Discrete: Σ Σ f(x,y) = 1",font=FFM,fill=DARK)
d.text((LX+10,y+82),"Continuous:",font=FSM,fill=DARK)
d.text((LX+10,y+100),"  ∫∫ f(x,y) dx dy = 1",font=FFM,fill=DARK)
d.text((LX+10,y+122),"The FULL probability table",font=FSM,fill=GRAY)
d.text((LX+10,y+136),"or density surface (X,Y)",font=FSM,fill=GRAY)

MX=LX+BW+PAD
rr(d,MX,y,BW,150,BLUE_L,BLUE,r=8)
d.text((MX+10,y+8),"MARGINAL",font=FS,fill=BLUE)
d.line([(MX,y+32),(MX+BW,y+32)],fill=BLUE,width=1)
d.text((MX+10,y+38),"f_X(x)=Σ_y f(x,y) [discrete]",font=FFM,fill=DARK)
d.text((MX+10,y+60),"f_X(x)=∫ f(x,y) dy [cont.]",font=FFM,fill=DARK)
d.text((MX+10,y+82),"f_Y(y)=Σ_x f(x,y) [discrete]",font=FFM,fill=DARK)
d.text((MX+10,y+104),"f_Y(y)=∫ f(x,y) dx [cont.]",font=FFM,fill=DARK)
d.text((MX+10,y+126),"= distribution of ONE var",font=FSM,fill=GRAY)
d.text((MX+10,y+140),"  ignoring the other",font=FSM,fill=GRAY)

RX2=MX+BW+PAD
rr(d,RX2,y,BW,150,GREEN_L,GREEN,r=8)
d.text((RX2+10,y+8),"CONDITIONAL",font=FS,fill=GREEN)
d.line([(RX2,y+32),(RX2+BW,y+32)],fill=GREEN,width=1)
d.text((RX2+10,y+38),"f(x|y) = f(x,y) / f_Y(y)",font=FFM,fill=DARK)
d.text((RX2+10,y+60),"f(y|x) = f(x,y) / f_X(x)",font=FFM,fill=DARK)
d.text((RX2+10,y+82),"INDEPENDENCE TEST:",font=FSM,fill=GREEN)
d.text((RX2+10,y+98),"f(x,y) = f_X(x) · f_Y(y)",font=FFM,fill=DARK)
d.text((RX2+10,y+120),"If equal → INDEPENDENT",font=FSM,fill=DARK)
d.text((RX2+10,y+136),"If not → DEPENDENT",font=FSM,fill=DARK)
y+=162

# Covariance & Correlation box
rr(d,PAD,y,W-2*PAD,120,BRAND_L,BRAND,r=8)
d.text((PAD+12,y+8),"COVARIANCE & CORRELATION",font=FH,fill=BRAND)
d.text((PAD+12,y+34),"Cov(X,Y) = E(XY) - E(X)·E(Y)",font=FFM,fill=DARK)
d.text((PAD+680,y+34),"E(XY) = Σ Σ x·y·P(X=x,Y=y)  [discrete]",font=FFM,fill=DARK)
d.text((PAD+12,y+58),"r(X,Y) = Cov(X,Y) / [SD(X)·SD(Y)]",font=FFM,fill=DARK)
d.text((PAD+680,y+58),"E(XY) = ∫∫ x·y·f(x,y) dx dy  [continuous]",font=FFM,fill=DARK)
d.text((PAD+12,y+82),"Cov=0 → no LINEAR relation (not necessarily independent!)",font=FSM,fill=GRAY)
d.text((PAD+12,y+100),"IF independent: E(XY)=E(X)·E(Y) → Cov=0 always",font=FSM,fill=GRAY)
y+=132

# Workflow
rr(d,PAD,y,W-2*PAD,34,DARK,None,r=6)
dtxt(d,0,y+8,"EXAM WORKFLOW — Given joint pdf/pmf f(x,y), do this in order:",FS,WHITE,cx=W-2*PAD)
y+=40

steps=[
    "Step 1","Find K (if unknown)","Set ∫∫ f(x,y)dxdy = 1  or  ΣΣ f(x,y) = 1 → solve for K",
    "Step 2","Marginal f_X(x)","Integrate/sum f(x,y) over all y → get distribution of X alone",
    "Step 3","Marginal f_Y(y)","Integrate/sum f(x,y) over all x → get distribution of Y alone",
    "Step 4","Check Independence","Does f(x,y) = f_X(x) · f_Y(y)? Yes → independent. No → dependent.",
    "Step 5","Conditional f(x|y)","= f(x,y) / f_Y(y)  (divide joint by marginal of given variable)",
    "Step 6","Find E(X), E(Y), E(XY)","Use marginals for E(X) and E(Y). Use joint for E(XY).",
    "Step 7","Covariance & r","Cov = E(XY)-E(X)E(Y).  r = Cov/[SD(X)·SD(Y)]",
]
i=0
while i<len(steps):
    bg=GOLD_L if (i//3)%2==0 else GRAY_L
    rr(d,PAD,y,80,36,GOLD if (i//3)%2==0 else GRAY,None,r=6)
    rr(d,PAD+80,y,W-2*PAD-80,36,bg,None,r=0)
    d.text((PAD+10,y+9),steps[i],font=FTG,fill=GOLD if (i//3)%2==0 else GRAY)
    d.text((PAD+92,y+4),steps[i+1],font=FS,fill=DARK)
    d.text((PAD+92,y+22),steps[i+2],font=FSM,fill=GRAY)
    y+=38; d.line([(PAD,y),(W-PAD,y)],fill=(215,215,220),width=1); i+=3

y+=20
img=img.crop((0,0,W,y+30))
img.save(os.path.join(OUT,"mindmap-unit2.png"))
print(f"DONE: mindmap-unit2.png  {W}x{y+30}")
