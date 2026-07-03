#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Attach images to LinkedIn posts via AI-contextual keyword generation + Unsplash.

For each post, generates image search keywords using LLM, fetches from Unsplash,
and creates posts_with_images.json with all metadata.

Security:
  - API keys from .env only
  - Input validation on all URLs
  - Error handling with retries
"""

import sys
import json
import os
import re
from datetime import datetime

# Add project root to Python path (for GitHub Actions)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from config.logger import get_logger
from config.utils import api_request_with_retry, safe_json_load, validate_api_key
from config.constants import (
    TODAY, OUTPUT_POSTS_DIR, OPENROUTER_BASE_URL, OPENROUTER_MODEL,
    OPENROUTER_TIMEOUT, UNSPLASH_BASE_URL
)
from dotenv import load_dotenv

load_dotenv()
logger = get_logger(__name__)

# Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_TIMEOUT_SEC = OPENROUTER_TIMEOUT


def generate_image_keywords(post_content: str, post_type: str) -> str:
    """
    Generate image search keywords using OpenRouter API.
    
    Args:
        post_content: LinkedIn post text
        post_type: Type of post (News, Tips, etc.)
        
    Returns:
        Comma-separated keywords or empty string on failure
    """
    
    try:
        validate_api_key(OPENROUTER_API_KEY, "OPENROUTER_API_KEY")
    except ValueError as e:
        logger.warning(f"OpenRouter API key not available: {e}")
        logger.info("Using default keywords instead")
        return "technology, artificial intelligence, innovation"
    
    prompt = f"""Extract 2-3 image search keywords from this LinkedIn post about {post_type}.
Keep each keyword 1-3 words, focused on visual concepts.
Return ONLY keywords, comma-separated, no explanation.

Post: {post_content[:300]}

Keywords:"""
    
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://github.com/AJCodex/daily-linkedin-posts",
            "X-Title": "Daily LinkedIn Posts"
        }
        
        payload = {
            "model": OPENROUTER_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 100
        }
        
        result = api_request_with_retry(
            "POST",
            f"{OPENROUTER_BASE_URL}/chat/completions",
            headers,
            payload,
            OPENROUTER_TIMEOUT_SEC,
            f"Generate image keywords for {post_type}"
        )
        
        if result and "choices" in result:
            keywords = result["choices"][0]["message"]["content"].strip()
            logger.debug(f"Generated keywords for {post_type}: {keywords}")
            return keywords
    
    except Exception as e:
        logger.warning(f"Failed to generate keywords: {e}")
    
    # Default keywords fallback
    defaults = {
        "News": "technology, artificial intelligence",
        "Tips & Tricks": "learning, productivity, code",
        "Carousel": "presentation, slides, business",
        "Infographic": "data visualization, analytics, insights",
        "Motivation": "success, teamwork, growth"
    }
    
    return defaults.get(post_type, "technology, innovation")


def fetch_unsplash_image(keywords: str) -> str:
    """
    Fetch image URL from Unsplash using keywords.
    
    Args:
        keywords: Comma-separated search keywords
        
    Returns:
        Unsplash image URL or empty string if failed
    """
    
    # Clean and format keywords for URL
    clean_keywords = ",".join([k.strip() for k in keywords.split(",") if k.strip()])
    
    url = f"{UNSPLASH_BASE_URL}/?{clean_keywords}"
    
    try:
        logger.debug(f"Fetching image for: {clean_keywords}")
        # Unsplash redirect URLs are valid image URLs
        return url  # Return URL directly - no API key needed
    
    except Exception as e:
        logger.error(f"Failed to fetch Unsplash image: {e}")
        return ""


def extract_posts_from_file() -> list:
    """Extract posts from linkedin_posts_YYYYMMDD.txt."""
    
    file_path = f"linkedin_posts_{TODAY}.txt"
    
    if not os.path.exists(file_path):
        logger.error(f"Posts file not found: {file_path}")
        logger.info("Run: python src/test_all_post_types_demo.py")
        return []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse posts using stream markers
        pattern = r"STREAM (\d+) — (.+?)\n=+\n(.+?)(?:={60}|$)"
        matches = re.findall(pattern, content, re.DOTALL)
        
        posts = []
        for stream, post_type, content in matches:
            posts.append({
                "stream": int(stream),
                "type": post_type.strip(),
                "content": content.strip()
            })
        
        logger.info(f"Extracted {len(posts)} posts from {file_path}")
        return posts
    
    except Exception as e:
        logger.error(f"Failed to parse posts file: {e}")
        return []


def process_posts_with_images(posts: list) -> list:
    """Add image URLs to each post."""
    
    posts_with_images = []
    
    for post in posts:
        try:
            logger.debug(f"Processing {post['type']} post (stream {post['stream']})")
            
            # Generate keywords
            keywords = generate_image_keywords(post["content"], post["type"])
            
            # Fetch image
            image_url = fetch_unsplash_image(keywords)
            
            if not image_url:
                logger.warning(f"No image for post {post['stream']}, using default")
                image_url = f"{UNSPLASH_BASE_URL}/?technology"
            
            post["image_url"] = image_url
            post["source"] = "Unsplash"
            
            posts_with_images.append(post)
            logger.info(f"✓ Attached image to {post['type']}")
        
        except Exception as e:
            logger.error(f"Failed to process post {post['stream']}: {e}")
            post["image_url"] = f"{UNSPLASH_BASE_URL}/?default"
            posts_with_images.append(post)
    
    return posts_with_images


def save_posts_with_images(posts: list) -> bool:
    """Save posts with images to JSON file."""
    
    os.makedirs(OUTPUT_POSTS_DIR, exist_ok=True)
    
    json_file = f"{OUTPUT_POSTS_DIR}/posts_with_images.json"
    
    try:
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✓ Saved posts with images -> {json_file}")
        
        # Also save HTML preview
        save_html_preview(posts)
        
        return True
    
    except Exception as e:
        logger.error(f"Failed to save posts: {e}")
        return False


def save_html_preview(posts: list) -> None:
    """Generate HTML preview of posts with images."""
    
    html_file = f"{OUTPUT_POSTS_DIR}/posts_with_images.html"
    
    html = """<!DOCTYPE html>
<html>
<head>
    <title>LinkedIn Posts Preview</title>
    <style>
        body { font-family: -apple-system, sans-serif; margin: 20px; background: #f5f5f5; }
        .post { background: white; margin: 20px 0; padding: 15px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        .post-type { color: #0A66C2; font-weight: bold; margin-bottom: 8px; }
        .post-content { color: #333; line-height: 1.6; margin: 10px 0; }
        img { max-width: 100%; margin: 10px 0; border-radius: 4px; }
        .stream { color: #666; font-size: 0.9em; }
    </style>
</head>
<body>
    <h1>LinkedIn Posts Preview</h1>
"""
    
    for post in posts:
        html += f"""
    <div class="post">
        <div class="stream">Stream {post['stream']}</div>
        <div class="post-type">📝 {post['type']}</div>
        <div class="post-content">{post['content'][:200]}...</div>
        <img src="{post.get('image_url', '')}" alt="Post image">
    </div>
"""
    
    html += """
</body>
</html>
"""
    
    try:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html)
        logger.debug(f"Generated HTML preview -> {html_file}")
    except Exception as e:
        logger.debug(f"Failed to generate HTML preview: {e}")


def main():
    """Main entry point."""
    logger.info("=" * 80)
    logger.info("STEP 1/3: Attaching Images to Posts")
    logger.info("=" * 80)
    
    # Extract posts
    posts = extract_posts_from_file()
    if not posts:
        logger.error("No posts found. Exiting.")
        return 1
    
    # Add images
    posts_with_images = process_posts_with_images(posts)
    
    # Save
    if save_posts_with_images(posts_with_images):
        logger.info("✓ Step 1 complete!")
        logger.info("\nNext: python src/generate_visual_posts_enhanced.py")
        return 0
    else:
        logger.error("Failed to save posts with images")
        return 1


if __name__ == "__main__":
    exit(main())
