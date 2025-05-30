"""
Create an icon for the Utility Token Generation GUI
"""
import tkinter as tk
from PIL import Image, ImageDraw, ImageFont
import os

# Icon size
icon_size = (256, 256)

# Create a blank image with transparency
icon = Image.new('RGBA', icon_size, (0, 0, 0, 0))
draw = ImageDraw.Draw(icon)

# Calculate positions
center_x, center_y = icon_size[0]//2, icon_size[1]//2
radius = min(center_x, center_y) - 20

# Draw a green circle for the background
draw.ellipse(
    [(center_x - radius, center_y - radius), 
     (center_x + radius, center_y + radius)],
    fill=(76, 175, 80, 255),  # Green color
    outline=(46, 125, 50, 255),
    width=5
)

# Draw a token symbol (T)
try:
    font = ImageFont.truetype("arial.ttf", int(radius * 1.2))
except IOError:
    # Fallback to default font
    font = ImageFont.load_default()

# Draw text
text = "UT"
# Get text size using different methods depending on PIL version
try:
    # For newer Pillow versions
    _, _, text_width, text_height = font.getbbox(text)
except AttributeError:
    try:
        # For slightly older Pillow versions
        text_width, text_height = font.getsize(text)
    except AttributeError:
        # For even older versions
        text_width, text_height = draw.textsize(text, font=font) if hasattr(draw, 'textsize') else (radius, radius)
text_x = center_x - text_width//2
text_y = center_y - text_height//2

draw.text(
    (text_x, text_y),
    text,
    fill=(255, 255, 255, 255),  # White text
    font=font
)

# Save as ICO
icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
icon.save(icon_path, format="ICO")

print(f"Icon created and saved to: {icon_path}")
