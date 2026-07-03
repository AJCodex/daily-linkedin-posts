#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate high-quality visual images for carousel and infographic posts.
Uses Matplotlib for infographics and HTML+Playwright for carousel slides.

This replaces PIL-based generation with professional, GitHub Actions-safe methods.
"""

import sys
import json
import os
import re
import asyncio
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from PIL import Image
import textwrap

# Add project root to Python path (for GitHub Actions)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from config.logger import get_logger

logger = get_logger(__name__)

try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    logger.warning("Playwright not available - will use PIL fallback")

# ============================================================================
# Configuration
# ============================================================================

CAROUSEL_IMAGE_SIZE = (1200, 1500)
INFOGRAPHIC_IMAGE_SIZE = (1200, 1800)
OUTPUT_DIR = "output/posts_generated_images"

# Professional color palette
COLORS = {
    "primary": "#0A66C2",      # LinkedIn blue
    "accent1": "#1A73E8",       # Google blue
    "accent2": "#4285F4",       # Light blue
    "accent3": "#34A853",       # Google green
    "accent4": "#EA4335",       # Google red
    "accent5": "#FBBC04",       # Google yellow
    "accent6": "#9C27B0",       # Purple
    "accent7": "#FF6D00",       # Orange
    "text_dark": "#202124",
    "text_light": "#FFFFFF",
    "bg_light": "#F8F9FA",
    "bg_dark": "#202124"
}

PALETTE = [COLORS["primary"], COLORS["accent1"], COLORS["accent2"], 
           COLORS["accent3"], COLORS["accent4"], COLORS["accent5"],
           COLORS["accent6"], COLORS["accent7"]]

# ============================================================================
# Carousel: HTML + Playwright Rendering
# ============================================================================

def parse_carousel_slides(carousel_text):
    """Parse carousel text into individual slides."""
    slides = []
    slide_pattern = r'(?:Slide\s+\d+[\s:—\-]+)(.*?)(?=Slide\s+\d+|$)'
    matches = re.findall(slide_pattern, carousel_text, re.IGNORECASE | re.DOTALL)
    
    for i, slide_content in enumerate(matches, 1):
        title_match = re.match(r'([^—\n]+)(?:—|—|:)?(.*)', slide_content, re.DOTALL)
        if title_match:
            title = title_match.group(1).strip()[:80]
            content = title_match.group(2).strip()[:300]
        else:
            title = f"Slide {i}"
            content = slide_content.strip()[:300]
        
        slides.append({
            "number": i,
            "title": title,
            "content": content
        })
    
    return slides if slides else [{"number": 1, "title": "Slide 1", "content": carousel_text[:200]}]

def create_carousel_html(slides):
    """Create professional HTML for carousel slides."""
    
    html_slides = ""
    
    for i, slide in enumerate(slides):
        slide_num = slide["number"]
        title = slide["title"]
        content = slide["content"]
        
        # Alternate colors for visual interest
        bg_color = PALETTE[i % len(PALETTE)]
        text_color = COLORS["text_light"]
        
        html_slides += f"""
        <div class="slide" style="background: linear-gradient(135deg, {bg_color} 0%, {lighten_color(bg_color, 20)} 100%);">
            <div class="slide-header">
                <div class="slide-number">{slide_num}/{len(slides)}</div>
                <h2 class="slide-title">{title}</h2>
            </div>
            <div class="slide-content">
                <p>{content}</p>
            </div>
            <div class="slide-footer">
                <span class="footer-text">LinkedIn AI Insights</span>
            </div>
        </div>
        """
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                background: #f0f0f0;
            }}
            
            .carousel-container {{
                width: {CAROUSEL_IMAGE_SIZE[0]}px;
                height: {CAROUSEL_IMAGE_SIZE[1]}px;
                display: flex;
                align-items: center;
                justify-content: center;
                background: white;
            }}
            
            .slide {{
                width: {CAROUSEL_IMAGE_SIZE[0]}px;
                height: {CAROUSEL_IMAGE_SIZE[1]}px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                padding: 60px;
                color: white;
                font-weight: 500;
                background-size: cover;
                background-position: center;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
            }}
            
            .slide-header {{
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                margin-bottom: 30px;
            }}
            
            .slide-number {{
                background: rgba(255,255,255,0.25);
                padding: 8px 16px;
                border-radius: 20px;
                font-size: 14px;
                font-weight: 700;
                backdrop-filter: blur(10px);
            }}
            
            .slide-title {{
                font-size: 48px;
                font-weight: 700;
                line-height: 1.2;
                max-width: 80%;
                text-align: right;
                margin-top: -10px;
            }}
            
            .slide-content {{
                flex: 1;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            
            .slide-content p {{
                font-size: 24px;
                line-height: 1.6;
                text-align: center;
                max-width: 90%;
                font-weight: 400;
            }}
            
            .slide-footer {{
                text-align: center;
                font-size: 14px;
                opacity: 0.8;
            }}
        </style>
    </head>
    <body>
        <div class="carousel-container">
            {html_slides}
        </div>
    </body>
    </html>
    """
    
    return html

def lighten_color(hex_color, percent):
    """Lighten a hex color by a percentage."""
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    r = min(255, int(r + (255 - r) * percent / 100))
    g = min(255, int(g + (255 - g) * percent / 100))
    b = min(255, int(b + (255 - b) * percent / 100))
    return f'#{r:02x}{g:02x}{b:02x}'

async def render_carousel_with_playwright(html_content, output_path):
    """Render HTML carousel to PNG using Playwright."""
    
    async with async_playwright() as p:
        # Launch browser (headless)
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": CAROUSEL_IMAGE_SIZE[0], "height": CAROUSEL_IMAGE_SIZE[1]})
        
        # Set HTML content
        await page.set_content(html_content)
        
        # Take screenshot
        await page.screenshot(path=output_path, full_page=False)
        
        await browser.close()

def create_carousel_image(slides):
    """Create carousel image using Playwright."""
    
    if not PLAYWRIGHT_AVAILABLE:
        print("[!] Playwright not available, using PIL fallback...")
        return create_carousel_image_pil(slides)
    
    html = create_carousel_html(slides)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = f"{OUTPUT_DIR}/carousel_{timestamp}.png"
    
    try:
        # Run async Playwright rendering
        asyncio.run(render_carousel_with_playwright(html, image_path))
        print(f"[+] Created carousel image: {image_path}")
        return image_path
    except Exception as e:
        print(f"[!] Playwright rendering failed: {e}, using PIL fallback...")
        return create_carousel_image_pil(slides)

def create_carousel_image_pil(slides):
    """Fallback PIL-based carousel (if Playwright fails)."""
    
    from PIL import ImageDraw, ImageFont
    
    img = Image.new('RGB', CAROUSEL_IMAGE_SIZE, color=COLORS["bg_light"])
    draw = ImageDraw.Draw(img)
    
    try:
        title_font = ImageFont.truetype("arial.ttf", 48)
        text_font = ImageFont.truetype("arial.ttf", 28)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
    
    # Header
    draw.rectangle([(0, 0), (CAROUSEL_IMAGE_SIZE[0], 120)], fill=COLORS["primary"])
    draw.text((60, 35), "AI Career Roadmap - Carousel", fill=COLORS["text_light"], font=title_font)
    
    # Content
    y = 180
    for i, slide in enumerate(slides[:4]):
        color = PALETTE[i % len(PALETTE)]
        draw.rectangle([(60, y), (CAROUSEL_IMAGE_SIZE[0]-60, y+70)], fill=color)
        draw.text((80, y+15), f"Slide {slide['number']}: {slide['title'][:40]}", 
                 fill=COLORS["text_light"], font=text_font)
        y += 100
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = f"{OUTPUT_DIR}/carousel_{timestamp}.png"
    img.save(image_path)
    print(f"[+] Created carousel image (PIL): {image_path}")
    return image_path

# ============================================================================
# Infographic: Matplotlib Data Visualization
# ============================================================================

def parse_infographic_data(infographic_text):
    """Parse infographic text into structured data."""
    
    lines = infographic_text.split('\n')
    title = lines[0] if lines else "Infographic"
    
    data_points = []
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        
        # Parse "Label: Value" or "Label - Value" or "- Label: Value"
        if ':' in line:
            parts = line.split(':', 1)
            label = parts[0].replace('-', '').strip()
            value = parts[1].strip()
        elif '-' in line:
            parts = line.split('-', 1)
            label = parts[0].strip()
            value = parts[1].strip()
        else:
            label = line.replace('-', '').strip()
            value = ""
        
        if label and len(label) < 100:
            data_points.append({"label": label, "value": value})
    
    return title, data_points[:8]

def create_infographic_image(title, data_points):
    """Create professional infographic using Matplotlib."""
    
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(12, 18), dpi=100)
    fig.patch.set_facecolor('white')
    ax.set_facecolor(COLORS["bg_light"])
    
    # Title
    fig.suptitle(title, fontsize=56, fontweight='bold', y=0.98, color=COLORS["text_dark"])
    
    # Extract values from data points (try to convert to numbers)
    labels = []
    values = []
    
    for i, dp in enumerate(data_points):
        labels.append(dp['label'][:40])
        
        # Try to extract numeric value
        value_str = dp['value'].replace('%', '').replace(',', '').strip()
        try:
            val = float(value_str.split()[0])
        except:
            val = (i + 1) * 10  # Default incremental values
        
        values.append(val)
    
    # Create bar chart
    y_pos = range(len(labels))
    colors_list = PALETTE[:len(labels)]
    
    bars = ax.barh(y_pos, values, color=colors_list, edgecolor='white', linewidth=2)
    
    # Customize chart
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=22, fontweight='bold')
    ax.set_xlabel('Value', fontsize=20, fontweight='bold', color=COLORS["text_dark"])
    ax.set_xlim(0, max(values) * 1.15)
    
    # Add value labels on bars
    for i, (bar, val) in enumerate(zip(bars, values)):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2, 
               f'{val:.0f}%', ha='left', va='center', 
               fontsize=18, fontweight='bold', color=COLORS["text_dark"], 
               bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS["text_light"], alpha=0.8))
    
    # Remove spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(COLORS["accent2"])
    ax.spines['bottom'].set_color(COLORS["accent2"])
    
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    # Footer
    fig.text(0.5, 0.02, 'Microsoft AI Insights | Data-Driven Intelligence', 
            ha='center', fontsize=14, style='italic', color=COLORS["accent2"])
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.96])
    
    # Save
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = f"{OUTPUT_DIR}/infographic_{timestamp}.png"
    
    fig.savefig(image_path, dpi=100, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"[+] Created infographic image: {image_path}")
    return image_path

# ============================================================================
# Main: Process posts
# ============================================================================

def process_visual_posts():
    """Process carousel and infographic posts with enhanced visuals."""
    
    today = datetime.now().strftime("%Y%m%d")
    json_file = f"output/posts_{today}/posts/posts_with_images.json"
    
    if not os.path.exists(json_file):
        print(f"[!] posts_with_images.json not found: {json_file}")
        return
    
    print(f"[>] Reading posts from: {json_file}")
    
    with open(json_file, 'r', encoding='utf-8') as f:
        posts = json.load(f)
    
    updated = False
    
    for post in posts:
        post_type = post.get("type", "")
        content = post.get("content", "")
        
        # Carousel posts
        if "Carousel" in post_type:
            print(f"\n[>] Processing carousel post...")
            slides = parse_carousel_slides(content)
            print(f"    Found {len(slides)} slides")
            image_path = create_carousel_image(slides)
            
            post["image_url"] = f"file://{os.path.abspath(image_path)}"
            post["generated_image"] = image_path
            post["is_generated"] = True
            updated = True
        
        # Infographic posts
        elif "Infographic" in post_type:
            print(f"\n[>] Processing infographic post...")
            title, data_points = parse_infographic_data(content)
            print(f"    Found {len(data_points)} data points")
            image_path = create_infographic_image(title, data_points)
            
            post["image_url"] = f"file://{os.path.abspath(image_path)}"
            post["generated_image"] = image_path
            post["is_generated"] = True
            updated = True
    
    # Save updated posts
    if updated:
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)
        print(f"\n[+] Updated posts_with_images.json with generated images")
    
    return posts

if __name__ == "__main__":
    print("=" * 60)
    print("Generating Enhanced Visual Images")
    print("=" * 60)
    print()
    
    process_visual_posts()
