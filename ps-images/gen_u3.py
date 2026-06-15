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
ORANGE=(170,70,0); ORANGE_L=(255,240,218)
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

def T(d,x,y,t,f,c):
    d.text((x,y),t,font=f,fill=c)

def rr(d,x,y,w,h,fill,stroke=None,r=8,sw=2):
    d.rounded_rectangle([x,y,x+w,y+h],radius=r,fill=fill,outline=stroke,width=sw if stroke else 0)

img=Image.new("RGB",(W,2400),BG)
d=ImageDraw.Draw(img)

FT=F(34,True); FH=F(20,True); FS=F(17,True)
FB=F(16); FSM=F(14); FFM=FM(15); FTG=F(13,True); FSB=F(15,True)

# HEADER
rr(d,0,0,W,95,BRAND_D,r=0)
dtxt(d,PAD,12,"Unit III · Descriptive Statistics",FT,WHITE)
dtxt(d,PAD,58,"BCD-202-V  |  ~16/75 Marks  |  Data Types + Central Tendency + Dispersion + Shape",FS,GOLD_L)
y=110

# DATA TYPES
rr(d,PAD,y,W-2*PAD,34,BLUE,None,r=6)
dtxt(d,0,y+8,"DATA TYPES — Know the difference (Part-A question every year)",FH,WHITE,cx=W-2*PAD)
y+=40

CW=(W-3*PAD)//2; LX=PAD; RX=PAD+CW+PAD

rr(d,LX,y,CW,120,BLUE_L,BLUE,r=8)
T(d,LX+12,y+8,"PRIMARY DATA",FSB,BLUE)
T(d,LX+12,y+30,"Collected DIRECTLY for current purpose",FFM,DARK)
T(d,LX+12,y+50,"• Surveys / questionnaires",FSM,DARK)
T(d,LX+12,y+68,"• Interviews / observations",FSM,DARK)
T(d,LX+12,y+86,"• Experiments",FSM,DARK)
T(d,LX+12,y+104,"Original, first-hand, more reliable",FSM,GRAY)

rr(d,RX,y,CW,120,GREEN_L,GREEN,r=8)
T(d,RX+12,y+8,"SECONDARY DATA",FSB,GREEN)
T(d,RX+12,y+30,"Collected by SOMEONE ELSE earlier",FFM,DARK)
T(d,RX+12,y+50,"• Published reports / census",FSM,DARK)
T(d,RX+12,y+68,"• Govt records / journals",FSM,DARK)
T(d,RX+12,y+86,"• Newspapers / internet",FSM,DARK)
T(d,RX+12,y+104,"Already processed, secondary use",FSM,GRAY)
y+=132

# CENTRAL TENDENCY
rr(d,PAD,y,W-2*PAD,34,TEAL,None,r=6)
dtxt(d,0,y+8,"CENTRAL TENDENCY — Single value representing the dataset",FH,WHITE,cx=W-2*PAD)
y+=40

TW=(W-5*PAD)//3
TX1=PAD; TX2=PAD+TW+PAD; TX3=PAD+2*(TW+PAD)

rr(d,TX1,y,TW,185,GOLD_L,GOLD,r=8)
T(d,TX1+10,y+8,"MEAN (AM)",FSB,GOLD)
d.line([(TX1,y+30),(TX1+TW,y+30)],fill=GOLD,width=1)
T(d,TX1+10,y+36,"x̄ = Σx / n",FFM,DARK)
T(d,TX1+10,y+58,"Weighted: x̄=Σwx/Σw",FFM,DARK)
T(d,TX1+10,y+78,"Freq: x̄=Σfx/Σf",FFM,DARK)
T(d,TX1+10,y+100,"WHEN TO USE:",FSM,GOLD)
T(d,TX1+10,y+116,"Symmetric data,",FSM,DARK)
T(d,TX1+10,y+132,"no outliers,",FSM,DARK)
T(d,TX1+10,y+148,"interval/ratio scale",FSM,DARK)
T(d,TX1+10,y+166,"Most used in exams",FSM,GRAY)

rr(d,TX2,y,TW,185,BLUE_L,BLUE,r=8)
T(d,TX2+10,y+8,"MEDIAN",FSB,BLUE)
d.line([(TX2,y+30),(TX2+TW,y+30)],fill=BLUE,width=1)
T(d,TX2+10,y+36,"Odd n: M=(n+1)/2 th val",FFM,DARK)
T(d,TX2+10,y+58,"Even n: avg of n/2 &",FFM,DARK)
T(d,TX2+10,y+76,"  (n/2+1) th values",FFM,DARK)
T(d,TX2+10,y+96,"WHEN TO USE:",FSM,BLUE)
T(d,TX2+10,y+112,"Skewed data,",FSM,DARK)
T(d,TX2+10,y+128,"outliers present,",FSM,DARK)
T(d,TX2+10,y+144,"ordinal scale",FSM,DARK)
T(d,TX2+10,y+160,"Not affected by extremes",FSM,GRAY)

rr(d,TX3,y,TW,185,GREEN_L,GREEN,r=8)
T(d,TX3+10,y+8,"MODE",FSB,GREEN)
d.line([(TX3,y+30),(TX3+TW,y+30)],fill=GREEN,width=1)
T(d,TX3+10,y+36,"Most FREQUENT value",FFM,DARK)
T(d,TX3+10,y+58,"Can be: no mode /",FFM,DARK)
T(d,TX3+10,y+76,"unimodal / bimodal",FFM,DARK)
T(d,TX3+10,y+96,"WHEN TO USE:",FSM,GREEN)
T(d,TX3+10,y+112,"Categorical data,",FSM,DARK)
T(d,TX3+10,y+128,"nominal scale,",FSM,DARK)
T(d,TX3+10,y+144,"find most popular",FSM,DARK)
T(d,TX3+10,y+160,"Only measure for nominal",FSM,GRAY)
y+=197

# Relation box
rr(d,PAD,y,W-2*PAD,36,GRAY_L,GRAY,r=6)
T(d,PAD+12,y+8,"Relation (Pearson's Empirical):  Mean - Mode = 3(Mean - Median)     |     Symmetric: Mean = Median = Mode",FFM,DARK)
y+=48

# DISPERSION
rr(d,PAD,y,W-2*PAD,34,ORANGE,None,r=6)
dtxt(d,0,y+8,"DISPERSION — How spread out is the data?",FH,WHITE,cx=W-2*PAD)
y+=40

rr(d,LX,y,CW,150,ORANGE_L,ORANGE,r=8)
T(d,LX+12,y+8,"VARIANCE & STANDARD DEVIATION",FSB,ORANGE)
T(d,LX+12,y+30,"σ² = Σ(x - x̄)² / n",FFM,DARK)
T(d,LX+12,y+52,"σ² = Σx²/n - (x̄)²  ← easier to compute",FFM,DARK)
T(d,LX+12,y+74,"σ = √σ²  (Standard Deviation)",FFM,DARK)
T(d,LX+12,y+96,"Freq data: σ²=Σf(x-x̄)²/Σf = Σfx²/Σf-(x̄)²",FFM,DARK)
T(d,LX+12,y+118,"SD keeps same units as data. Var = SD².",FSM,GRAY)
T(d,LX+12,y+136,"Larger σ = more spread. σ=0 means all same.",FSM,GRAY)

rr(d,RX,y,CW,150,GRAY_L,GRAY,r=8)
T(d,RX+12,y+8,"MOMENTS (raw & central)",FSB,GRAY)
T(d,RX+12,y+30,"Raw μ'ᵣ = Σ xʳ·f(x)/N  (about origin)",FFM,DARK)
T(d,RX+12,y+52,"Central μᵣ = Σ(x-x̄)ʳ·f(x)/N (about mean)",FFM,DARK)
T(d,RX+12,y+74,"μ₁ = 0  (always!)",FFM,DARK)
T(d,RX+12,y+96,"μ₂ = Variance = σ²",FFM,DARK)
T(d,RX+12,y+118,"μ₃ → skewness   μ₄ → kurtosis",FFM,DARK)
T(d,RX+12,y+136,"μ'₁ = x̄ (mean)   μ'₂ = σ²+(x̄)²",FSM,GRAY)
y+=162

# SKEWNESS & KURTOSIS
rr(d,PAD,y,W-2*PAD,34,BRAND,None,r=6)
dtxt(d,0,y+8,"SHAPE — Skewness & Kurtosis (β₁ β₂ are the numbers examiners want)",FH,WHITE,cx=W-2*PAD)
y+=40

rr(d,LX,y,CW,200,BRAND_L,BRAND,r=8)
T(d,LX+12,y+8,"SKEWNESS — β₁",FSB,BRAND)
T(d,LX+12,y+30,"β₁ = μ₃² / μ₂³",FFM,DARK)
T(d,LX+12,y+52,"γ₁ = μ₃ / μ₂^(3/2)  (Pearson's γ)",FFM,DARK)
d.line([(LX+12,y+72),(LX+CW-12,y+72)],fill=BRAND,width=1)
T(d,LX+12,y+78,"β₁ = 0  → SYMMETRIC (normal)",FFM,GREEN)
T(d,LX+12,y+100,"β₁ > 0  → POSITIVELY SKEWED",FFM,DARK)
T(d,LX+12,y+118,"         (tail right, Mode<Med<Mean)",FSM,GRAY)
T(d,LX+12,y+136,"β₁ < 0  → NEGATIVELY SKEWED",FFM,DARK)
T(d,LX+12,y+154,"         (tail left, Mean<Med<Mode)",FSM,GRAY)
T(d,LX+12,y+174,"Measures ASYMMETRY of distribution",FSM,GRAY)

rr(d,RX,y,CW,200,GOLD_L,GOLD,r=8)
T(d,RX+12,y+8,"KURTOSIS — β₂",FSB,GOLD)
T(d,RX+12,y+30,"β₂ = μ₄ / μ₂²",FFM,DARK)
T(d,RX+12,y+52,"(excess kurtosis = β₂ - 3)",FFM,GRAY)
d.line([(RX+12,y+72),(RX+CW-12,y+72)],fill=GOLD,width=1)
T(d,RX+12,y+78,"β₂ = 3  → MESOKURTIC (Normal dist.)",FFM,DARK)
T(d,RX+12,y+100,"β₂ > 3  → LEPTOKURTIC",FFM,DARK)
T(d,RX+12,y+118,"         Tall & thin, heavy tails",FSM,GRAY)
T(d,RX+12,y+136,"β₂ < 3  → PLATYKURTIC",FFM,DARK)
T(d,RX+12,y+154,"         Flat & wide, light tails",FSM,GRAY)
T(d,RX+12,y+174,"Measures PEAKEDNESS of distribution",FSM,GRAY)
y+=212

# Frequency Distribution table
rr(d,PAD,y,W-2*PAD,34,DARK,None,r=6)
dtxt(d,0,y+8,"FREQUENCY DISTRIBUTION — How to compute stats from table",FS,WHITE,cx=W-2*PAD)
y+=40

rr(d,PAD,y,W-2*PAD,130,GRAY_L,None,r=6)
T(d,PAD+12,y+8,"Given: class intervals with frequencies f",FS,DARK)
T(d,PAD+12,y+30,"Step 1: Find midpoint x of each class:  x = (lower + upper) / 2",FFM,DARK)
T(d,PAD+12,y+52,"Step 2: Mean x̄ = Σfx / Σf  (= Σfx / N where N = total frequency)",FFM,DARK)
T(d,PAD+12,y+74,"Step 3: Variance σ² = Σf(x-x̄)²/N  =  Σfx²/N - (x̄)²",FFM,DARK)
T(d,PAD+12,y+96,"Step 4: μᵣ = Σf(x-x̄)ʳ / N  for central moments (r=2,3,4)",FFM,DARK)
T(d,PAD+12,y+116,"Step 5: β₁=μ₃²/μ₂³  β₂=μ₄/μ₂²  → comment on shape",FFM,DARK)
y+=142

y+=10
img=img.crop((0,0,W,y+30))
img.save(os.path.join(OUT,"mindmap-unit3.png"))
print(f"DONE: mindmap-unit3.png  {W}x{y+30}")
