import os
import sys
from PIL import Image, ImageDraw, ImageFont

# Set up paths
font_dir = r"C:\Windows\Fonts"
output_dir = r"C:\Users\ankit\OneDrive\Desktop\sem\rds-images"
output_path = os.path.join(output_dir, "r-data-structures.png")

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
forest_green = (42, 90, 67)      # #2A5A43 (Homogeneous structures)
forest_green_light = (234, 244, 238) # #EAF4EE
slate_blue = (46, 91, 130)       # #2E5B82 (Heterogeneous structures)
slate_blue_light = (230, 240, 250)   # #E6F0FA
charcoal = (51, 51, 51)          # #333333 (General text, factor)
factor_purple = (94, 75, 139)    # #5E4B8B (Factor accent)
factor_purple_light = (243, 232, 255) # #F3E8FF
gray_border = (182, 194, 201)    # #B6C2C9
axis_gray = (126, 141, 153)      # #7E8D99
shadow_color = (235, 231, 220)   # #EBE7DC

# -------------------------------------------------------------
# DRAW TITLE & HEADER
# -------------------------------------------------------------
title_font = get_font("segoeuib.ttf", 44)
subtitle_font = get_font("segoeuii.ttf", 18)

# Title text
title_text = "R Data Structures"
# Draw centered title
draw.text((800, 45), title_text, fill=charcoal, font=title_font, anchor="mm")

# Subtitle
subtitle_text = "A classification by dimensionality and data type homogeneity"
draw.text((800, 85), subtitle_text, fill=(100, 100, 100), font=subtitle_font, anchor="mm")

# Decorative line under title
draw.line([(700, 105), (900, 105)], fill=forest_green, width=3)

# -------------------------------------------------------------
# DRAW AXES & LABELS
# -------------------------------------------------------------
axis_label_font = get_font("segoeuib.ttf", 18)
axis_desc_font = get_font("segoeuii.ttf", 14)

# Y-Axis (Vertical): Dimension (1-D vs 2-D)
# Upward Arrow (1-D)
draw.line([(800, 390), (800, 130)], fill=axis_gray, width=3)
draw.polygon([(800, 125), (792, 140), (808, 140)], fill=axis_gray)
draw.text((800, 115), "1-D (Linear)", fill=charcoal, font=axis_label_font, anchor="mb")

# Downward Arrow (2-D)
draw.line([(800, 610), (800, 850)], fill=axis_gray, width=3)
draw.polygon([(800, 855), (792, 840), (808, 840)], fill=axis_gray)
draw.text((800, 865), "2-D (Grid / Table)", fill=charcoal, font=axis_label_font, anchor="mt")

# X-Axis (Horizontal): Homogeneity (Same Type vs Mixed Types)
# Left Arrow (Same Type)
draw.line([(600, 500), (120, 500)], fill=axis_gray, width=3)
draw.polygon([(115, 500), (130, 492), (130, 508)], fill=axis_gray)
draw.text((55, 490), "SAME TYPE", fill=forest_green, font=axis_label_font, anchor="rm")
draw.text((55, 510), "(Homogeneous)", fill=(100, 100, 100), font=axis_desc_font, anchor="rm")

# Right Arrow (Mixed Types)
draw.line([(1000, 500), (1480, 500)], fill=axis_gray, width=3)
draw.polygon([(1485, 500), (1470, 492), (1470, 508)], fill=axis_gray)
draw.text((1545, 490), "MIXED TYPES", fill=slate_blue, font=axis_label_font, anchor="lm")
draw.text((1545, 510), "(Heterogeneous)", fill=(100, 100, 100), font=axis_desc_font, anchor="lm")


# -------------------------------------------------------------
# BOX DRAWING HELPER
# -------------------------------------------------------------
def draw_card(x1, y1, x2, y2, title, subtitle, code_lines, border_color, accent_color):
    # Draw soft flat shadow
    draw.rounded_rectangle([x1 + 6, y1 + 6, x2 + 6, y2 + 6], radius=10, fill=shadow_color)
    # Draw card body
    draw.rounded_rectangle([x1, y1, x2, y2], radius=10, fill=(255, 255, 255), outline=border_color, width=2)
    
    # Draw Title
    card_title_font = get_font("segoeuib.ttf", 24)
    draw.text((x1 + 24, y1 + 20), title, fill=accent_color, font=card_title_font)
    
    # Draw Subtitle
    card_sub_font = get_font("segoeui.ttf", 15)
    draw.text((x1 + 24, y1 + 54), subtitle, fill=(120, 120, 120), font=card_sub_font)
    
    # Draw Code Block (gray capsule)
    code_bg_x1 = x1 + 24
    code_bg_y1 = y1 + 84
    code_bg_x2 = x1 + 210
    code_bg_y2 = y1 + 156
    draw.rounded_rectangle([code_bg_x1, code_bg_y1, code_bg_x2, code_bg_y2], radius=6, fill=(245, 245, 245))
    
    # Draw Code lines
    card_code_font = get_font("consola.ttf", 14)
    y_offset = 8
    for line in code_lines:
        draw.text((code_bg_x1 + 10, code_bg_y1 + y_offset), line, fill=(50, 50, 50), font=card_code_font)
        y_offset += 18

# Box coordinates configuration
box_w = 380
box_h = 180

# -------------------------------------------------------------
# 1. VECTOR (Top-Left)
# -------------------------------------------------------------
vx1, vy1 = 130, 140
vx2, vy2 = vx1 + box_w, vy1 + box_h
draw_card(vx1, vy1, vx2, vy2, "VECTOR", "1-D • Homogeneous", ["c(1, 2, 3)", "# Base 1D type"], forest_green, forest_green)

# Visual for Vector: Row of cells
v_vis_cx = vx1 + 295
v_vis_cy = vy1 + 90
cell_size = 32
cells_num = 4
v_start_x = v_vis_cx - (cells_num * cell_size + (cells_num - 1) * 4) // 2
v_start_y = v_vis_cy - cell_size // 2

cell_font = get_font("segoeuib.ttf", 14)
for i in range(cells_num):
    cx1 = v_start_x + i * (cell_size + 4)
    cy1 = v_start_y
    cx2 = cx1 + cell_size
    cy2 = cy1 + cell_size
    draw.rounded_rectangle([cx1, cy1, cx2, cy2], radius=4, fill=forest_green_light, outline=forest_green, width=2)
    draw.text((cx1 + cell_size//2, cy1 + cell_size//2), str(i+1), fill=forest_green, font=cell_font, anchor="mm")

# -------------------------------------------------------------
# 2. MATRIX (Bottom-Left)
# -------------------------------------------------------------
mx1, my1 = 130, 680
mx2, my2 = mx1 + box_w, my1 + box_h
draw_card(mx1, my1, mx2, my2, "MATRIX", "2-D • Homogeneous", ["matrix(1:6, nrow=2)", "# 2 rows, 3 cols"], forest_green, forest_green)

# Visual for Matrix: 2D Grid
m_vis_cx = mx1 + 295
m_vis_cy = my1 + 90
m_rows, m_cols = 2, 3
m_start_x = m_vis_cx - (m_cols * cell_size + (m_cols - 1) * 4) // 2
m_start_y = m_vis_cy - (m_rows * cell_size + (m_rows - 1) * 4) // 2

vals = [["1", "3", "5"], ["2", "4", "6"]] # column-major
for r in range(m_rows):
    for c in range(m_cols):
        cx1 = m_start_x + c * (cell_size + 4)
        cy1 = m_start_y + r * (cell_size + 4)
        cx2 = cx1 + cell_size
        cy2 = cy1 + cell_size
        draw.rounded_rectangle([cx1, cy1, cx2, cy2], radius=4, fill=forest_green_light, outline=forest_green, width=2)
        draw.text((cx1 + cell_size//2, cy1 + cell_size//2), vals[r][c], fill=forest_green, font=cell_font, anchor="mm")

# -------------------------------------------------------------
# 3. LIST (Top-Right)
# -------------------------------------------------------------
lx1, ly1 = 1090, 140
lx2, ly2 = lx1 + box_w, ly1 + box_h
draw_card(lx1, ly1, lx2, ly2, "LIST", "1-D • Heterogeneous", ["list(1, 'a', TRUE)", "# Mixed data types"], slate_blue, slate_blue)

# Visual for List: Mixed shape/type cells
l_vis_cx = lx1 + 295
l_vis_cy = ly1 + 90
l_cells = 3
l_cell_w = 34
l_spacing = 8
l_start_x = l_vis_cx - (l_cells * l_cell_w + (l_cells - 1) * l_spacing) // 2
l_start_y = l_vis_cy - l_cell_w // 2

# Cell 1: Numeric (Blue Square)
lc1_x1 = l_start_x
lc1_y1 = l_start_y
lc1_x2 = lc1_x1 + l_cell_w
lc1_y2 = lc1_y1 + l_cell_w
draw.rounded_rectangle([lc1_x1, lc1_y1, lc1_x2, lc1_y2], radius=4, fill=slate_blue_light, outline=slate_blue, width=2)
draw.text((lc1_x1 + l_cell_w//2, lc1_y1 + l_cell_w//2), "1", fill=slate_blue, font=cell_font, anchor="mm")

# Cell 2: Character (Orange Circle)
lc2_x1 = l_start_x + (l_cell_w + l_spacing)
lc2_y1 = l_start_y
lc2_x2 = lc2_x1 + l_cell_w
lc2_y2 = lc2_y1 + l_cell_w
draw.ellipse([lc2_x1, lc2_y1, lc2_x2, lc2_y2], fill=(253, 242, 226), outline=(217, 119, 6), width=2)
draw.text((lc2_x1 + l_cell_w//2, lc2_y1 + l_cell_w//2), "'a'", fill=(180, 83, 9), font=cell_font, anchor="mm")

# Cell 3: Logical (Green Capsule/Diamond style)
lc3_x1 = l_start_x + 2 * (l_cell_w + l_spacing)
lc3_y1 = l_start_y
lc3_x2 = lc3_x1 + l_cell_w
lc3_y2 = lc3_y1 + l_cell_w
draw.rounded_rectangle([lc3_x1, lc3_y1, lc3_x2, lc3_y2], radius=10, fill=forest_green_light, outline=forest_green, width=2)
draw.text((lc3_x1 + l_cell_w//2, lc3_y1 + l_cell_w//2), "T", fill=forest_green, font=cell_font, anchor="mm")

# -------------------------------------------------------------
# 4. DATA FRAME (Bottom-Right)
# -------------------------------------------------------------
dfx1, dfy1 = 1090, 680
dfx2, dfy2 = dfx1 + box_w, dfy1 + box_h
draw_card(dfx1, dfy1, dfx2, dfy2, "DATA FRAME", "2-D • Heterogeneous", ["data.frame(", "  id=1:3,", "  gp=c('A','B','A')", ")"], slate_blue, slate_blue)

# Visual for Data Frame: Spreadsheet table
df_vis_cx = dfx1 + 295
df_vis_cy = dfy1 + 90
df_cols, df_rows = 2, 3
df_col_w = 60
df_row_h = 22
df_start_x = df_vis_cx - (df_cols * df_col_w) // 2
df_start_y = df_vis_cy - (df_rows * df_row_h) // 2

# Table cell font
df_font = get_font("segoeui.ttf", 12)
df_header_font = get_font("segoeuib.ttf", 12)

headers = ["id", "gp"]
row_data = [
    ["1", "A"],
    ["2", "B"],
    ["3", "A"]
]

# Draw headers
for c in range(df_cols):
    cx1 = df_start_x + c * df_col_w
    cy1 = df_start_y
    cx2 = cx1 + df_col_w
    cy2 = cy1 + df_row_h
    # Fill headers with dark background
    bg = slate_blue if c == 0 else (217, 119, 6)
    draw.rectangle([cx1, cy1, cx2, cy2], fill=bg, outline=(255, 255, 255), width=1)
    draw.text((cx1 + df_col_w//2, cy1 + df_row_h//2), headers[c], fill=(255, 255, 255), font=df_header_font, anchor="mm")

# Draw data rows
for r in range(1, df_rows):
    for c in range(df_cols):
        cx1 = df_start_x + c * df_col_w
        cy1 = df_start_y + r * df_row_h
        cx2 = cx1 + df_col_w
        cy2 = cy1 + df_row_h
        bg = slate_blue_light if c == 0 else (253, 242, 226)
        text_color = slate_blue if c == 0 else (180, 83, 9)
        draw.rectangle([cx1, cy1, cx2, cy2], fill=bg, outline=(200, 200, 200), width=1)
        draw.text((cx1 + df_col_w//2, cy1 + df_row_h//2), row_data[r-1][c], fill=text_color, font=df_font, anchor="mm")

# -------------------------------------------------------------
# 5. FACTOR (Center)
# -------------------------------------------------------------
fx1, fy1 = 610, 410
fx2, fy2 = fx1 + box_w, fy1 + box_h
draw_card(fx1, fy1, fx2, fy2, "FACTOR", "Categorical Vector", ["factor(c('H', 'L', 'H'))", "# Levels: H, L"], factor_purple, factor_purple)

# Visual for Factor: Category Chips
f_vis_cx = fx1 + 295
f_vis_cy = fy1 + 82
chip_w = 42
chip_h = 24
chip_spacing = 6
chips_count = 3
f_start_x = f_vis_cx - (chips_count * chip_w + (chips_count - 1) * chip_spacing) // 2
f_start_y = f_vis_cy - chip_h // 2

chip_labels = ["High", "Low", "High"]
chip_colors = [
    (forest_green_light, forest_green),
    (slate_blue_light, slate_blue),
    (forest_green_light, forest_green)
]

chip_font = get_font("segoeuib.ttf", 11)
for i in range(chips_count):
    cx1 = f_start_x + i * (chip_w + chip_spacing)
    cy1 = f_start_y
    cx2 = cx1 + chip_w
    cy2 = cy1 + chip_h
    bg, fg = chip_colors[i]
    draw.rounded_rectangle([cx1, cy1, cx2, cy2], radius=12, fill=bg, outline=fg, width=2)
    draw.text((cx1 + chip_w//2, cy1 + chip_h//2), chip_labels[i], fill=fg, font=chip_font, anchor="mm")

# Factor Levels label below chips
levels_font = get_font("segoeuii.ttf", 13)
draw.text((f_vis_cx, f_vis_cy + 28), "Levels: Low < High", fill=(100, 100, 100), font=levels_font, anchor="mm")

# Save Image
img.save(output_path, "PNG")
print(f"Image successfully saved to {output_path}")
