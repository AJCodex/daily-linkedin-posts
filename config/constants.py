"""
Global constants and configuration for LinkedIn Posts Pipeline.
Centralized config to reduce duplication and ensure consistency.
"""

import os
from datetime import datetime

# ============================================================================
# API Configuration
# ============================================================================

# OpenRouter API (for test content generation)
OPENROUTER_BASE_URL = "https://openrouter.io/api/v1"
OPENROUTER_MODEL = "google/gemma-4-31b-it:free"
OPENROUTER_TIMEOUT = 60

# Zernio API (LinkedIn integration)
ZERNIO_BASE_URL = os.getenv("ZERNIO_BASE_URL", "https://zernio.com/api/v1")
ZERNIO_TIMEOUT = 30

# Unsplash API (image fetching)
UNSPLASH_BASE_URL = "https://source.unsplash.com/1200x630"

# ============================================================================
# Image Generation Configuration
# ============================================================================

CAROUSEL_SIZE = (1200, 1500)
INFOGRAPHIC_SIZE = (1200, 1800)
IMAGE_OUTPUT_DIR = "output/posts_generated_images"
GITHUB_IMAGES_BASE = "https://raw.githubusercontent.com/AJCodex/daily-linkedin-posts/main/images"

# Professional color palette (Google + LinkedIn brand colors)
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

COLOR_PALETTE = [
    COLORS["primary"], COLORS["accent1"], COLORS["accent2"],
    COLORS["accent3"], COLORS["accent4"], COLORS["accent5"],
    COLORS["accent6"], COLORS["accent7"]
]

# ============================================================================
# Post Types
# ============================================================================

POST_TYPES = {
    1: "News",
    2: "Tips & Tricks",
    3: "Carousel",
    4: "Infographic",
    5: "Motivation"
}

SCHEDULING = {
    1: 8,      # News at 8 AM UTC
    2: 16,     # Tips at 4 PM UTC
    3: None,   # Carousel posted now
    4: None,   # Infographic posted now
    5: None    # Motivation posted now
}

# ============================================================================
# Retry Configuration
# ============================================================================

MAX_RETRIES = 3
INITIAL_RETRY_DELAY = 1  # seconds
EXPONENTIAL_BASE = 2

# ============================================================================
# File Paths
# ============================================================================

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_BASE = f"output/posts_{TODAY}"
OUTPUT_POSTS_DIR = f"{OUTPUT_BASE}/posts"
OUTPUT_LOGS_DIR = f"{OUTPUT_BASE}/logs"

# ============================================================================
# Logging Configuration
# ============================================================================

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = f"logs/linkedin_pipeline_{TODAY}.log"
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
