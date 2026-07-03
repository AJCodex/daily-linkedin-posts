#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Daily Posts Pipeline - Main Entry Point.

Complete end-to-end pipeline for generating and posting AI-focused content to LinkedIn.

Pipeline Stages:
  1. Generate test posts (or use OpenRouter API for production)
  2. Attach Unsplash images to each post
  3. Generate professional carousel/infographic visuals
  4. Post all 5 types to LinkedIn via Zernio

Usage:
  python main.py              # Run full pipeline (interactive)
  python src/test_all_post_types_demo.py       # Step 1 only (generate posts)
  python src/attach_images_to_posts.py         # Step 2 only (add images)
  python src/generate_visual_posts_enhanced.py # Step 3 only (create visuals)
  python src/post_to_linkedin_zernio.py        # Step 4 only (post to LinkedIn)
"""

import sys
import subprocess
import datetime
import os
from config.logger import get_logger

logger = get_logger(__name__)


def print_header(title: str, width: int = 80):
    """Print formatted header."""
    print("\n" + "=" * width)
    print(f"  {title.center(width - 4)}")
    print("=" * width + "\n")


def run_step(step_num: int, script_path: str, description: str) -> bool:
    """
    Run a pipeline step as subprocess.
    
    Args:
        step_num: Step number (1-4)
        script_path: Path to Python script
        description: Step description
        
    Returns:
        True if successful, False otherwise
    """
    
    print_header(f"STEP {step_num}/4: {description}")
    
    try:
        result = subprocess.run([sys.executable, script_path], capture_output=False, text=True)
        
        if result.returncode == 0:
            logger.info(f"✓ Step {step_num} successful")
            return True
        else:
            logger.error(f"✗ Step {step_num} failed with exit code {result.returncode}")
            return False
    
    except Exception as e:
        logger.error(f"✗ Step {step_num} error: {e}")
        return False


def main():
    """Run the complete LinkedIn posts pipeline."""
    
    logger.info("=" * 80)
    logger.info("LinkedIn AI Daily Posts Pipeline".center(80))
    logger.info("=" * 80)
    logger.info(f"Date: {datetime.date.today().strftime('%Y-%m-%d')}")
    logger.info("Status: Starting full pipeline\n")
    
    # Check if posts already generated today
    today = datetime.date.today().strftime("%Y%m%d")
    existing_posts = f"linkedin_posts_{today}.txt"
    
    skip_generation = False
    if os.path.exists(existing_posts):
        response = input(f"\n[?] Posts already generated today ({existing_posts}). Skip generation? (y/n): ").strip().lower()
        skip_generation = (response == 'y')
    
    # Step 1: Generate test posts
    if not skip_generation:
        success = run_step(1, "src/test_all_post_types_demo.py", "Generate Test Posts")
        if not success:
            logger.error("Pipeline aborted at step 1")
            return 1
    else:
        logger.info("⊘ Skipping post generation (using existing posts)")
    
    # Step 2: Attach images
    success = run_step(2, "src/attach_images_to_posts.py", "Attach Images")
    if not success:
        logger.error("Pipeline aborted at step 2")
        return 1
    
    # Step 3: Generate visuals
    success = run_step(3, "src/generate_visual_posts_enhanced.py", "Generate Visual Composites")
    if not success:
        logger.error("Pipeline aborted at step 3 (continuing anyway - visuals optional)")
        # Don't abort, visuals are optional
    
    # Step 4: Post to LinkedIn
    success = run_step(4, "src/post_to_linkedin_zernio.py", "Post to LinkedIn")
    if not success:
        logger.error("Pipeline completed with errors at final step")
        return 1
    
    # Success
    print_header("✓ PIPELINE COMPLETE!", 80)
    logger.info("All 5 post types generated and posted to LinkedIn!")
    logger.info("\nNext steps:")
    logger.info("  • Check LinkedIn for drafted/scheduled posts")
    logger.info("  • Verify images attached correctly")
    logger.info("  • Review scheduled times (8 AM & 4 PM UTC)")
    logger.info("\nLogs available in: logs/")
    
    return 0


if __name__ == "__main__":
    exit(main())
