import os
import math
from PIL import Image, ImageDraw, ImageFont

# Set up paths
font_dir = r"C:\Windows\Fonts"
output_dir = r"C:\Users\ankit\OneDrive\Desktop\sem\rds-images"
output_path = os.path.join(output_dir, "csv-io-flow.png")

os.makedirs(output_dir, exist_ok=True)

# Helper function to load Windows fonts
def get_font(font_name, size):
    path = os.path.join(font_dir, font_name)
    if os.path.exists(path):
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            return ImageFont.load_default()
    # Try alternate names
    for alt_name in [font_name, font_name.lower(), font_name.upper()]:
        alt_path = os.path.join(font_dir, alt_name)
        if os.path.exists(alt_path):
            try:
                return ImageFont.truetype(alt_path, size)
            except Exception:
                pass
    return ImageFont.load_default()

# Colors
bg_color = (253, 251, 247)  # Light cream paper background #FDFBF7
shadow_color = (242, 238, 230)  # Soft shadow #F2EEE6
forest_green = (42, 90, 67)  # Forest Green #2A5A43 (Arrows in, import)
forest_green_light = (238, 246, 242)  # Light green for import code blocks
slate_blue = (46, 91, 130)  # Slate Blue #2E5B82 (Arrows out, export)
slate_blue_light = (235, 242, 248)  # Light blue for export code blocks
charcoal = (51, 51, 51)  # Charcoal for general text #333333
gray_border = (200, 195, 185)  # Neutral border #C8C3B9
code_bg = (245, 245, 245)  # Soft gray for code block containers

# Initialize Canvas (1600x700 as requested)
img = Image.new("RGB", (1600, 700), bg_color)
draw = ImageDraw.Draw(img)

# Load Fonts
title_font = get_font("segoeuib.ttf", 36)
section_font = get_font("segoeuib.ttf", 18)
card_title_font = get_font("segoeuib.ttf", 15)
card_code_font = get_font("consola.ttf", 13)
card_code_font_small = get_font("consola.ttf", 11)
detail_font = get_font("segoeui.ttf", 13)
detail_font_bold = get_font("segoeuib.ttf", 13)

# -------------------------------------------------------------
# DRAW HEADER & TITLE
# -------------------------------------------------------------
title_text = "Reading & Writing Data in R"
draw.text((800, 45), title_text, fill=charcoal, font=title_font, anchor="mm")
# Accent line
draw.line([(700, 75), (900, 75)], fill=slate_blue, width=3)

# -------------------------------------------------------------
# DRAW SECTION HEADERS
# -------------------------------------------------------------
draw.text((240, 105), "READ / IMPORT", fill=forest_green, font=section_font, anchor="mm")
draw.text((1340, 105), "WRITE / EXPORT", fill=slate_blue, font=section_font, anchor="mm")

# -------------------------------------------------------------
# CARD DRAWING HELPER
# -------------------------------------------------------------
def draw_box(x1, y1, x2, y2, title, code_str, border_color, fill_color, code_txt_color, is_small_code=False, icon_type=None):
    # Draw soft flat shadow
    draw.rounded_rectangle([x1 + 4, y1 + 4, x2 + 4, y2 + 4], radius=8, fill=shadow_color)
    # Draw main box
    draw.rounded_rectangle([x1, y1, x2, y2], radius=8, fill=(255, 255, 255), outline=border_color, width=2)
    
    # Draw Icon
    icon_offset = 0
    if icon_type == "csv":
        # Draw paper icon
        draw.rounded_rectangle([x1 + 16, y1 + 14, x1 + 32, y1 + 34], radius=2, fill=fill_color, outline=border_color, width=1)
        draw.line([(x1 + 20, y1 + 20), (x1 + 28, y1 + 20)], fill=border_color, width=1)
        draw.line([(x1 + 20, y1 + 24), (x1 + 28, y1 + 24)], fill=border_color, width=1)
        draw.line([(x1 + 20, y1 + 28), (x1 + 28, y1 + 28)], fill=border_color, width=1)
        icon_offset = 24
    elif icon_type == "excel":
        # Draw green spreadsheet icon
        draw.rounded_rectangle([x1 + 14, y1 + 14, x1 + 34, y1 + 34], radius=2, fill=fill_color, outline=forest_green, width=1)
        # Grid lines
        draw.line([(x1 + 24, y1 + 14), (x1 + 24, y1 + 34)], fill=forest_green, width=1)
        draw.line([(x1 + 14, y1 + 24), (x1 + 34, y1 + 24)], fill=forest_green, width=1)
        icon_offset = 24
    elif icon_type == "db":
        # Draw database cylinders
        db_border = (100, 100, 100)
        draw.ellipse([x1 + 16, y1 + 14, x1 + 32, y1 + 20], fill=fill_color, outline=db_border, width=1)
        draw.ellipse([x1 + 16, y1 + 20, x1 + 32, y1 + 26], fill=fill_color, outline=db_border, width=1)
        draw.ellipse([x1 + 16, y1 + 26, x1 + 32, y1 + 32], fill=fill_color, outline=db_border, width=1)
        draw.line([(x1 + 16, y1 + 17), (x1 + 16, y1 + 29)], fill=db_border, width=1)
        draw.line([(x1 + 32, y1 + 17), (x1 + 32, y1 + 29)], fill=db_border, width=1)
        icon_offset = 24

    # Draw Title
    draw.text((x1 + 16 + icon_offset, y1 + 16), title, fill=charcoal, font=card_title_font)
    
    # Draw Code Block (gray capsule)
    code_bg_x1 = x1 + 16
    code_bg_y1 = y1 + 44
    code_bg_x2 = x2 - 16
    code_bg_y2 = y2 - 14
    draw.rounded_rectangle([code_bg_x1, code_bg_y1, code_bg_x2, code_bg_y2], radius=4, fill=code_bg)
    
    # Draw Code
    font_to_use = card_code_font_small if is_small_code else card_code_font
    draw.text((code_bg_x1 + 10, code_bg_y1 + (code_bg_y2 - code_bg_y1)//2), code_str, fill=code_txt_color, font=font_to_use, anchor="lm")

# -------------------------------------------------------------
# DRAW LEFT CARDS (READS)
# -------------------------------------------------------------
# Box 1: CSV read
draw_box(80, 140, 400, 230, "CSV File", "read.csv('file.csv')", forest_green, forest_green_light, forest_green, icon_type="csv")
# Box 2: Excel read
draw_box(80, 250, 400, 340, "Excel Spreadsheet", "readxl::read_excel()", forest_green, forest_green_light, forest_green, icon_type="excel")
# Box 3: Database read
draw_box(80, 360, 400, 450, "Database Connection", "RODBC/DBI sqlQuery()", forest_green, forest_green_light, forest_green, icon_type="db")

# -------------------------------------------------------------
# DRAW RIGHT CARDS (WRITES)
# -------------------------------------------------------------
# Box 1: CSV write (is_small_code=True to fit the long code string)
draw_box(1140, 180, 1540, 275, "CSV Export", "write.csv(df, 'out.csv', row.names = FALSE)", slate_blue, slate_blue_light, slate_blue, is_small_code=True, icon_type="csv")
# Box 2: Database write
draw_box(1140, 315, 1540, 410, "Database Save", "sqlSave()", slate_blue, slate_blue_light, slate_blue, icon_type="db")

# -------------------------------------------------------------
# DRAW CENTER CARD (R DATA FRAME)
# -------------------------------------------------------------
cx1, cy1, cx2, cy2 = 630, 205, 970, 385
# Draw shadow
draw.rounded_rectangle([cx1 + 6, cy1 + 6, cx2 + 6, cy2 + 6], radius=12, fill=shadow_color)
# Draw main box
draw.rounded_rectangle([cx1, cy1, cx2, cy2], radius=12, fill=(255, 255, 255), outline=slate_blue, width=3)

# Draw R Logo Oval
draw.ellipse([650, 255, 720, 335], fill=(230, 238, 248), outline=(160, 185, 215), width=2)
# Draw bold "R" in the logo
r_logo_font = get_font("segoeuib.ttf", 48)
draw.text((685, 290), "R", fill=(20, 80, 150), font=r_logo_font, anchor="mm")

# Draw "R data frame" text
df_title_font = get_font("segoeuib.ttf", 26)
draw.text((740, 270), "R data frame", fill=charcoal, font=df_title_font)

# Draw descriptive text inside center card
desc_font = get_font("segoeui.ttf", 14)
draw.text((740, 305), "• 2D Heterogeneous Table", fill=(100, 100, 100), font=desc_font)
draw.text((740, 325), "• Columns = vectors/factors", fill=(100, 100, 100), font=desc_font)
draw.text((740, 345), "• Fundamental R data structure", fill=(100, 100, 100), font=desc_font)

# -------------------------------------------------------------
# DRAW ARROWS
# -------------------------------------------------------------
def draw_arrow(x1, y1, x2, y2, color):
    # Draw line
    draw.line([(x1, y1), (x2, y2)], fill=color, width=4)
    # Calculate arrowhead direction
    dx = x2 - x1
    dy = y2 - y1
    length = math.sqrt(dx*dx + dy*dy)
    if length > 0:
        ux = dx / length
        uy = dy / length
        arrow_len = 16
        arrow_width = 8
        bx = x2 - arrow_len * ux
        by = y2 - arrow_len * uy
        nx = -uy
        ny = ux
        p1 = (x2, y2)
        p2 = (bx + arrow_width * nx, by + arrow_width * ny)
        p3 = (bx - arrow_width * nx, by - arrow_width * ny)
        draw.polygon([p1, p2, p3], fill=color)

# Arrows IN (Forest Green) - adjust endpoints slightly to avoid overlap
draw_arrow(405, 185, 620, 240, forest_green)
draw_arrow(405, 295, 620, 295, forest_green)
draw_arrow(405, 405, 620, 350, forest_green)

# Arrows OUT (Slate Blue)
draw_arrow(980, 255, 1130, 227.5, slate_blue)
draw_arrow(980, 335, 1130, 362.5, slate_blue)

# -------------------------------------------------------------
# DRAW TIP STRIP
# -------------------------------------------------------------
ts_x1, ts_y1, ts_x2, ts_y2 = 80, 495, 1520, 635
# Draw shadow
draw.rounded_rectangle([ts_x1 + 4, ts_y1 + 4, ts_x2 + 4, ts_y2 + 4], radius=8, fill=shadow_color)
# Draw body
draw.rounded_rectangle([ts_x1, ts_y1, ts_x2, ts_y2], radius=8, fill=(250, 248, 242), outline=gray_border, width=2)

# Draw "BEST PRACTICES & TIPS" badge/label on the left
badge_x1, badge_y1, badge_x2, badge_y2 = 80, 495, 210, 635
draw.rounded_rectangle([badge_x1, badge_y1, badge_x2, badge_y2], radius=8, fill=slate_blue)
# Draw vertical text or draw normal horizontal text rotated? Let's just draw horizontal text inside the badge.
# Actually, let's draw it in two lines to fit nicely:
draw.text((145, 545), "CRITICAL", fill=(255, 255, 255), font=get_font("segoeuib.ttf", 15), anchor="mm")
draw.text((145, 565), "I/O", fill=(255, 255, 255), font=get_font("segoeuib.ttf", 15), anchor="mm")
draw.text((145, 585), "TIPS", fill=(255, 255, 255), font=get_font("segoeuib.ttf", 15), anchor="mm")

# Three Tip Columns
# Column 1: header = TRUE
c1_cx = 380
draw.text((c1_cx, 535), "header = TRUE default", fill=charcoal, font=get_font("consola.ttf", 14), anchor="mm")
draw.text((c1_cx, 565), "Treats the first row as column names.", fill=(80, 80, 80), font=detail_font, anchor="mm")
draw.text((c1_cx, 585), "Use header = FALSE if file has no header.", fill=(110, 110, 110), font=detail_font, anchor="mm")

# Divider 1
draw.line([(570, 520), (570, 610)], fill=gray_border, width=1)

# Column 2: stringsAsFactors
c2_cx = 830
draw.text((c2_cx, 535), "stringsAsFactors", fill=charcoal, font=get_font("consola.ttf", 14), anchor="mm")
draw.text((c2_cx, 565), "Set to FALSE to keep text columns as characters.", fill=(80, 80, 80), font=detail_font, anchor="mm")
draw.text((c2_cx, 585), "Note: default is FALSE in R 4.0+.", fill=(110, 110, 110), font=detail_font, anchor="mm")

# Divider 2
draw.line([(1090, 520), (1090, 610)], fill=gray_border, width=1)

# Column 3: check getwd() / setwd()
c3_cx = 1300
draw.text((c3_cx, 535), "check getwd() / setwd()", fill=charcoal, font=get_font("consola.ttf", 14), anchor="mm")
draw.text((c3_cx, 565), "Verify active folder using getwd() before reading.", fill=(80, 80, 80), font=detail_font, anchor="mm")
draw.text((c3_cx, 585), "Set path via setwd('path') if files are missing.", fill=(110, 110, 110), font=detail_font, anchor="mm")

# Save image
img.save(output_path, "PNG")
print(f"Successfully generated diagram and saved to {output_path}")
