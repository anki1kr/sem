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

# helper: text with explicit keyword args — avoids positional-arg color bug in newer Pillow
def T(d,xy,text,font,fill):
    d.text(xy,text,font=font,fill=fill)

def rr(d,x,y,w,h,fill,stroke=None,r=8,sw=2):
    d.rounded_rectangle([x,y,x+w,y+h],radius=r,fill=fill,outline=stroke,width=sw if stroke else 0)

img=Image.new("RGB",(W,2400),BG)
d=ImageDraw.Draw(img)

FT=F(34,True); FH=F(20,True); FS=F(17,True)
FSM=F(14); FFM=FM(15); FTG=F(13,True); FSB=F(15,True)

# HEADER
rr(d,0,0,W,95,BRAND_D,r=0)
dtxt(d,PAD,12,"Unit IV · Correlation & Curve Fitting",FT,WHITE)
dtxt(d,PAD,58,"BCD-202-V  |  ~16/75 Marks  |  Numericals only — NO derivations needed",FS,GOLD_L)
y=110

# CORRELATION section
rr(d,PAD,y,W-2*PAD,34,BLUE,None,r=6)
dtxt(d,0,y+8,"CORRELATION — Strength & direction of LINEAR relationship between X and Y",FH,WHITE,cx=W-2*PAD)
y+=40

CW=(W-3*PAD)//2; LX=PAD; RX=PAD+CW+PAD

rr(d,LX,y,CW,230,BLUE_L,BLUE,r=8)
T(d,(LX+12,y+8),"KARL PEARSON's r",FSB,BLUE)
T(d,(LX+12,y+30),"r = Σ(x-x̄)(y-ȳ) / [n·σₓ·σᵧ]",FFM,DARK)
T(d,(LX+12,y+52),"  = Σxy/n - x̄ȳ  /  [σₓ·σᵧ]",FFM,DARK)
T(d,(LX+12,y+74),"Short-cut formula:",FSM,BLUE)
T(d,(LX+12,y+92),"r = [NΣxy - ΣxΣy] /",FFM,DARK)
T(d,(LX+12,y+110),"   √[(NΣx²-(Σx)²)(NΣy²-(Σy)²)]",FFM,DARK)
d.line([(LX+12,y+132),(LX+CW-12,y+132)],fill=BLUE,width=1)
T(d,(LX+12,y+138),"-1 ≤ r ≤ +1  (always!)",FSM,DARK)
T(d,(LX+12,y+156),"r = +1 → perfect positive",FSM,GREEN)
T(d,(LX+12,y+174),"r = -1 → perfect negative",FSM,BRAND)
T(d,(LX+12,y+192),"r =  0 → no linear relation",FSM,GRAY)
T(d,(LX+12,y+210),"USE: continuous, quantitative data",FSM,GRAY)

rr(d,RX,y,CW,230,TEAL_L,TEAL,r=8)
T(d,(RX+12,y+8),"SPEARMAN's RANK CORRELATION ρ",FSB,TEAL)
T(d,(RX+12,y+30),"ρ = 1 - [6·Σd²] / [n(n²-1)]",FFM,DARK)
T(d,(RX+12,y+52),"d = difference in ranks of (x,y)",FSM,GRAY)
T(d,(RX+12,y+70),"Σd² = sum of squared rank differences",FSM,GRAY)
d.line([(RX+12,y+90),(RX+CW-12,y+90)],fill=TEAL,width=1)
T(d,(RX+12,y+96),"STEPS:",FSB,TEAL)
T(d,(RX+12,y+114),"1. Rank X values (1=smallest) → Rₓ",FFM,DARK)
T(d,(RX+12,y+134),"2. Rank Y values similarly    → Rᵧ",FFM,DARK)
T(d,(RX+12,y+154),"3. d = Rₓ - Rᵧ  for each pair",FFM,DARK)
T(d,(RX+12,y+174),"4. Σd² → apply formula",FFM,DARK)
T(d,(RX+12,y+194),"USE: ordinal/ranked data, non-normal",FSM,GRAY)
T(d,(RX+12,y+212),"Tied ranks → average the tied ranks",FSM,GRAY)
y+=242

# Pearson vs Spearman comparison
rr(d,PAD,y,W-2*PAD,34,DARK,None,r=6)
dtxt(d,0,y+8,"PEARSON vs SPEARMAN — when question says 'rank correlation' use Spearman",FS,WHITE,cx=W-2*PAD)
y+=40

headers=["Parameter","Karl Pearson  r","Spearman  ρ"]
rows_data=[
    ("Data type","Quantitative continuous","Ordinal / ranked data"),
    ("Assumption","Linear relation, normal dist.","No distributional assumption"),
    ("Outliers","Sensitive to outliers","Not affected by outliers"),
    ("Formula","NΣxy-ΣxΣy / √[…]","1 - 6Σd²/n(n²-1)"),
    ("Range","−1 to +1","−1 to +1"),
    ("Trigger in Q","correlation coefficient","rank correlation / marks → rank"),
]
col_ws=[220, (W-2*PAD-220-40)//2, (W-2*PAD-220-40)//2]
col_xs=[PAD, PAD+col_ws[0]+10, PAD+col_ws[0]+10+col_ws[1]+10]
rh=30
# header row
rr(d,PAD,y,W-2*PAD,rh,BLUE,None,r=4)
for ci,(cx,cw,hd) in enumerate(zip(col_xs,col_ws,headers)):
    T(d,(cx+6,y+7),hd,FSB,WHITE)
y+=rh
for ri,row in enumerate(rows_data):
    bg=BLUE_L if ri%2==0 else WHITE
    rr(d,PAD,y,W-2*PAD,rh,bg,None,r=0)
    for ci,(cx,cw,cell) in enumerate(zip(col_xs,col_ws,row)):
        col=BLUE if ci==1 else(TEAL if ci==2 else DARK)
        T(d,(cx+6,y+7),cell,FSM,col)
    y+=rh
    d.line([(PAD,y),(W-PAD,y)],fill=(210,215,225),width=1)
y+=16

# REGRESSION
rr(d,PAD,y,W-2*PAD,34,GREEN,None,r=6)
dtxt(d,0,y+8,"REGRESSION — Predict Y from X (or X from Y) using the best-fit line",FH,WHITE,cx=W-2*PAD)
y+=40

rr(d,LX,y,CW,190,GREEN_L,GREEN,r=8)
T(d,(LX+12,y+8),"LINE OF REGRESSION — Y on X",FSB,GREEN)
T(d,(LX+12,y+30),"Y - ȳ = bᵧₓ · (X - x̄)",FFM,DARK)
T(d,(LX+12,y+52),"bᵧₓ = r · σᵧ/σₓ",FFM,DARK)
T(d,(LX+12,y+74),"bᵧₓ = [NΣxy-ΣxΣy]/[NΣx²-(Σx)²]",FFM,DARK)
d.line([(LX+12,y+96),(LX+CW-12,y+96)],fill=GREEN,width=1)
T(d,(LX+12,y+102),"USE: given X, PREDICT Y",FSM,GREEN)
T(d,(LX+12,y+118),"bᵧₓ = regression coeff of Y on X",FSM,GRAY)
T(d,(LX+12,y+136),"Both lines PASS through (x̄, ȳ)",FSM,GRAY)
T(d,(LX+12,y+154),"r² = bᵧₓ × bₓᵧ  (coefficient of determination)",FSM,GRAY)
T(d,(LX+12,y+172),"r = √(bᵧₓ × bₓᵧ)  sign = sign of b",FSM,GRAY)

rr(d,RX,y,CW,190,GOLD_L,GOLD,r=8)
T(d,(RX+12,y+8),"LINE OF REGRESSION — X on Y",FSB,GOLD)
T(d,(RX+12,y+30),"X - x̄ = bₓᵧ · (Y - ȳ)",FFM,DARK)
T(d,(RX+12,y+52),"bₓᵧ = r · σₓ/σᵧ",FFM,DARK)
T(d,(RX+12,y+74),"bₓᵧ = [NΣxy-ΣxΣy]/[NΣy²-(Σy)²]",FFM,DARK)
d.line([(RX+12,y+96),(RX+CW-12,y+96)],fill=GOLD,width=1)
T(d,(RX+12,y+102),"USE: given Y, PREDICT X",FSM,GOLD)
T(d,(RX+12,y+118),"2 regression lines (not same line!)",FSM,GRAY)
T(d,(RX+12,y+136),"Angle between them → r (closer=higher r)",FSM,GRAY)
T(d,(RX+12,y+154),"If r=1: both lines coincide",FSM,GRAY)
T(d,(RX+12,y+172),"If r=0: lines ⊥ to each other",FSM,GRAY)
y+=202

# CURVE FITTING
rr(d,PAD,y,W-2*PAD,34,PURPLE,None,r=6)
dtxt(d,0,y+8,"CURVE FITTING by Least Squares — Numerical problems ONLY (no derivation)",FH,WHITE,cx=W-2*PAD)
y+=40

rr(d,PAD,y,W-2*PAD,34,GRAY_L,None,r=4)
T(d,(PAD+12,y+8),"Principle of Least Squares: choose a,b,c so that Σ(observed y - fitted ŷ)² is MINIMISED",FFM,DARK)
y+=44

BW=(W-5*PAD)//4
for ci,(name,eq,normals,note) in enumerate([
    ("Straight Line","y = a + b·x",["Σy = na + bΣx","Σxy = aΣx + bΣx²"],"Linear trend"),
    ("Parabola","y = a + bx + cx²",["Σy = na+bΣx+cΣx²","Σxy = aΣx+bΣx²+cΣx³","Σx²y=aΣx²+bΣx³+cΣx⁴"],"Curved/quadratic trend"),
    ("Power Curve","y = ax^b",["log y = log a + b·log x","Y = A + bX","(linearise by log)"],"log-log transform first"),
    ("Exponential","y = ae^(bx)",["log y = log a + bx·log e","Y = A + Bx","(linearise by log)"],"log y vs x is linear"),
]):
    bx=PAD+ci*(BW+PAD)
    rr(d,bx,y,BW,200,PURPLE_L,PURPLE,r=8)
    T(d,(bx+8,y+8),name,FSB,PURPLE)
    T(d,(bx+8,y+28),eq,FFM,DARK)
    d.line([(bx+8,y+48),(bx+BW-8,y+48)],fill=PURPLE,width=1)
    T(d,(bx+8,y+54),"Normal eqns:",FSM,PURPLE)
    ny=y+70
    for nl in normals:
        T(d,(bx+8,ny),nl,FM(13),DARK); ny+=20
    T(d,(bx+8,y+178),note,FSM,GRAY)
y+=212

# Workflow box
rr(d,PAD,y,W-2*PAD,34,BRAND,None,r=6)
dtxt(d,0,y+8,"EXAM WORKFLOW — Correlation & Regression typical 15M question",FS,WHITE,cx=W-2*PAD)
y+=40

steps=[
    ("1","Build table","Columns: x, y, x², y², xy  →  compute each row  →  sum all columns"),
    ("2","Find means","x̄ = Σx/n   ȳ = Σy/n"),
    ("3","Find r (Pearson)","r = [NΣxy-ΣxΣy] / √[(NΣx²-(Σx)²)·(NΣy²-(Σy)²)]"),
    ("4","Find bᵧₓ","bᵧₓ = [NΣxy-ΣxΣy] / [NΣx²-(Σx)²]"),
    ("5","Find bₓᵧ","bₓᵧ = [NΣxy-ΣxΣy] / [NΣy²-(Σy)²]"),
    ("6","Regression lines","Y-ȳ = bᵧₓ(X-x̄)  and  X-x̄ = bₓᵧ(Y-ȳ)"),
    ("7","Verify r","Check: r = √(bᵧₓ·bₓᵧ)  (sign = sign of b's)"),
]
for sn,st,sd in steps:
    bg=BRAND_L if int(sn)%2==1 else GRAY_L
    rr(d,PAD,y,60,34,BRAND,None,r=4)
    rr(d,PAD+60,y,W-2*PAD-60,34,bg,None,r=0)
    T(d,(PAD+10,y+9),sn,FSB,WHITE)
    T(d,(PAD+70,y+4),st,FS,DARK)
    T(d,(PAD+70,y+21),sd,FSM,GRAY)
    y+=36; d.line([(PAD,y),(W-PAD,y)],fill=(210,215,220),width=1)

y+=20
img=img.crop((0,0,W,y+30))
img.save(os.path.join(OUT,"mindmap-unit4.png"))
print(f"DONE: mindmap-unit4.png  {W}x{y+30}")
