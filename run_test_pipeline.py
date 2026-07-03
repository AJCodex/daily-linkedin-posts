#!/usr/bin/env python3
"""
Test pipeline runner - runs the full pipeline for all 5 post types.
Converts test posts to the expected format, then runs:
1. attach_images_to_posts.py
2. generate_visual_posts.py
3. post_to_linkedin_zernio.py
"""

import os
import json
import datetime
import subprocess

def convert_test_posts_to_pipeline_format():
    """Convert test posts to linkedin_posts_YYYYMMDD.txt format"""
    today = datetime.date.today()
    test_file = f"test_posts_{today.strftime('%Y%m%d')}.txt"
    pipeline_file = f"linkedin_posts_{today.strftime('%Y%m%d')}.txt"
    
    if not os.path.exists(test_file):
        print(f"[X] Test file not found: {test_file}")
        return False
    
    print(f"[>] Converting test posts to pipeline format...")
    
    # Read test posts
    with open(test_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse into posts
    import re
    posts = []
    pattern = r'STREAM: (\d+)\s+TYPE: (.+?)\s+={80}\s+(.+?)(?====|$)'
    matches = re.findall(pattern, content, re.DOTALL)
    
    if not matches:
        print(f"[X] Could not parse test posts")
        return False
    
    # Create pipeline format file
    with open(pipeline_file, 'w', encoding='utf-8') as f:
        for stream_num, post_type, post_content in matches:
            f.write(f"{'='*80}\n")
            f.write(f"STREAM {stream_num} — {post_type.strip()}\n")
            f.write(f"{'='*80}\n")
            f.write(f"{post_content.strip()}\n\n")
    
    print(f"[+] Converted to: {pipeline_file}")
    return True

def run_pipeline():
    """Run the full pipeline: attach images -> generate visuals -> post to LinkedIn"""
    today = datetime.date.today()
    
    print("\n" + "="*80)
    print("[RUN] RUNNING FULL PIPELINE FOR ALL 5 POST TYPES")
    print("="*80 + "\n")
    
    # Step 1: Attach Images
    print("[1/3] Attaching images to posts...")
    result = subprocess.run(["python", "attach_images_to_posts.py"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[!] attach_images_to_posts.py had issues:")
        print(result.stdout)
        print(result.stderr)
    else:
        print(result.stdout)
    
    # Step 2: Generate Enhanced Visuals (Matplotlib + Playwright)
    print("\n[2/3] Generating carousel and infographic visuals...")
    result = subprocess.run(["python", "generate_visual_posts_enhanced.py"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[!] generate_visual_posts_enhanced.py had issues:")
        print(result.stdout)
        print(result.stderr)
    else:
        print(result.stdout)
    
    # Step 3: Post to LinkedIn
    print("\n[3/3] Posting all 5 types to LinkedIn...")
    result = subprocess.run(["python", "post_to_linkedin_zernio.py"], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    
    print("\n" + "="*80)
    print("[OK] PIPELINE COMPLETE!")
    print("="*80)
    print("\n[*] Check LinkedIn for all 5 post types!")
    print("   - Posts should appear in drafts or scheduled")
    print("   - Images should be attached to each post")
    print("   - Carousel and Infographic should have visual composites")

def main():
    # Convert test posts
    if not convert_test_posts_to_pipeline_format():
        return
    
    # Run pipeline
    run_pipeline()
    
    print("\n[*] Results saved to:")
    today = datetime.date.today().strftime('%Y%m%d')
    print(f"   - output/posts_{today}/posts/posts_with_images.json")
    print(f"   - output/posts_{today}/posts/posts_with_images.html")
    print(f"   - output/posts_{today}/generated_images/")
    print(f"   - output/posts_{today}/logs/linkedin_posting_log_{today}.json")

if __name__ == "__main__":
    main()
