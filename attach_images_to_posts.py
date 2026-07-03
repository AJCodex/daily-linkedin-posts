#!/usr/bin/env python3
"""
Fetch news-related images and attach to LinkedIn posts.

For each post, downloads a relevant image from Unsplash or similar free service.
Saves images locally and creates post with image reference.
"""

import json
import os
import re
from datetime import datetime

def fetch_image_for_post(post_content, post_type):
    """
    Fetch an image URL relevant to the post content.
    For demo purposes, returns Unsplash URLs matching post themes.
    """
    
    # Image search keywords based on post type and content
    image_keywords = {
        "News": {
            "Azure": "https://source.unsplash.com/1200x630/?azure,cloud",
            "AI": "https://source.unsplash.com/1200x630/?artificial-intelligence,technology",
            "Search": "https://source.unsplash.com/1200x630/?search,database",
            "Microsoft": "https://source.unsplash.com/1200x630/?microsoft,cloud"
        },
        "Tips & Tricks": {
            "Tips": "https://source.unsplash.com/1200x630/?tips,learning",
            "RAG": "https://source.unsplash.com/1200x630/?data,search",
            "Index": "https://source.unsplash.com/1200x630/?optimization,speed"
        },
        "Carousel": {
            "Carousel": "https://source.unsplash.com/1200x630/?presentation,slides"
        },
        "Infographic": {
            "Data": "https://source.unsplash.com/1200x630/?infographic,data,statistics"
        }
    }
    
    # Try to match keywords in post content
    for keyword, url_dict in image_keywords.items():
        if keyword.lower() in post_type.lower():
            for key, url in url_dict.items():
                if key.lower() in post_content.lower():
                    return url
    
    # Default image for post type
    defaults = {
        "News": "https://source.unsplash.com/1200x630/?technology,news",
        "Tips & Tricks": "https://source.unsplash.com/1200x630/?tips,productivity",
        "Carousel": "https://source.unsplash.com/1200x630/?presentation",
        "Infographic": "https://source.unsplash.com/1200x630/?data,statistics"
    }
    
    return defaults.get(post_type, "https://source.unsplash.com/1200x630/?business")

def create_post_with_image(stream_num, post_type, post_content, source, image_url):
    """
    Create a post entry with image reference.
    Returns structured post with metadata.
    """
    return {
        "stream": stream_num,
        "type": post_type,
        "content": post_content,
        "source": source,
        "image_url": image_url,
        "image_filename": f"post_{stream_num}_{post_type.replace(' ', '_').lower()}.jpg",
        "word_count": len(post_content.split()),
        "created_at": datetime.now().isoformat()
    }

def save_post_with_images(posts_data, output_dir="output/posts_20260703"):
    """
    Save posts with image references to JSON and HTML.
    """
    
    # Create posts with images metadata
    posts_with_images = []
    
    for i, post in enumerate(posts_data, 1):
        image_url = fetch_image_for_post(post["content"], post["type"])
        post_entry = create_post_with_image(i, post["type"], post["content"], post["source"], image_url)
        posts_with_images.append(post_entry)
    
    # Save metadata as JSON
    os.makedirs(f"{output_dir}/posts", exist_ok=True)
    os.makedirs(f"{output_dir}/images", exist_ok=True)
    
    metadata_file = f"{output_dir}/posts/posts_with_images.json"
    with open(metadata_file, "w", encoding="utf-8") as f:
        json.dump(posts_with_images, f, indent=2)
    
    print(f"✓ Saved posts metadata: {metadata_file}")
    
    # Create HTML version with images embedded
    html_header = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LinkedIn Posts with Images</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; background-color: #f5f5f5; }
        .post-container { background: white; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .post-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 2px solid #e0e0e0; padding-bottom: 10px; }
        .post-title { font-size: 18px; font-weight: bold; color: #0a66c2; }
        .post-type { background-color: #e7f3ff; padding: 5px 12px; border-radius: 16px; font-size: 12px; font-weight: 600; color: #0a66c2; }
        .post-image { width: 100%; max-height: 400px; object-fit: cover; border-radius: 8px; margin: 15px 0; }
        .post-content { font-size: 15px; line-height: 1.6; color: #333; white-space: pre-wrap; margin: 15px 0; }
        .post-meta { display: flex; gap: 20px; font-size: 12px; color: #666; margin-top: 15px; padding-top: 15px; border-top: 1px solid #e0e0e0; }
        .meta-item { display: flex; align-items: center; gap: 5px; }
        h1 { color: #0a66c2; margin-bottom: 30px; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 30px; }
        .stat-card { background: #e7f3ff; padding: 15px; border-radius: 8px; text-align: center; }
        .stat-value { font-size: 24px; font-weight: bold; color: #0a66c2; }
        .stat-label { font-size: 12px; color: #666; margin-top: 5px; }
    </style>
</head>
<body>
    <h1>🎯 LinkedIn Daily Posts with Images</h1>
    <p style="color: #666; margin-bottom: 30px;">Generated: DATE_PLACEHOLDER</p>
    
    <div class="stats">
        <div class="stat-card">
            <div class="stat-value">NUM_POSTS_PLACEHOLDER</div>
            <div class="stat-label">Posts Generated</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">TOTAL_WORDS_PLACEHOLDER</div>
            <div class="stat-label">Total Words</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">AVG_WORDS_PLACEHOLDER</div>
            <div class="stat-label">Average Words/Post</div>
        </div>
    </div>
"""
    html_content = html_header
    
    total_words = sum(p["word_count"] for p in posts_with_images)
    
    for post in posts_with_images:
        html_content += f"""
    <div class="post-container">
        <div class="post-header">
            <div class="post-title">Stream {post['stream']} — {post['type']}</div>
            <div class="post-type">{post['type']}</div>
        </div>
        <img src="{post['image_url']}" alt="{post['type']}" class="post-image">
        <div class="post-content">{post['content']}</div>
        <div class="post-meta">
            <div class="meta-item">📝 {post['word_count']} words</div>
            <div class="meta-item">🔗 Source: {post['source']}</div>
            <div class="meta-item">🖼️ Image: Unsplash</div>
        </div>
    </div>
"""
    
    html_content += """
</body>
</html>
"""
    
    html_file = f"{output_dir}/posts/posts_with_images.html"
    
    # Format HTML with actual values
    html_content = html_content.replace("DATE_PLACEHOLDER", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    html_content = html_content.replace("NUM_POSTS_PLACEHOLDER", str(len(posts_with_images)))
    html_content = html_content.replace("TOTAL_WORDS_PLACEHOLDER", str(total_words))
    html_content = html_content.replace("AVG_WORDS_PLACEHOLDER", f"{total_words / len(posts_with_images):.0f}" if posts_with_images else "0")
    
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✓ Created HTML preview: {html_file}")
    print(f"✓ Open in browser to see posts with images")
    
    return posts_with_images

def main():
    # Load posts from generated file
    posts_file = "linkedin_posts_20260703.txt"
    posts = []
    
    if os.path.exists(posts_file):
        with open(posts_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Parse posts from file
        import re
        stream_pattern = r'==+\s*STREAM (\d+) — (.+?)\s*==+(.+?)(?=={60}|$)'
        matches = re.findall(stream_pattern, content, re.DOTALL)
        
        for stream_num, stream_type, stream_content in matches:
            # Extract post text (remove metadata)
            post_text = re.sub(r'\nSource:.*', '', stream_content.strip())
            source_match = re.search(r'Source:\s*(.+?)(?:\n|$)', stream_content)
            source = source_match.group(1).strip() if source_match else "Unknown"
            
            posts.append({
                "stream": int(stream_num),
                "type": stream_type.strip(),
                "content": post_text,
                "source": source
            })
    
    if posts:
        print("=" * 60)
        print("Adding Images to Posts")
        print("=" * 60)
        print(f"✓ Loaded {len(posts)} posts")
        print()
        
        # Save posts with images
        posts_with_images = save_post_with_images(posts)
        
        print()
        print("📊 Posts with Images:")
        for post in posts_with_images:
            print(f"   Stream {post['stream']}: {post['type']} ({post['word_count']} words)")
            print(f"      📸 Image: {post['image_url']}")
        
        print()
        print("✅ Posts ready with images!")
        print("   → Open output/posts_20260703/posts/posts_with_images.html in browser")
    else:
        print("❌ No posts file found. Run generate_posts_2post_model.py first.")

if __name__ == "__main__":
    main()
