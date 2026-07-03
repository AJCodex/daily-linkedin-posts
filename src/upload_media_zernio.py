#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Upload media files to Zernio using presigned URL flow.

Zernio media upload process:
  1. Get presigned URL from /v1/media/presign
  2. Upload file directly to presigned URL
  3. Use publicUrl in post's mediaItems field

Security:
  - API keys from .env only
  - Validates file existence and size
  - No sensitive data in logs
"""

import sys
import os
import requests
import json
from pathlib import Path

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from config.logger import get_logger
from config.utils import api_request_with_retry, validate_api_key
from config.constants import ZERNIO_BASE_URL, ZERNIO_TIMEOUT_SEC
from dotenv import load_dotenv

load_dotenv()
logger = get_logger(__name__)

ZERNIO_API_KEY = os.getenv("ZERNIO_API_KEY", "")
MEDIA_PRESIGN_ENDPOINT = f"{ZERNIO_BASE_URL}/media/presign"

# Media size limits
MAX_FILE_SIZE = 5 * 1024 * 1024 * 1024  # 5 GB


def get_media_presigned_url(file_path: str, content_type: str = "image/jpeg") -> dict:
    """
    Step 1: Get presigned URL from Zernio.
    
    Args:
        file_path: Path to file to upload
        content_type: MIME type (image/jpeg, image/png, video/mp4, etc.)
        
    Returns:
        Dict with uploadUrl, publicUrl, key, expiresIn
    """
    
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return {}
    
    file_size = os.path.getsize(file_path)
    if file_size > MAX_FILE_SIZE:
        logger.error(f"File too large: {file_size} bytes (max {MAX_FILE_SIZE})")
        return {}
    
    filename = os.path.basename(file_path)
    
    payload = {
        "filename": filename,
        "contentType": content_type
    }
    
    headers = {
        "Authorization": f"Bearer {ZERNIO_API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "Daily LinkedIn Posts Pipeline"
    }
    
    logger.info(f"Requesting presigned URL for: {filename} ({file_size} bytes)")
    
    try:
        response = requests.post(
            MEDIA_PRESIGN_ENDPOINT,
            json=payload,
            headers=headers,
            timeout=ZERNIO_TIMEOUT_SEC
        )
        response.raise_for_status()
        
        result = response.json()
        logger.debug(f"Presigned URL response: {json.dumps({k: (v[:50] + '...' if len(str(v)) > 50 else v) for k, v in result.items()})}")
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to get presigned URL: {e}")
        return {}


def upload_file_to_presigned_url(file_path: str, upload_url: str, content_type: str = "image/jpeg") -> bool:
    """
    Step 2: Upload file directly to presigned URL.
    
    Args:
        file_path: Path to file
        upload_url: Presigned upload URL
        content_type: MIME type
        
    Returns:
        True if successful, False otherwise
    """
    
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return False
    
    file_size = os.path.getsize(file_path)
    filename = os.path.basename(file_path)
    
    logger.info(f"Uploading file: {filename} ({file_size} bytes)")
    
    try:
        with open(file_path, 'rb') as f:
            response = requests.put(
                upload_url,
                data=f,
                headers={"Content-Type": content_type},
                timeout=ZERNIO_TIMEOUT_SEC
            )
        
        if response.status_code in [200, 204]:
            logger.info(f"✓ File uploaded successfully: {filename}")
            return True
        else:
            logger.error(f"Upload failed with status {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Failed to upload file: {e}")
        return False


def upload_media(file_path: str, content_type: str = None) -> dict:
    """
    Complete media upload flow: presign → upload → get publicUrl.
    
    Args:
        file_path: Path to file to upload
        content_type: MIME type (auto-detected if None)
        
    Returns:
        Dict with publicUrl, uploadUrl, key, or empty dict on failure
    """
    
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return {}
    
    # Auto-detect content type if not provided
    if not content_type:
        file_ext = os.path.splitext(file_path)[1].lower()
        content_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp',
            '.mp4': 'video/mp4',
            '.mov': 'video/quicktime',
            '.avi': 'video/x-msvideo',
            '.webm': 'video/webm',
            '.pdf': 'application/pdf'
        }
        content_type = content_types.get(file_ext, 'application/octet-stream')
    
    filename = os.path.basename(file_path)
    logger.info(f"\n📤 Starting media upload: {filename}")
    
    # Step 1: Get presigned URL
    presign_response = get_media_presigned_url(file_path, content_type)
    if not presign_response:
        logger.error("Failed to get presigned URL")
        return {}
    
    upload_url = presign_response.get("uploadUrl", "")
    public_url = presign_response.get("publicUrl", "")
    
    if not upload_url:
        logger.error("No uploadUrl in presigned response")
        return {}
    
    # Step 2: Upload file
    if not upload_file_to_presigned_url(file_path, upload_url, content_type):
        logger.error("Failed to upload file to presigned URL")
        return {}
    
    # Step 3: Return public URL for use in post
    logger.info(f"✓ Media ready for posting: {public_url[:60]}...")
    
    return {
        "publicUrl": public_url,
        "uploadUrl": upload_url,
        "key": presign_response.get("key", ""),
        "expiresIn": presign_response.get("expiresIn", 0),
        "filename": filename,
        "contentType": content_type
    }


def main():
    """Test media upload (upload a sample image)."""
    
    logger.info("Testing Zernio media upload...")
    
    # Validate API key
    try:
        validate_api_key(ZERNIO_API_KEY, "ZERNIO_API_KEY")
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return 1
    
    # Find a test image file
    test_files = [
        "carousel_20260703_*.png",
        "infographic_20260703_*.png",
        "output/posts_*/images/carousel_*.png"
    ]
    
    found_file = None
    for pattern in test_files:
        from glob import glob
        matches = glob(pattern)
        if matches:
            found_file = matches[0]
            break
    
    if not found_file:
        logger.warning("No test image files found. Create a carousel/infographic first.")
        return 0
    
    logger.info(f"Found test file: {found_file}")
    
    # Upload
    result = upload_media(found_file)
    
    if result:
        logger.info(f"\n✓ Upload successful!")
        logger.info(f"Public URL: {result['publicUrl']}")
        return 0
    else:
        logger.error("Upload failed")
        return 1


if __name__ == "__main__":
    exit(main())
