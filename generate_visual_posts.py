#!/usr/bin/env python3
"""
Generate visual images for carousel and infographic posts.
Converts text-based carousel/infographic content into actual images.

This enhances Phase 2 (Carousel) and Phase 3 (Infographic) multimedia support.
"""

import json
import os
import re
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import textwrap

# ============================================================================
# Configuration
# ============================================================================

CAROUSEL_IMAGE_SIZE = (1200, 1500)  # LinkedIn carousel slide size
INFOGRAPHIC_IMAGE_SIZE = (1200, 1800)  # LinkedIn infographic size
OUTPUT_DIR = "output/posts_generated_images"

# Colors
COLOR_PRIMARY = "#0A66C2"  # LinkedIn blue
COLOR_SECONDARY = "#F1F2F2"  # Light gray
COLOR_TEXT_DARK = "#000000"
COLOR_TEXT_LIGHT = "#FFFFFF"
COLOR_ACCENT = "#E7E5E1"

# ============================================================================
# Carousel Image Generation
# ============================================================================

def parse_carousel_slides(carousel_text):
    """
    Parse carousel text into individual slides.
    Format: "Slide 1: Title\nSlide 2: Content..." etc.
    """
    slides = []
    # Match patterns like "Slide 1:" or "Slide 1 —"
    slide_pattern = r'(?:Slide\s+\d+[\s:—\-]+)(.*?)(?=Slide\s+\d+|$)'
    matches = re.findall(slide_pattern, carousel_text, re.IGNORECASE | re.DOTALL)
    
    for i, slide_content in enumerate(matches, 1):
        slides.append({
            "number": i,
            "content": slide_content.strip()[:200]  # Limit content
        })
    
    return slides if slides else [{"number": 1, "content": carousel_text[:200]}]

def create_carousel_composite_image(slides):
    """
    Create a composite image showing all carousel slides.
    Returns file path to generated image.
    """
    
    # Create composite image
    img = Image.new('RGB', CAROUSEL_IMAGE_SIZE, color=COLOR_SECONDARY)
    draw = ImageDraw.Draw(img)
    
    # Try to use system fonts, fallback to default
    try:
        title_font = ImageFont.truetype("arial.ttf", 48)
        slide_font = ImageFont.truetype("arial.ttf", 32)
        small_font = ImageFont.truetype("arial.ttf", 24)
    except:
        title_font = ImageFont.load_default()
        slide_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Draw header
    draw.rectangle([(0, 0), (CAROUSEL_IMAGE_SIZE[0], 150)], fill=COLOR_PRIMARY)
    draw.text((60, 50), "📊 Carousel: Multi-Slide Deep Dive", fill=COLOR_TEXT_LIGHT, font=title_font)
    
    y_position = 180
    
    # Draw slides preview
    for slide in slides[:5]:  # Show first 5 slides
        # Slide number box
        draw.rectangle(
            [(60, y_position), (120, y_position + 50)],
            fill=COLOR_PRIMARY,
            outline=COLOR_ACCENT,
            width=2
        )
        draw.text(
            (75, y_position + 10),
            f"Slide {slide['number']}",
            fill=COLOR_TEXT_LIGHT,
            font=small_font
        )
        
        # Slide content preview
        content_preview = slide['content'][:100]
        wrapped_text = textwrap.fill(content_preview, width=60)
        draw.text(
            (150, y_position + 10),
            wrapped_text,
            fill=COLOR_TEXT_DARK,
            font=small_font
        )
        
        y_position += 180
    
    # Draw footer with slide count
    draw.rectangle([(0, CAROUSEL_IMAGE_SIZE[1] - 80), (CAROUSEL_IMAGE_SIZE[0], CAROUSEL_IMAGE_SIZE[1])], fill=COLOR_PRIMARY)
    draw.text(
        (60, CAROUSEL_IMAGE_SIZE[1] - 50),
        f"🎯 {len(slides)} slides • Swipe to explore",
        fill=COLOR_TEXT_LIGHT,
        font=slide_font
    )
    
    # Save image
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = f"{OUTPUT_DIR}/carousel_{timestamp}.png"
    img.save(image_path)
    print(f"✅ Created carousel image: {image_path}")
    return image_path

# ============================================================================
# Infographic Image Generation
# ============================================================================

def parse_infographic_data(infographic_text):
    """
    Parse infographic text into title and data points.
    Format: "Title\n- Point 1\n- Point 2..." or "Title\nPoint 1: value\nPoint 2: value..."
    """
    lines = infographic_text.split('\n')
    
    title = lines[0] if lines else "Infographic"
    
    data_points = []
    for line in lines[1:]:
        line = line.strip()
        if line and (line.startswith('-') or ':' in line):
            # Remove leading dash or format "Label: Value"
            if line.startswith('-'):
                point = line[1:].strip()
            else:
                point = line
            
            if point and len(point) < 150:  # Reasonable length
                data_points.append(point)
    
    return title, data_points[:8]  # Limit to 8 points

def create_infographic_image(title, data_points):
    """
    Create a professional infographic image.
    Returns file path to generated image.
    """
    
    img = Image.new('RGB', INFOGRAPHIC_IMAGE_SIZE, color=COLOR_SECONDARY)
    draw = ImageDraw.Draw(img)
    
    # Try to use system fonts
    try:
        title_font = ImageFont.truetype("arial.ttf", 56)
        heading_font = ImageFont.truetype("arial.ttf", 40)
        text_font = ImageFont.truetype("arial.ttf", 28)
        small_font = ImageFont.truetype("arial.ttf", 20)
    except:
        title_font = ImageFont.load_default()
        heading_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Draw header with title
    draw.rectangle([(0, 0), (INFOGRAPHIC_IMAGE_SIZE[0], 180)], fill=COLOR_PRIMARY)
    draw.text((60, 50), "📈 " + title[:60], fill=COLOR_TEXT_LIGHT, font=title_font)
    
    # Draw data points in a grid-like layout
    y_position = 220
    colors = [COLOR_PRIMARY, "#1A73E8", "#4285F4", "#34A853", "#EA4335", "#FBBC04", "#9C27B0", "#FF6D00"]
    
    for i, point in enumerate(data_points):
        # Colored box for each point
        color = colors[i % len(colors)]
        draw.rectangle(
            [(60, y_position), (INFOGRAPHIC_IMAGE_SIZE[0] - 60, y_position + 120)],
            fill=color,
            outline=COLOR_ACCENT,
            width=2
        )
        
        # Draw point text
        wrapped_point = textwrap.fill(point, width=80)
        draw.text(
            (80, y_position + 20),
            wrapped_point,
            fill=COLOR_TEXT_LIGHT,
            font=text_font
        )
        
        y_position += 150
    
    # Draw footer
    draw.rectangle([(0, INFOGRAPHIC_IMAGE_SIZE[1] - 80), (INFOGRAPHIC_IMAGE_SIZE[0], INFOGRAPHIC_IMAGE_SIZE[1])], fill=COLOR_PRIMARY)
    draw.text(
        (60, INFOGRAPHIC_IMAGE_SIZE[1] - 50),
        "Microsoft AI • Data-Driven Insights",
        fill=COLOR_TEXT_LIGHT,
        font=text_font
    )
    
    # Save image
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = f"{OUTPUT_DIR}/infographic_{timestamp}.png"
    img.save(image_path)
    print(f"✅ Created infographic image: {image_path}")
    return image_path

# ============================================================================
# Main: Process posts_with_images.json
# ============================================================================

def process_visual_posts():
    """
    Read posts_with_images.json and generate carousel/infographic images.
    Update image URLs for carousel and infographic posts.
    """
    
    today = datetime.now().strftime("%Y%m%d")
    json_file = f"output/posts_{today}/posts/posts_with_images.json"
    
    if not os.path.exists(json_file):
        print(f"❌ posts_with_images.json not found: {json_file}")
        return
    
    print(f"📖 Reading posts from: {json_file}")
    
    with open(json_file, 'r', encoding='utf-8') as f:
        posts = json.load(f)
    
    # Process each post
    updated = False
    for post in posts:
        post_type = post.get("type", "")
        content = post.get("content", "")
        
        # Phase 2: Carousel posts
        if "Carousel" in post_type or "carousel" in post_type:
            print(f"\n🎬 Processing carousel post...")
            slides = parse_carousel_slides(content)
            print(f"   Found {len(slides)} slides")
            image_path = create_carousel_composite_image(slides)
            
            # Update posts with local image path or Unsplash fallback
            post["image_url"] = f"file://{os.path.abspath(image_path)}"
            post["generated_image"] = image_path
            post["is_generated"] = True
            updated = True
        
        # Phase 3: Infographic posts
        elif "Infographic" in post_type or "infographic" in post_type:
            print(f"\n📊 Processing infographic post...")
            title, data_points = parse_infographic_data(content)
            print(f"   Found {len(data_points)} data points")
            image_path = create_infographic_image(title, data_points)
            
            # Update posts with local image path
            post["image_url"] = f"file://{os.path.abspath(image_path)}"
            post["generated_image"] = image_path
            post["is_generated"] = True
            updated = True
    
    # Save updated posts
    if updated:
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Updated posts_with_images.json with generated images")
    else:
        print(f"\nℹ️  No carousel/infographic posts found to update")
    
    return posts

if __name__ == "__main__":
    print("=" * 60)
    print("Generating Visual Images for Carousel & Infographic Posts")
    print("=" * 60)
    print()
    
    process_visual_posts()
    
    print("\n" + "=" * 60)
    print("✅ Phase 2 & 3 Visual Generation Complete")
    print("=" * 60)
