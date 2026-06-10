import os
import sys
from PIL import Image, ImageDraw, ImageFont

# Set up paths
font_dir = r"C:\Windows\Fonts"
output_dir = r"C:\Users\ankit\OneDrive\Desktop\sem\rds-images"
output_path = os.path.join(output_dir, "oop-s3-s4-r5.png")

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
# 1600x800 textbook-style background (light cream)
bg_color = (253, 251, 247)  # #FDFBF7 (light cream paper background)
img = Image.new("RGB", (1600, 800), bg_color)
draw = ImageDraw.Draw(img)

# Define Colors
forest_green = (34, 112, 63)       # #22703F (S3)
forest_green_light = (235, 246, 238) # #EBF6EE (S3 code / light bg)
slate_blue = (46, 91, 130)        # #2E5B82 (S4)
slate_blue_light = (235, 242, 248)  # #EBF2F8 (S4 code / light bg)
copper = (184, 92, 26)            # #B85C1A (R5 Reference Classes)
copper_light = (253, 243, 234)      # #FDF3EA (R5 code / light bg)

charcoal = (51, 51, 51)           # #333333 (General text)
text_gray = (102, 102, 102)        # #666666 (Subtitles, labels)
code_comment_color = (115, 135, 115) # #738773 (Code comments)
code_keyword_color = (150, 40, 120)  # #962878 (Code keywords)
code_text_color = (40, 40, 40)       # #282828 (Standard code)

gray_border = (205, 205, 195)     # #CDCDC3 (Card border)
shadow_color = (240, 236, 226)    # #F0ECE2 (Soft drop shadow)
bottom_bg = (243, 239, 230)       # #F3EFE6 (Bottom strip background)
bottom_border = (195, 190, 180)   # #C3BEB4 (Bottom strip border)

# -------------------------------------------------------------
# DRAW TITLE & HEADER
# -------------------------------------------------------------
title_font = get_font("segoeuib.ttf", 36)
subtitle_font = get_font("segoeuii.ttf", 16)

# Title text
title_text = "OOP in R: S3 vs S4 vs Reference Classes"
draw.text((800, 40), title_text, fill=charcoal, font=title_font, anchor="mm")

# Subtitle
subtitle_text = "A comparative overview of the three primary object-oriented systems in the R language"
draw.text((800, 78), subtitle_text, fill=text_gray, font=subtitle_font, anchor="mm")

# Decorative line under title
draw.line([(650, 100), (950, 100)], fill=(180, 180, 170), width=2)

# -------------------------------------------------------------
# CARD DRAWING HELPER
# -------------------------------------------------------------
def draw_panel(x1, y1, x2, y2, title, tagline, system_name, code_lines, bullets, accent_color, accent_light):
    # Draw soft flat shadow
    draw.rounded_rectangle([x1 + 6, y1 + 6, x2 + 6, y2 + 6], radius=12, fill=shadow_color)
    # Draw card body
    draw.rounded_rectangle([x1, y1, x2, y2], radius=12, fill=(255, 255, 255), outline=gray_border, width=2)
    
    # Draw Top Accent Pill
    draw.rounded_rectangle([x1 + 18, y1 + 12, x2 - 18, y1 + 18], radius=3, fill=accent_color)
    
    # Draw System Type Label (e.g. "S3 SYSTEM")
    type_font = get_font("segoeuib.ttf", 13)
    draw.text((x1 + 24, y1 + 28), system_name, fill=text_gray, font=type_font)
    
    # Draw Title
    card_title_font = get_font("segoeuib.ttf", 26)
    draw.text((x1 + 24, y1 + 46), title, fill=accent_color, font=card_title_font)
    
    # Draw Tagline
    card_tag_font = get_font("segoeuii.ttf", 14)
    draw.text((x1 + 24, y1 + 84), tagline, fill=text_gray, font=card_tag_font)
    
    # Draw Code Block (light capsule)
    code_bg_x1 = x1 + 20
    code_bg_y1 = y1 + 115
    code_bg_x2 = x2 - 20
    code_bg_y2 = y1 + 265
    draw.rounded_rectangle([code_bg_x1, code_bg_y1, code_bg_x2, code_bg_y2], radius=8, fill=accent_light, outline=gray_border, width=1)
    
    # Draw Code lines (with syntax highlighting)
    card_code_font = get_font("consola.ttf", 13)
    y_offset = 10
    
    for line in code_lines:
        x_offset = 12
        # Check if comment
        if line.strip().startswith("#"):
            draw.text((code_bg_x1 + x_offset, code_bg_y1 + y_offset), line, fill=code_comment_color, font=card_code_font)
        else:
            # Tokenize simple keywords for styling
            tokens = line.split(" ")
            current_x = code_bg_x1 + x_offset
            for token in tokens:
                # Basic keywords
                if token in ["list", "class<-", "function", "cat", "setClass", "new", "setRefClass"]:
                    draw.text((current_x, code_bg_y1 + y_offset), token, fill=code_keyword_color, font=card_code_font)
                else:
                    draw.text((current_x, code_bg_y1 + y_offset), token, fill=code_text_color, font=card_code_font)
                # Re-add space
                space_w = draw.textlength(" ", font=card_code_font)
                token_w = draw.textlength(token, font=card_code_font)
                current_x += token_w + space_w
                
        y_offset += 17

    # Draw Bullets
    bullet_title_font = get_font("segoeuib.ttf", 14)
    bullet_body_font = get_font("segoeui.ttf", 13)
    
    by_start = y1 + 285
    for i, (b_title, b_body) in enumerate(bullets):
        by = by_start + i * 46
        # Draw custom bullet marker (colored square or circle)
        marker_size = 8
        mx = x1 + 26
        my = by + 6
        draw.rectangle([mx, my, mx + marker_size, my + marker_size], fill=accent_color)
        
        # Draw bold lead-in
        lead_in = b_title + ": "
        draw.text((x1 + 42, by), lead_in, fill=charcoal, font=bullet_title_font)
        
        # Draw body text after lead-in
        lead_w = draw.textlength(lead_in, font=bullet_title_font)
        draw.text((x1 + 42 + lead_w, by + 1), b_body, fill=charcoal, font=bullet_body_font)

# Define Panels coordinates
box_w = 460
box_h = 480
y_start = 130

# S3 Panel (Left)
s3_x1 = 70
s3_x2 = s3_x1 + box_w
s3_code = [
    "# Create list & assign class",
    "p <- list(name = \"Alice\", age = 30)",
    "class(p) <- \"Person\"",
    "",
    "# Generic & method definition",
    "print.Person <- function(x) {",
    "  cat(\"S3:\", x$name, \"\\n\")",
    "}"
]
s3_bullets = [
    ("Informal OOP", "No formal class schema or structure definitions."),
    ("Class Attribute", "Objects are base types (lists) with a \"class\" attribute."),
    ("Generic Dispatch", "Dispatched at runtime using UseMethod(\"generic\")."),
    ("Simplest System", "Easiest to write; used for >90% of base R functions.")
]
draw_panel(s3_x1, y_start, s3_x2, y_start + box_h, "S3 Class", "simplest, most of base R", "S3 SYSTEM", s3_code, s3_bullets, forest_green, forest_green_light)

# S4 Panel (Middle)
s4_x1 = 570
s4_x2 = s4_x1 + box_w
s4_code = [
    "# Define S4 class & typed slots",
    "setClass(\"Person\",",
    "  slots = c(name=\"character\", age=\"numeric\")",
    ")",
    "# Instantiate object",
    "p <- new(\"Person\", name=\"Alice\", age=30)",
    "# Access slot using @",
    "p@name"
]
s4_bullets = [
    ("Formal OOP", "Class defined using setClass() with strict typed slots."),
    ("Multiple Dispatch", "setMethod() dispatches based on multiple arguments."),
    ("Slot Accessor", "Slots are accessed using @ operator (e.g. obj@slot)."),
    ("Rigorous & Safe", "Supports validity checks; preferred by Bioconductor.")
]
draw_panel(s4_x1, y_start, s4_x2, y_start + box_h, "S4 Class", "rigorous, Bioconductor", "S4 SYSTEM", s4_code, s4_bullets, slate_blue, slate_blue_light)

# R5 Reference Classes Panel (Right)
r5_x1 = 1070
r5_x2 = r5_x1 + box_w
r5_code = [
    "# Define Reference Class",
    "Person <- setRefClass(\"Person\",",
    "  fields = list(name=\"character\", age=\"numeric\"),",
    "  methods = list(",
    "    greet = function() { cat(\"Hi\", name) }",
    "  )",
    ")",
    "p <- Person$new(name=\"Alice\", age=30)"
]
r5_bullets = [
    ("Reference Semantics", "Objects are mutable; modified in-place, no copying."),
    ("Encapsulated OOP", "Fields and methods defined inside setRefClass()."),
    ("Method Invocation", "Methods are called using $ operator (e.g. obj$greet())."),
    ("Familiar OOP Style", "Behaves like standard OOP in Java, Python, or C++.")
]
draw_panel(r5_x1, y_start, r5_x2, y_start + box_h, "Reference Class", "OOP like Java/Python", "R5 SYSTEM", r5_code, r5_bullets, copper, copper_light)


# -------------------------------------------------------------
# DRAW BOTTOM COMPARISON STRIP
# -------------------------------------------------------------
bottom_y1 = 640
bottom_y2 = bottom_y1 + 120
bottom_width = s5_x2_temp = r5_x2

# Draw background capsule
draw.rounded_rectangle([s3_x1 + 6, bottom_y1 + 6, r5_x2 + 6, bottom_y2 + 6], radius=10, fill=shadow_color)
draw.rounded_rectangle([s3_x1, bottom_y1, r5_x2, bottom_y2], radius=10, fill=bottom_bg, outline=bottom_border, width=2)

# Divider X-coordinates (align with gaps between panels)
div1_x = 550
div2_x = 1050

draw.line([(div1_x, bottom_y1 + 8), (div1_x, bottom_y2 - 8)], fill=bottom_border, width=1)
draw.line([(div2_x, bottom_y1 + 8), (div2_x, bottom_y2 - 8)], fill=bottom_border, width=1)

# Label & Value Fonts
tbl_lbl_font = get_font("segoeui.ttf", 13)
tbl_val_font = get_font("segoeuib.ttf", 14)

def draw_row(x_start, x_end, y_pos, label, val_text, val_color):
    # Draw label (left aligned)
    draw.text((x_start + 24, y_pos), label, fill=text_gray, font=tbl_lbl_font)
    # Draw value (right aligned)
    draw.text((x_end - 24, y_pos), val_text, fill=val_color, font=tbl_val_font, anchor="ra")

# Row 1: Formality
y1 = bottom_y1 + 18
draw_row(s3_x1, div1_x, y1, "Formality", "Low (Informal / Ad-hoc)", forest_green)
draw_row(div1_x, div2_x, y1, "Formality", "High (Formal / Schema)", slate_blue)
draw_row(div2_x, r5_x2, y1, "Formality", "High (Formal / Encapsulated)", copper)

# Row 2: Mutability
y2 = bottom_y1 + 48
draw_row(s3_x1, div1_x, y2, "Mutability", "Copy-on-Modify (Immutable)", forest_green)
draw_row(div1_x, div2_x, y2, "Mutability", "Copy-on-Modify (Immutable)", slate_blue)
draw_row(div2_x, r5_x2, y2, "Mutability", "In-Place (Mutable)", copper)

# Row 3: Dispatch & Calling Style
y3 = bottom_y1 + 78
draw_row(s3_x1, div1_x, y3, "Dispatch Style", "Generic-based (generic(obj))", forest_green)
draw_row(div1_x, div2_x, y3, "Dispatch Style", "Generic-based (generic(obj))", slate_blue)
draw_row(div2_x, r5_x2, y3, "Calling Style", "Message-passing (obj$method())", copper)

# Save Image
img.save(output_path, "PNG")
print(f"Image successfully saved to {output_path}")
