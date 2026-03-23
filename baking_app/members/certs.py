from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
import os

def generate_certificate(member, output_path):

        # Open the image
        template_path = os.path.join(settings.BASE_DIR, f"certificate_templates/{settings.CERT_IMAGE_FILE}")
        background = Image.open(template_path).convert("RGB")
        draw = ImageDraw.Draw(background)

        # Load a font
        font_path = os.path.join(settings.BASE_DIR, 'static/fonts/GothicB.ttf')
        line_height = 30

        # Generate the business name text
        font = ImageFont.truetype(font_path, size=line_height)
        business_name_text = f"{member.business_name}"
        
        # Determine the correct position
        column_x_start = 505          
        max_width = 1080 - 505
        start_y = 480

        # Ensure text fits within the image column 
        wrapped_lines = wrap_text(draw, business_name_text, font, max_width)

        # draw text onto image 
        for i, line in enumerate(wrapped_lines):
            text_width, _ = draw.textsize(line, font=font)
            x = column_x_start + (max_width - text_width) // 2
            y = start_y + i * line_height
            draw.text((x, y), line, font=font, fill="black")

        # draw membership number onto image
        font = ImageFont.truetype(font_path, size=24)
        membership_number_text = f"{member.membership_number}"
        draw.text((600, 600), membership_number_text, font=font, fill="black")

        # Save to PDF
        background.save(output_path, "PDF", resolution=100.0)

def wrap_text(draw, text, font, max_width):
    words = text.strip().split()
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        text_width, _ = draw.textsize(test_line, font=font)
        if text_width > max_width and current_line:
            lines.append(current_line)
            current_line = word
        else:
            current_line = test_line

    if current_line:
        lines.append(current_line)

    return lines