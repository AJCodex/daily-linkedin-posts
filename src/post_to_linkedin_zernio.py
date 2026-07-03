#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Post generated LinkedIn posts to LinkedIn via Zernio API with multimedia support.

Security:
  - Validates all URLs
  - API keys from .env only
  - No sensitive data in logs
  - Handles 409 duplicates gracefully
  - Retries with exponential backoff
"""

import sys
import os
import json
import datetime
import re
import base64

# Add project root to Python path (for GitHub Actions)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from config.logger import get_logger
from config.utils import api_request_with_retry, validate_api_key, validate_url, safe_json_load
from config.constants import (
    TODAY, ZERNIO_BASE_URL, ZERNIO_TIMEOUT_SEC,
    SCHEDULING, POST_TYPES, GITHUB_IMAGES_BASE
)
from dotenv import load_dotenv

load_dotenv()
logger = get_logger(__name__)

# Load from environment (with validation)
LINKEDIN_ACCOUNT_ID = os.getenv("LINKEDIN_ACCOUNT_ID", "")
ZERNIO_API_KEY = os.getenv("ZERNIO_API_KEY", "")
ZERNIO_ENDPOINT = f"{ZERNIO_BASE_URL}/posts"


def file_url_to_base64(file_url: str) -> str:
    """
    Convert file:// URL to base64 data URL for LinkedIn posting.
    
    Args:
        file_url: file:// URL path to local image
        
    Returns:
        data:image/png;base64,... data URL, or empty string on failure
    """
    try:
        # Extract file path from file:// URL
        file_path = file_url.replace("file://", "").strip()
        
        # Make sure file exists
        if not os.path.exists(file_path):
            logger.warning(f"Image file not found: {file_path}")
            return ""
        
        # Determine image type
        if file_path.lower().endswith(".png"):
            mime_type = "image/png"
        elif file_path.lower().endswith(".jpg") or file_path.lower().endswith(".jpeg"):
            mime_type = "image/jpeg"
        elif file_path.lower().endswith(".gif"):
            mime_type = "image/gif"
        else:
            mime_type = "image/png"  # Default to PNG
        
        # Read file and encode to base64
        with open(file_path, "rb") as f:
            image_data = f.read()
            b64_data = base64.b64encode(image_data).decode("utf-8")
            
        data_url = f"data:{mime_type};base64,{b64_data}"
        logger.debug(f"Converted local image to base64: {os.path.basename(file_path)} ({len(image_data)} bytes)")
        return data_url
        
    except Exception as e:
        logger.error(f"Failed to convert file to base64: {e}")
        return ""


def validate_configuration() -> bool:
    """Validate all required configuration is present."""
    
    try:
        validate_api_key(ZERNIO_API_KEY, "ZERNIO_API_KEY")
        validate_api_key(LINKEDIN_ACCOUNT_ID, "LINKEDIN_ACCOUNT_ID")
        logger.debug("✓ Configuration validated")
        return True
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return False


def extract_posts_from_file() -> list:
    """
    Extract posts with images from multimedia JSON file.
    Falls back to text file if JSON not found.
    Converts file:// URLs to base64 data URLs for Zernio API.
    """
    
    # Try JSON file (has images)
    json_file = f"output/posts_{TODAY}/posts/posts_with_images.json"
    
    if os.path.exists(json_file):
        logger.info(f"Reading posts with images from: {json_file}")
        
        posts_data = safe_json_load(json_file, "Load posts with images")
        if not posts_data:
            logger.warning("Failed to load JSON, trying text file")
        else:
            posts = []
            for post in posts_data:
                image_url = post.get("image_url", "")
                
                # Convert file:// URLs to base64 data URLs
                if image_url.startswith("file://"):
                    logger.debug(f"Converting local file to base64 data URL...")
                    image_url = file_url_to_base64(image_url)
                    if image_url:
                        logger.info(f"✓ Local image converted to base64 ({len(image_url)//1000} KB)")
                
                # SECURITY: Validate URL (skip for base64 data URLs)
                if image_url and not image_url.startswith("data:") and not validate_url(image_url):
                    logger.warning(f"Invalid image URL, skipping: {image_url[:50]}")
                    image_url = ""
                
                posts.append({
                    "stream": post.get("stream"),
                    "type": post.get("type", "Text"),
                    "content": post.get("content", ""),
                    "image_url": image_url,
                    "source": post.get("source", "")
                })
            
            logger.info(f"✓ Extracted {len(posts)} posts with images")
            return posts
    
    # Fallback: Read from text file (no images)
    text_file = f"linkedin_posts_{TODAY}.txt"
    if os.path.exists(text_file):
        logger.info(f"Fallback: Reading from text file: {text_file}")
        
        try:
            with open(text_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse posts using stream markers
            pattern = r"STREAM (\d+) — (.+?)\n=+\n(.+?)(?:={60}|$)"
            matches = re.findall(pattern, content, re.DOTALL)
            
            posts = []
            for stream, post_type, post_content in matches:
                posts.append({
                    "stream": int(stream),
                    "type": post_type.strip(),
                    "content": post_content.strip(),
                    "image_url": "",
                    "source": "Text File"
                })
            
            logger.info(f"✓ Extracted {len(posts)} posts from text file")
            return posts
        
        except Exception as e:
            logger.error(f"Failed to parse text file: {e}")
            return []
    
    logger.error(f"No posts file found ({json_file} or {text_file})")
    return []


def post_to_linkedin(post_data: dict) -> dict:
    """
    Post to LinkedIn via Zernio API with retry logic.
    
    Args:
        post_data: Dictionary with 'content', 'type', 'image_url', 'stream'
        
    Returns:
        Result dictionary with success status and details
    """
    
    stream_num = post_data.get("stream", 0)
    post_type = post_data.get("type", "Text")
    content = post_data.get("content", "")
    image_url = post_data.get("image_url", "")
    
    # SECURITY: Validate content length
    if not content or len(content) > 3000:
        logger.error(f"Post {stream_num}: Invalid content length")
        return {"success": False, "error": "Invalid content", "stream": stream_num}
    
    # SECURITY: Validate URL if present (skip validation for data URLs)
    if image_url and not image_url.startswith("data:") and not validate_url(image_url):
        logger.warning(f"Post {stream_num}: Invalid image URL, posting without image")
        image_url = ""
    
    # Build platform configuration
    platform_config = {
        "platform": "linkedin",
        "accountId": LINKEDIN_ACCOUNT_ID,
    }
    
    # Add scheduling if specified for this post type
    schedule_hour = SCHEDULING.get(stream_num)
    if schedule_hour is not None:
        today = datetime.date.today()
        scheduled_time = datetime.datetime.combine(
            today,
            datetime.time(schedule_hour, 0, 0)
        )
        platform_config["scheduledFor"] = scheduled_time.isoformat() + "Z"
        platform_config["publishNow"] = False
        publish_status = f"scheduled for {schedule_hour}:00"
    else:
        platform_config["publishNow"] = True
        publish_status = "posting now"
    
    # Build Zernio API payload
    payload = {
        "content": content,
        "platforms": [platform_config]
    }
    
    # Add image if present
    if image_url:
        payload["media"] = [{"type": "image", "url": image_url}]
        image_info = "with image" if image_url.startswith("data:") else f"with image: {image_url[:60]}..."
    else:
        image_info = "without image"
    
    # Build headers (SECURITY: no sensitive data in logs)
    headers = {
        "Authorization": f"Bearer {ZERNIO_API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "Daily LinkedIn Posts Pipeline"
    }
    
    logger.info(f"\n[{stream_num}] Posting {post_type} ({publish_status}) {image_info}")
    
    try:
        # Make API request with retry logic
        result = api_request_with_retry(
            "POST",
            ZERNIO_ENDPOINT,
            headers,
            payload,
            ZERNIO_TIMEOUT_SEC,
            f"Post #{stream_num} ({post_type})"
        )
        
        if not result:
            return {"success": False, "error": "No response", "stream": stream_num}
        
        # Check for errors
        if "error" in result:
            error_msg = result.get("error", "Unknown error")
            status_code = result.get("status_code", "")
            
            if status_code == 409:
                logger.info(f"[{stream_num}] ✓ Conflict (409) - Content already posted (duplicate protection)")
                return {"success": False, "error": "409 Duplicate", "stream": stream_num}
            else:
                logger.error(f"[{stream_num}] ✗ Error: {error_msg}")
                return {"success": False, "error": error_msg, "stream": stream_num}
        
        # Success
        post_id = result.get("post", {}).get("_id", "unknown")
        scheduled_for = result.get("post", {}).get("scheduledFor", "")
        
        logger.info(f"[{stream_num}] ✓ Posted successfully! ID: {post_id}")
        if scheduled_for:
            logger.info(f"      Scheduled for: {scheduled_for}")
        
        return {
            "success": True,
            "post_id": post_id,
            "stream": stream_num,
            "type": post_type,
            "scheduled_for": scheduled_for,
            "has_image": bool(image_url),
            "timestamp": datetime.datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"[{stream_num}] ✗ Failed to post: {str(e)[:100]}")
        return {
            "success": False,
            "error": str(e)[:100],
            "stream": stream_num
        }


def save_posting_log(results: list) -> None:
    """Save posting results to JSON log file."""
    
    log_file = f"linkedin_posting_log_{TODAY}.json"
    
    try:
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": datetime.datetime.now().isoformat(),
                "total": len(results),
                "successful": sum(1 for r in results if r.get("success")),
                "posts": results
            }, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✓ Posting log saved: {log_file}")
    
    except Exception as e:
        logger.error(f"Failed to save posting log: {e}")


def main():
    """Main entry point."""
    logger.info("=" * 80)
    logger.info("STEP 3/3: Posting to LinkedIn via Zernio")
    logger.info("=" * 80)
    
    # Validate configuration
    if not validate_configuration():
        logger.error("Configuration validation failed")
        return 1
    
    # Extract posts
    posts = extract_posts_from_file()
    if not posts:
        logger.error("No posts found")
        return 1
    
    # Post each post
    logger.info(f"\nPosting {len(posts)} posts...\n")
    results = []
    
    for post in posts:
        result = post_to_linkedin(post)
        results.append(result)
    
    # Summary
    successful = sum(1 for r in results if r.get("success"))
    logger.info("\n" + "=" * 80)
    logger.info(f"SUMMARY: {successful}/{len(results)} posts successful")
    logger.info("=" * 80)
    
    # Save log
    save_posting_log(results)
    
    logger.info("\n✓ Step 3 complete! All posts posted/scheduled to LinkedIn.")
    
    return 0 if successful > 0 else 1


if __name__ == "__main__":
    exit(main())
