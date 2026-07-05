#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate images locally using PIL/Pillow based on post content.
Creates blackboard-style educational infographics for LinkedIn posts.

This uses local image generation (PIL) rather than external APIs for reliability.
"""

import sys
import os
import textwrap
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import random

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from config.logger import get_logger
from config.constants import TODAY

logger = get_logger(__name__)

OUTPUT_DIR = "output/posts_generated_images"

# ============================================================================
# Color Palettes
# ============================================================================

BLACKBOARD_PALETTE = {
    "bg": (30, 45, 75),           # Dark blue-black
    "chalk_white": (245, 245, 245),
    "chalk_yellow": (255, 225, 50),
    "chalk_green": (150, 255, 150),
    "chalk_pink": (255, 150, 200),
    "chalk_orange": (255, 180, 80),
}

# ============================================================================
# Image Generation
# ============================================================================

def wrap_text(text: str, max_chars: int = 40) -> list:
    """Wrap text for display on image."""
    lines = []
    for line in text.split('\n'):
        if len(line) <= max_chars:
            lines.append(line)
        else:
            wrapped = textwrap.wrap(line, width=max_chars)
            lines.extend(wrapped)
    return lines


def generate_blackboard_image(content: str, post_type: str) -> str:
    """
    Generate a blackboard-style educational image using PIL.
    
    Args:
        content: The LinkedIn post text
        post_type: Type of post (Carousel, Infographic, Motivation)
    
    Returns:
        Path to generated image
    """
    try:
        # Create image with blackboard background
        img = Image.new("RGB", (1200, 1800), color=BLACKBOARD_PALETTE["bg"])
        draw = ImageDraw.Draw(img)
        
        # Load fonts (with fallback)
        try:
            title_font = ImageFont.truetype("arial.ttf", 60)
            text_font = ImageFont.truetype("arial.ttf", 36)
            small_font = ImageFont.truetype("arial.ttf", 28)
        except:
            # Fallback to default font
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        # Choose chalk color based on type
        colors = [
            BLACKBOARD_PALETTE["chalk_yellow"],
            BLACKBOARD_PALETTE["chalk_green"],
            BLACKBOARD_PALETTE["chalk_pink"],
            BLACKBOARD_PALETTE["chalk_orange"],
        ]
        chalk_color = random.choice(colors)
        
        y_pos = 80
        
        # Draw title
        title_text = post_type
        title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (1200 - title_width) // 2
        draw.text((title_x, y_pos), title_text, fill=BLACKBOARD_PALETTE["chalk_white"], font=title_font)
        
        # Draw decorative line
        y_pos += 100
        draw.line([(100, y_pos), (1100, y_pos)], fill=chalk_color, width=3)
        y_pos += 50
        
        # Draw content (wrap to fit)
        lines = wrap_text(content[:300], max_chars=45)  # Limit content
        
        for line in lines:
            if y_pos > 1650:  # Stop if we're running out of space
                break
            
            # Alternate colors for visual interest
            line_color = chalk_color if random.random() > 0.5 else BLACKBOARD_PALETTE["chalk_white"]
            
            draw.text((120, y_pos), f"• {line}", fill=line_color, font=text_font)
            y_pos += 80
        
        # Add footer with date
        footer_text = f"Generated: {datetime.now().strftime('%Y-%m-%d')}"
        footer_bbox = draw.textbbox((0, 0), footer_text, font=small_font)
        footer_width = footer_bbox[2] - footer_bbox[0]
        footer_x = (1200 - footer_width) // 2
        draw.text((footer_x, 1700), footer_text, fill=BLACKBOARD_PALETTE["chalk_orange"], font=small_font)
        
        # Save image
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%H%M%S")
        filename = f"{post_type.lower()}_{TODAY}_{timestamp}.png"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        img.save(filepath, "PNG")
        logger.info(f"✓ Blackboard image generated: {filename}")
        return filepath
        
    except Exception as e:
        logger.error(f"Error generating blackboard image: {e}")
        return None


def generate_and_save_image(post_content: str, post_type: str) -> str:
    """
    Generate and save image based on post content.
    
    Args:
        post_content: The post text
        post_type: Type of post (Carousel, Infographic, Motivation)
    
    Returns:
        Path to saved image, or None if generation failed
    """
    return generate_blackboard_image(post_content, post_type)


if __name__ == "__main__":
    # Test image generation
    test_content = "AI is transforming education through personalized learning paths and adaptive systems that adapt to each student's needs."
    result = generate_and_save_image(test_content, "Infographic")
    if result:
        print(f"✓ Test image generated: {result}")
    else:
        print("✗ Test image generation failed")
