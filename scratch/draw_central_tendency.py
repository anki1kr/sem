import os
import math
from PIL import Image, ImageDraw, ImageFont

# Set up paths
font_dir = r"C:\Windows\Fonts"
output_dir = r"C:\Users\ankit\OneDrive\Desktop\sem\rds-images"
output_path = os.path.join(output_dir, "central-tendency-dispersion.png")

os.makedirs(output_dir, exist_ok=True)

# Helper function to load Windows fonts
def get_font(font_name, size):
    path = os.path.join(font_dir, font_name)
    if os.path.exists(path):
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            return ImageFont.load_default()
    # Try generic names
    for alt_name in [font_name, font_name.lower(), font_name.upper()]:
        alt_path = os.path.join(font_dir, alt_name)
        if os.path.exists(alt_path):
            try:
                return ImageFont.truetype(alt_path, size)
            except Exception:
                pass
    return ImageFont.load_default()

# Initialize Canvas
# 1600x900 textbook-style background (light cream)
bg_color = (253, 251, 247)  # #FDFBF7
img = Image.new("RGB", (1600, 900), bg_color)
draw = ImageDraw.Draw(img)

# Define Colors
forest_green = (42, 90, 67)        # #2A5A43 (Central Tendency accent)
forest_green_light = (234, 244, 238)  # #EAF4EE (Central Tendency fill)
crimson = (180, 30, 45)            # #B41E2D (Dispersion accent)
crimson_light = (253, 242, 242)    # #FDF2F2 (Dispersion fill)
charcoal = (51, 51, 51)            # #333333 (General text)
gray_border = (182, 194, 201)      # #B6C2C9
axis_gray = (126, 141, 153)        # #7E8D99
shadow_color = (235, 231, 220)     # #EBE7DC

# -------------------------------------------------------------
# DRAW TITLE & HEADER
# -------------------------------------------------------------
title_font = get_font("segoeuib.ttf", 40)
subtitle_font = get_font("segoeuii.ttf", 18)

title_text = "Measures of Central Tendency & Dispersion"
draw.text((800, 40), title_text, fill=charcoal, font=title_font, anchor="mm")

subtitle_text = "Core Statistical Summaries of Data Location and Spread"
draw.text((800, 80), subtitle_text, fill=(100, 100, 100), font=subtitle_font, anchor="mm")

draw.line([(600, 100), (1000, 100)], fill=forest_green, width=3)

# -------------------------------------------------------------
# BOX DRAWING HELPER
# -------------------------------------------------------------
def draw_panel_skeleton(x1, y1, x2, y2, title, accent_color, fill_color):
    # Draw soft flat shadow
    draw.rounded_rectangle([x1 + 6, y1 + 6, x2 + 6, y2 + 6], radius=12, fill=shadow_color)
    # Draw card body
    draw.rounded_rectangle([x1, y1, x2, y2], radius=12, fill=(255, 255, 255), outline=gray_border, width=2)
    # Header bar
    draw.rounded_rectangle([x1, y1, x2, y1 + 45], radius=12, fill=fill_color)
    # Flatten bottom of header
    draw.rectangle([x1, y1 + 33, x2, y1 + 45], fill=fill_color)
    draw.line([(x1, y1 + 45), (x2, y1 + 45)], fill=accent_color, width=2)
    
    # Title text
    panel_title_font = get_font("segoeuib.ttf", 20)
    draw.text((x1 + 20, y1 + 22), title, fill=accent_color, font=panel_title_font, anchor="lm")

# Grid coordinates
col_w = 440
col_h = 345
y_row1 = 135
y_row2 = 510

col1_x = 60
col2_x = 580
col3_x = 1100

# =============================================================
# ROW 1: CENTRAL TENDENCY (Forest Green Accent)
# =============================================================

# -------------------------------------------------------------
# 1. MEAN
# -------------------------------------------------------------
x1, y1 = col1_x, y_row1
x2, y2 = x1 + col_w, y1 + col_h
draw_panel_skeleton(x1, y1, x2, y2, "MEAN (Arithmetic Average)", forest_green, forest_green_light)

# Formula: x-bar = sum x / n
fx = x1 + 30
fy = y1 + 75
draw.text((fx, fy + 5), "Formula:", fill=charcoal, font=get_font("segoeuib.ttf", 16))

f_start_x = fx + 75
f_start_y = fy
# x
draw.text((f_start_x, f_start_y + 3), "x", fill=forest_green, font=get_font("segoeui.ttf", 22))
# bar above x
draw.line([(f_start_x - 2, f_start_y + 2), (f_start_x + 12, f_start_y + 2)], fill=forest_green, width=2)
# =
draw.text((f_start_x + 22, f_start_y + 2), "=", fill=charcoal, font=get_font("segoeui.ttf", 20))
# Numerator sum x
draw.text((f_start_x + 52, f_start_y - 12), "Σ x", fill=forest_green, font=get_font("segoeui.ttf", 20))
# Fraction line
draw.line([(f_start_x + 48, f_start_y + 16), (f_start_x + 82, f_start_y + 16)], fill=charcoal, width=2)
# Denominator n
draw.text((f_start_x + 58, f_start_y + 20), "n", fill=forest_green, font=get_font("segoeui.ttf", 18))

# Takeaway text
draw.text((x2 - 170, y1 + 75), "• Pulled by outliers", fill=crimson, font=get_font("segoeuib.ttf", 14))
draw.text((x2 - 170, y1 + 95), "• Sensitive to extreme\n  values", fill=charcoal, font=get_font("segoeui.ttf", 12))

# Visual: Seesaw
beam_y = y1 + 250
draw.line([(x1 + 40, beam_y), (x2 - 40, beam_y)], fill=axis_gray, width=4)

# Left weight stack (normal values)
wx1 = x1 + 100
box_sz = 24
draw.rounded_rectangle([wx1 - box_sz//2, beam_y - box_sz, wx1 + box_sz//2, beam_y], radius=3, fill=forest_green_light, outline=forest_green, width=2)
draw.rounded_rectangle([wx1 - box_sz//2, beam_y - 2*box_sz - 2, wx1 + box_sz//2, beam_y - box_sz - 2], radius=3, fill=forest_green_light, outline=forest_green, width=2)

# Middle weight
wx2 = x1 + 170
draw.rounded_rectangle([wx2 - box_sz//2, beam_y - box_sz, wx2 + box_sz//2, beam_y], radius=3, fill=forest_green_light, outline=forest_green, width=2)

# Right Outlier weight (crimson)
wx_out = x2 - 80
draw.rounded_rectangle([wx_out - box_sz//2, beam_y - box_sz, wx_out + box_sz//2, beam_y], radius=3, fill=crimson_light, outline=crimson, width=2)

# Labels
draw.text((wx1, beam_y - 2*box_sz - 14), "Data Stack", fill=forest_green, font=get_font("segoeuib.ttf", 11), anchor="mm")
draw.text((wx_out, beam_y - box_sz - 10), "Outlier", fill=crimson, font=get_font("segoeuib.ttf", 11), anchor="mm")

# Actual Mean Fulcrum (shifted right)
fulc_x = x1 + 235
draw.polygon([(fulc_x, beam_y), (fulc_x - 12, beam_y + 20), (fulc_x + 12, beam_y + 20)], fill=charcoal)
draw.text((fulc_x, beam_y + 32), "Mean (Balance Point)", fill=forest_green, font=get_font("segoeuib.ttf", 12), anchor="mm")

# Dotted line at original center (unbiased center)
orig_x = x1 + 140
for dy in range(0, 30, 6):
    draw.line([(orig_x, beam_y - 30 + dy), (orig_x, beam_y - 30 + dy + 3)], fill=axis_gray, width=2)

# Shift arrow
draw.line([(orig_x, beam_y - 35), (fulc_x, beam_y - 35)], fill=crimson, width=2)
draw.polygon([(fulc_x, beam_y - 35), (fulc_x - 6, beam_y - 39), (fulc_x - 6, beam_y - 31)], fill=crimson)
draw.text(((orig_x + fulc_x)//2, beam_y - 48), "Pulled Right", fill=crimson, font=get_font("segoeuii.ttf", 10), anchor="mm")


# -------------------------------------------------------------
# 2. MEDIAN
# -------------------------------------------------------------
x1, y1 = col2_x, y_row1
x2, y2 = x1 + col_w, y1 + col_h
draw_panel_skeleton(x1, y1, x2, y2, "MEDIAN (Middle Value)", forest_green, forest_green_light)

# Formula
fx = x1 + 30
fy = y1 + 75
draw.text((fx, fy + 5), "Formula:", fill=charcoal, font=get_font("segoeuib.ttf", 16))

f_start_x = fx + 75
f_start_y = fy
# Position =
draw.text((f_start_x, f_start_y + 3), "Position =", fill=forest_green, font=get_font("segoeui.ttf", 18))
# Numerator n + 1
draw.text((f_start_x + 92, f_start_y - 12), "n + 1", fill=forest_green, font=get_font("segoeui.ttf", 18))
# Fraction line
draw.line([(f_start_x + 88, f_start_y + 14), (f_start_x + 132, f_start_y + 14)], fill=charcoal, width=2)
# Denominator 2
draw.text((f_start_x + 105, f_start_y + 18), "2", fill=forest_green, font=get_font("segoeui.ttf", 18))

# Takeaway text
draw.text((x2 - 180, y1 + 75), "• Robust to outliers", fill=forest_green, font=get_font("segoeuib.ttf", 14))
draw.text((x2 - 180, y1 + 95), "• Unaffected by extreme\n  outlier values", fill=charcoal, font=get_font("segoeui.ttf", 12))

# Visual: Cells row
cell_w = 42
cell_h = 42
spacing = 6
vals = ["12", "15", "18", "22", "30", "35", "99"]
start_x = x1 + 220 - (7 * cell_w + 6 * spacing) // 2
cell_y = y1 + 220

draw.text((x1 + 220, cell_y - 25), "Sorted Dataset (Ascending)", fill=(120, 120, 120), font=get_font("segoeuii.ttf", 12), anchor="mm")

for i, val in enumerate(vals):
    cx1 = start_x + i * (cell_w + spacing)
    cy1 = cell_y
    cx2 = cx1 + cell_w
    cy2 = cy1 + cell_h
    
    if i == 3: # Median
        draw.rounded_rectangle([cx1, cy1, cx2, cy2], radius=5, fill=forest_green_light, outline=forest_green, width=3)
        draw.text((cx1 + cell_w//2, cy1 + cell_h//2), val, fill=forest_green, font=get_font("segoeuib.ttf", 18), anchor="mm")
        
        # Pointing arrow
        draw.line([(cx1 + cell_w//2, cy1 + cell_h + 25), (cx1 + cell_w//2, cy1 + cell_h + 5)], fill=forest_green, width=2)
        draw.polygon([(cx1 + cell_w//2, cy1 + cell_h + 3), (cx1 + cell_w//2 - 5, cy1 + cell_h + 9), (cx1 + cell_w//2 + 5, cy1 + cell_h + 9)], fill=forest_green)
        draw.text((cx1 + cell_w//2, cy1 + cell_h + 38), "Median = 22", fill=forest_green, font=get_font("segoeuib.ttf", 13), anchor="mm")
    else:
        # Normal cell
        draw.rounded_rectangle([cx1, cy1, cx2, cy2], radius=5, fill=(250, 250, 250), outline=gray_border, width=2)
        if i == 6: # Outlier highlighted
            draw.text((cx1 + cell_w//2, cy1 + cell_h//2), val, fill=crimson, font=get_font("segoeuib.ttf", 16), anchor="mm")
            draw.text((cx1 + cell_w//2, cy1 - 42), "Outlier", fill=crimson, font=get_font("segoeuib.ttf", 10), anchor="mm")
        else:
            draw.text((cx1 + cell_w//2, cy1 + cell_h//2), val, fill=charcoal, font=get_font("segoeui.ttf", 16), anchor="mm")


# -------------------------------------------------------------
# 3. MODE
# -------------------------------------------------------------
x1, y1 = col3_x, y_row1
x2, y2 = x1 + col_w, y1 + col_h
draw_panel_skeleton(x1, y1, x2, y2, "MODE (Most Frequent)", forest_green, forest_green_light)

# Takeaway text
draw.text((x1 + 30, y1 + 75), "• Most frequent value", fill=forest_green, font=get_font("segoeuib.ttf", 15))
draw.text((x1 + 30, y1 + 98), "• Peak of distribution\n• Best for categorical data", fill=charcoal, font=get_font("segoeui.ttf", 13))

# Chart visual
chart_base_y = y1 + 285
chart_start_x = x1 + 120
bar_w = 36
bar_spacing = 8
heights = [30, 60, 115, 50, 35]
labels = ["A", "B", "C", "D", "E"]

# Axes
draw.line([(x1 + 80, chart_base_y), (x2 - 80, chart_base_y)], fill=axis_gray, width=2)
draw.line([(x1 + 80, y1 + 150), (x1 + 80, chart_base_y)], fill=axis_gray, width=2)

for i in range(5):
    bx1 = chart_start_x + i * (bar_w + bar_spacing)
    by1 = chart_base_y - heights[i]
    bx2 = bx1 + bar_w
    by2 = chart_base_y
    
    if i == 2: # Highlight tallest
        draw.rectangle([bx1, by1, bx2, by2], fill=forest_green_light, outline=forest_green, width=3)
        draw.text((bx1 + bar_w//2, by1 - 15), "Mode", fill=forest_green, font=get_font("segoeuib.ttf", 12), anchor="mm")
        draw.polygon([(bx1 + bar_w//2, by1 - 2), (bx1 + bar_w//2 - 4, by1 - 7), (bx1 + bar_w//2 + 4, by1 - 7)], fill=forest_green)
    else:
        draw.rectangle([bx1, by1, bx2, by2], fill=(240, 240, 240), outline=gray_border, width=2)
        
    draw.text((bx1 + bar_w//2, chart_base_y + 12), labels[i], fill=charcoal, font=get_font("segoeui.ttf", 11), anchor="mm")

draw.text((x1 + 65, y1 + 165), "Freq", fill=(120, 120, 120), font=get_font("segoeuii.ttf", 10), anchor="mm")


# =============================================================
# ROW 2: DISPERSION (Crimson Accent)
# =============================================================

# -------------------------------------------------------------
# 4. RANGE
# -------------------------------------------------------------
x1, y1 = col1_x, y_row2
x2, y2 = x1 + col_w, y1 + col_h
draw_panel_skeleton(x1, y1, x2, y2, "RANGE (Simplest Spread)", crimson, crimson_light)

# Formula
fx = x1 + 30
fy = y1 + 75
draw.text((fx, fy + 5), "Formula:", fill=charcoal, font=get_font("segoeuib.ttf", 16))
draw.text((fx + 75, fy + 5), "Range = Max - Min", fill=crimson, font=get_font("segoeuib.ttf", 16))

# Takeaway text
draw.text((x2 - 170, y1 + 75), "• Sensitive to outliers", fill=crimson, font=get_font("segoeuib.ttf", 14))
draw.text((x2 - 170, y1 + 95), "• Ignores intermediate\n  data distribution", fill=charcoal, font=get_font("segoeui.ttf", 12))

# Visual: Number Line
line_y = y1 + 230
start_pt_x = x1 + 50
end_pt_x = x2 - 50

draw.line([(start_pt_x - 10, line_y), (end_pt_x + 10, line_y)], fill=axis_gray, width=2)
draw.line([(start_pt_x, line_y - 5), (start_pt_x, line_y + 5)], fill=axis_gray, width=2)
draw.line([(end_pt_x, line_y - 5), (end_pt_x, line_y + 5)], fill=axis_gray, width=2)

draw.text((start_pt_x, line_y + 14), "0", fill=(120, 120, 120), font=get_font("segoeui.ttf", 11), anchor="mm")
draw.text((end_pt_x, line_y + 14), "100", fill=(120, 120, 120), font=get_font("segoeui.ttf", 11), anchor="mm")

# Data coordinates
min_x = start_pt_x + 68  # Value 20
max_x = start_pt_x + 306 # Value 90
other_xs = [start_pt_x + 115, start_pt_x + 170, start_pt_x + 220, start_pt_x + 255]

for ox in other_xs:
    draw.ellipse([ox - 5, line_y - 5, ox + 5, line_y + 5], fill=(210, 210, 210), outline=(150, 150, 150), width=1)
    
draw.ellipse([min_x - 8, line_y - 8, min_x + 8, line_y + 8], fill=crimson_light, outline=crimson, width=3)
draw.text((min_x, line_y - 18), "Min (20)", fill=crimson, font=get_font("segoeuib.ttf", 11), anchor="mm")

draw.ellipse([max_x - 8, line_y - 8, max_x + 8, line_y + 8], fill=crimson_light, outline=crimson, width=3)
draw.text((max_x, line_y - 18), "Max (90)", fill=crimson, font=get_font("segoeuib.ttf", 11), anchor="mm")

# Dimension bracket
bracket_y = line_y + 35
draw.line([(min_x, bracket_y), (max_x, bracket_y)], fill=crimson, width=2)
draw.line([(min_x, bracket_y - 6), (min_x, bracket_y + 6)], fill=crimson, width=2)
draw.line([(max_x, bracket_y - 6), (max_x, bracket_y + 6)], fill=crimson, width=2)

draw.text(((min_x + max_x)//2, bracket_y + 18), "Range = 90 - 20 = 70", fill=crimson, font=get_font("segoeuib.ttf", 13), anchor="mm")


# -------------------------------------------------------------
# 5. VARIANCE & SD
# -------------------------------------------------------------
x1, y1 = col2_x, y_row2
x2, y2 = x1 + col_w, y1 + col_h
draw_panel_skeleton(x1, y1, x2, y2, "VARIANCE & STAND. DEVIATION", crimson, crimson_light)

# Formulas
fx1 = x1 + 20
fy = y1 + 65

# s^2
draw.text((fx1, fy + 12), "s", fill=crimson, font=get_font("segoeuib.ttf", 20))
draw.text((fx1 + 10, fy + 2), "2", fill=crimson, font=get_font("segoeuib.ttf", 12))
draw.text((fx1 + 22, fy + 12), "=", fill=charcoal, font=get_font("segoeui.ttf", 20))

# Numerator: Σ(x - x-bar)²
draw.text((fx1 + 42, fy - 6), "Σ(x - ", fill=crimson, font=get_font("segoeui.ttf", 18))
draw.text((fx1 + 90, fy - 6), "x", fill=crimson, font=get_font("segoeui.ttf", 18))
# Bar above the second x
draw.line([(fx1 + 88, fy - 5), (fx1 + 102, fy - 5)], fill=crimson, width=2)
# Closing parenthesis and squared symbol
draw.text((fx1 + 104, fy - 6), ")", fill=crimson, font=get_font("segoeui.ttf", 18))
draw.text((fx1 + 110, fy - 14), "2", fill=crimson, font=get_font("segoeui.ttf", 12))

# Fraction line
draw.line([(fx1 + 38, fy + 19), (fx1 + 125, fy + 19)], fill=charcoal, width=2)
draw.text((fx1 + 62, fy + 22), "n - 1", fill=crimson, font=get_font("segoeui.ttf", 15))

# s formula
fx2 = x1 + 180
draw.text((fx2, fy + 12), "s =", fill=crimson, font=get_font("segoeuib.ttf", 20))
# root symbol
rx = fx2 + 38
ry = fy + 18
draw.line([(rx, ry), (rx + 4, ry), (rx + 8, ry + 16), (rx + 14, ry - 14), (rx + 82, ry - 14)], fill=charcoal, width=2)
draw.text((rx + 18, ry - 10), "Variance", fill=crimson, font=get_font("segoeui.ttf", 14))

# Takeaway label on right
draw.text((x2 - 125, y1 + 75), "• s² = Variance", fill=crimson, font=get_font("segoeuib.ttf", 12))
draw.text((x2 - 125, y1 + 93), "• s  = Stand. Dev.", fill=crimson, font=get_font("segoeuib.ttf", 12))

# Visual: Bell curve
curve_pts = []
x_mean = x1 + 220
y_base = y1 + 280
sigma = 50
amplitude = 80
for cx in range(x1 + 50, x2 - 50 + 1):
    exponent = -0.5 * ((cx - x_mean) / sigma) ** 2
    cy = y_base - amplitude * math.exp(exponent)
    curve_pts.append((cx, cy))
draw.line(curve_pts, fill=crimson, width=3)

# Mean vertical line
draw.line([(x_mean, y_base), (x_mean, y_base - amplitude)], fill=charcoal, width=1)
draw.text((x_mean, y_base + 12), "x-bar", fill=charcoal, font=get_font("segoeuib.ttf", 11), anchor="mm")

# SD lines and arrows
sd_y = y_base - 30
for dy in range(0, 40, 6):
    draw.line([(x_mean - sigma, y_base - dy), (x_mean - sigma, y_base - dy - 3)], fill=axis_gray, width=1)
    draw.line([(x_mean + sigma, y_base - dy), (x_mean + sigma, y_base - dy - 3)], fill=axis_gray, width=1)
    
draw.line([(x_mean, sd_y), (x_mean + sigma, sd_y)], fill=crimson, width=2)
draw.polygon([(x_mean + sigma, sd_y), (x_mean + sigma - 5, sd_y - 3), (x_mean + sigma - 5, sd_y + 3)], fill=crimson)
draw.text((x_mean + sigma//2, sd_y - 10), "+s", fill=crimson, font=get_font("segoeuib.ttf", 10), anchor="mm")

draw.line([(x_mean, sd_y), (x_mean - sigma, sd_y)], fill=crimson, width=2)
draw.polygon([(x_mean - sigma, sd_y), (x_mean - sigma + 5, sd_y - 3), (x_mean - sigma + 5, sd_y + 3)], fill=crimson)
draw.text((x_mean - sigma//2, sd_y - 10), "-s", fill=crimson, font=get_font("segoeuib.ttf", 10), anchor="mm")

draw.text((x_mean - sigma, y_base + 12), "x-bar - s", fill=crimson, font=get_font("segoeui.ttf", 10), anchor="mm")
draw.text((x_mean + sigma, y_base + 12), "x-bar + s", fill=crimson, font=get_font("segoeui.ttf", 10), anchor="mm")


# -------------------------------------------------------------
# 6. IQR
# -------------------------------------------------------------
x1, y1 = col3_x, y_row2
x2, y2 = x1 + col_w, y1 + col_h
draw_panel_skeleton(x1, y1, x2, y2, "IQR (Interquartile Range)", crimson, crimson_light)

# Takeaway text
draw.text((x1 + 30, y1 + 75), "• IQR = Q3 - Q1", fill=crimson, font=get_font("segoeuib.ttf", 16))
draw.text((x1 + 30, y1 + 98), "• Robust to outliers\n• Measure of middle 50% spread", fill=charcoal, font=get_font("segoeui.ttf", 13))

# Visual: Boxplot
by = y1 + 200
bx_min = x1 + 50
bx_q1 = x1 + 130
bx_med = x1 + 195
bx_q3 = x1 + 285
bx_max = x1 + 370

# Whiskers
draw.line([(bx_min, by), (bx_q1, by)], fill=crimson, width=2)
draw.line([(bx_q3, by), (bx_max, by)], fill=crimson, width=2)

# Whisker caps
draw.line([(bx_min, by - 12), (bx_min, by + 12)], fill=crimson, width=2)
draw.line([(bx_max, by - 12), (bx_max, by + 12)], fill=crimson, width=2)

# Box
draw.rounded_rectangle([bx_q1, by - 25, bx_q3, by + 25], radius=4, fill=crimson_light, outline=crimson, width=3)

# Median line inside box
draw.line([(bx_med, by - 25), (bx_med, by + 25)], fill=crimson, width=3)

# Labels
lbl_font = get_font("segoeuib.ttf", 11)
draw.text((bx_min, by - 24), "Min", fill=charcoal, font=lbl_font, anchor="mm")
draw.text((bx_max, by - 24), "Max", fill=charcoal, font=lbl_font, anchor="mm")
draw.text((bx_q1, by - 38), "Q1 (25%)", fill=crimson, font=lbl_font, anchor="mm")
draw.text((bx_med, by + 38), "Median (Q2)", fill=crimson, font=lbl_font, anchor="mm")
draw.text((bx_q3, by - 38), "Q3 (75%)", fill=crimson, font=lbl_font, anchor="mm")

# IQR Bracket
bracket_y = by + 58
draw.line([(bx_q1, bracket_y), (bx_q3, bracket_y)], fill=crimson, width=2)
draw.line([(bx_q1, bracket_y - 6), (bx_q1, bracket_y + 6)], fill=crimson, width=2)
draw.line([(bx_q3, bracket_y - 6), (bx_q3, bracket_y + 6)], fill=crimson, width=2)

draw.text(((bx_q1 + bx_q3)//2, bracket_y + 16), "IQR = Q3 - Q1 (Middle 50%)", fill=crimson, font=get_font("segoeuib.ttf", 12), anchor="mm")

# Save Image
img.save(output_path, "PNG")
print(f"Image successfully saved to {output_path}")
