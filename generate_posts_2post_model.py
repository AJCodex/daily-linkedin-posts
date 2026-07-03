#!/usr/bin/env python3
"""
Generate 2 LinkedIn posts daily: News + rotating secondary type (Tips, Carousel, Infographic, Motivation).
Local storage only (no Git push during testing).

Usage:
    python3 generate_posts_via_openrouter.py

Outputs:
    - linkedin_posts_YYYYMMDD.txt (2 posts)
    - post-rotation-log.json (tracks rotation)
"""

import os
import json
import datetime
import requests
from dotenv import load_dotenv

load_dotenv()

# Constants
API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://api.openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemma-4-31b-it:free"  # Free model with reasoning

POST_TYPES = ["Tips & Tricks", "Carousel", "Infographic", "Motivation/Productivity"]
ROTATION_LOG_PATH = "./post-rotation-log.json"
OUTPUT_DIR = "./"

if not API_KEY:
    raise ValueError("OPENROUTER_API_KEY not set in .env file")

# ============================================================================
# Rotation Logic: Determine today's secondary post type
# ============================================================================

def get_today_post_type():
    """Determine today's secondary post type, rotating through the list."""
    rotation_log = []
    
    if os.path.exists(ROTATION_LOG_PATH):
        with open(ROTATION_LOG_PATH, 'r') as f:
            rotation_log = json.load(f)
    
    # Get last posted type
    last_type = rotation_log[-1]["type"] if rotation_log else None
    
    # Find next type (skip if it was just used)
    today_type = None
    for post_type in POST_TYPES:
        if post_type != last_type:
            today_type = post_type
            break
    
    if today_type is None:
        today_type = POST_TYPES[0]  # Fallback to first type
    
    # Save to rotation log
    today = str(datetime.date.today())
    rotation_log.append({"date": today, "type": today_type})
    rotation_log = rotation_log[-30:]  # Keep last 30 days
    
    with open(ROTATION_LOG_PATH, 'w') as f:
        json.dump(rotation_log, f, indent=2)
    
    print(f"✓ Today's post types: News + {today_type}")
    return today_type

# ============================================================================
# Fetch RSS Data
# ============================================================================

def fetch_ai_news():
    """Fetch latest AI news from RSS feeds."""
    print("Fetching Microsoft AI news from RSS feeds...")
    
    # In a real scenario, this would call fetch_ai_news_rss.py
    # For testing, we'll use a placeholder
    ai_news_file = "./ai_news_data.json"
    
    if os.path.exists(ai_news_file):
        with open(ai_news_file, 'r') as f:
            return json.load(f)
    else:
        # Placeholder if no RSS data available
        return [
            {
                "title": "Microsoft Announces New Copilot AI Features",
                "description": "New AI capabilities for enterprise users...",
                "url": "https://blogs.microsoft.com/ai/",
                "source": "Microsoft AI Blog",
                "pubDate": str(datetime.date.today())
            }
        ]

# ============================================================================
# LLM API Call
# ============================================================================

def call_llm(prompt):
    """Call OpenRouter LLM API with the given prompt (free Gemma model with reasoning)."""
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "https://github.com/AJCodex/daily-linkedin-posts",
        "X-Title": "Daily LinkedIn Posts"
    }
    
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 1.0,
        "max_tokens": 800,
        "reasoning": {"enabled": True}  # Enable reasoning for better quality
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if "choices" in result and len(result["choices"]) > 0:
            message = result["choices"][0]["message"]
            # Extract content, preserving reasoning details if present
            return message.get("content", "")
        else:
            raise ValueError(f"Unexpected API response: {result}")
    
    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
        raise

# ============================================================================
# Post Generation Prompts
# ============================================================================

def generate_news_post(ai_news_list):
    """Generate a News post from latest Microsoft AI news."""
    
    news_context = ""
    for i, item in enumerate(ai_news_list[:5]):  # Top 5 news items
        news_context += f"News {i+1}: {item['title']}\n{item['description'][:200]}...\nSource: {item['url']}\n---\n"
    
    prompt = f"""
You are Abhinav Jain's AI content generator for Microsoft AI, Azure, and Copilot topics on LinkedIn.

Write ONE LinkedIn post (News) from the following Microsoft AI news:

{news_context}

POST RULES:
1. Third-person observer voice (no "I" or "my")
2. 150–250 words
3. Hook (1–2 lines) → What happened → Why it matters → CTA question
4. Include one source URL from the news above
5. No em-dashes, max 2 hashtags
6. End with an engagement question

DO NOT include "Post 1:" or any post labels. Write the post content directly.

OUTPUT FORMAT:
[Post text here]

Source: [URL]
"""
    
    post = call_llm(prompt)
    post = post.replace('**', '').replace('*', '')
    lines = post.split('\n')
    cleaned_lines = [l for l in lines if not l.strip().startswith('Word count:') and not l.strip().startswith('Format:') and not l.strip().startswith('Source:')]
    return '\n'.join(cleaned_lines).strip()

def generate_tips_post():
    """Generate a Tips & Tricks post."""
    
    prompt = """
You are Abhinav Jain, writing practical tips about Power Platform, Azure, Copilot Studio, or AI Search on LinkedIn.

Write ONE LinkedIn post (Tips & Tricks) about a practical, actionable tip readers can try today.

POST RULES:
1. First-person allowed ("Here is what I do...")
2. 100–200 words
3. Numbered steps (max 5) where helpful
4. Must be replicable today
5. End with: "Try this and let me know how it goes."
6. No em-dashes

DO NOT include "Post 2:" or any post labels. Write the post content directly.

OUTPUT FORMAT:
[Post text here]
"""
    
    post = call_llm(prompt)
    post = post.replace('**', '').replace('*', '')
    lines = post.split('\n')
    cleaned_lines = [l for l in lines if not l.strip().startswith('Word count:') and not l.strip().startswith('Format:')]
    return '\n'.join(cleaned_lines).strip()

def generate_carousel_post():
    """Generate a Carousel post (7 slides + caption)."""
    
    prompt = """
You are Abhinav Jain, writing a LinkedIn carousel (7 slides) about a deep-dive Microsoft AI topic.

Pick a topic: RAG architecture, Copilot Studio, Prompt Flow, Azure OpenAI integration, AI Search indexing, etc.

SLIDE STRUCTURE:
- Slide 1: Hook (6–8 words, curiosity gap)
- Slides 2–6: One key insight per slide, max 2 sentences each
- Slide 7: Summary + CTA ("Follow Abhinav Jain for daily Microsoft AI breakdowns.")

Caption (50–80 words): Hook + what you'll learn + question + CTA

OUTPUT FORMAT (clearly separated):
=== SLIDE 1 ===
[Hook text]

=== SLIDE 2 ===
[Insight]

[... and so on for all 7 slides]

=== CAPTION ===
[Caption text]
"""
    
    post = call_llm(prompt)
    post = post.replace('**', '').replace('*', '')
    lines = post.split('\n')
    cleaned_lines = [l for l in lines if not l.strip().startswith('Word count:') and not l.strip().startswith('Format:')]
    return '\n'.join(cleaned_lines).strip()

def generate_infographic_post():
    """Generate an Infographic post (PNG + caption)."""
    
    prompt = """
You are Abhinav Jain, creating a LinkedIn infographic post about Microsoft/Azure adoption or productivity.

Write a caption for an infographic (1080×1080 PNG) with a dataset you create or know about.

CAPTION RULES (60–100 words):
1. Third-person voice
2. Hook: most surprising number
3. One context sentence
4. One implication for the reader
5. Question CTA
6. No em-dashes

Also provide:
- Infographic title
- 6–10 data points (percentages, numbers, growth rates)
- Data format (ranked list, donut breakdown, timeline, etc.)

OUTPUT FORMAT:
=== CAPTION ===
[Caption text]

=== TITLE ===
[Infographic title]

=== DATA FORMAT ===
[e.g., RANKED_BARS or DONUT_BREAKDOWN]

=== DATA POINTS ===
1. [Item]: [Number/Percentage]
2. [Item]: [Number/Percentage]
[... etc]
"""
    
    post = call_llm(prompt)
    post = post.replace('**', '').replace('*', '')
    lines = post.split('\n')
    cleaned_lines = [l for l in lines if not l.strip().startswith('Word count:') and not l.strip().startswith('Format:')]
    return '\n'.join(cleaned_lines).strip()

def generate_motivation_post():
    """Generate a Motivation/Productivity post."""
    
    prompt = """
You are Abhinav Jain, sharing an AI productivity hack using Microsoft tools on LinkedIn.

Write ONE LinkedIn post (Motivation/Productivity) about a specific, replicable way to save time using Copilot, Power Automate, Teams, Loop, or OneNote AI.

POST RULES:
1. First-person allowed
2. 150–250 words
3. Include: specific tool + specific task it replaces/accelerates + time saved (specific number)
4. End with: "To do this yourself: [1–3 steps]"
5. CTA: "What is one thing you are still doing manually that Copilot could handle?"
6. No em-dashes

DO NOT include "Post 5:" or any post labels. Write the post content directly.

OUTPUT FORMAT:
[Post text here]
"""
    
    post = call_llm(prompt)
    post = post.replace('**', '').replace('*', '')
    lines = post.split('\n')
    cleaned_lines = [l for l in lines if not l.strip().startswith('Word count:') and not l.strip().startswith('Format:')]
    return '\n'.join(cleaned_lines).strip()

# ============================================================================
# Main Pipeline
# ============================================================================

def main():
    """Generate 2 posts and save to file."""
    
    print("=" * 60)
    print("LinkedIn Daily Posts Generator (2-Post Model)")
    print("=" * 60)
    print()
    
    # Step 1: Determine today's post type
    today_type = get_today_post_type()
    
    # Step 2: Fetch news
    ai_news = fetch_ai_news()
    print(f"✓ Fetched {len(ai_news)} news items")
    
    # Step 3: Generate News post
    print(f"\n📝 Generating News post...")
    news_post = generate_news_post(ai_news)
    
    # Step 4: Generate secondary post
    print(f"📝 Generating {today_type} post...")
    
    if today_type == "Tips & Tricks":
        secondary_post = generate_tips_post()
    elif today_type == "Carousel":
        secondary_post = generate_carousel_post()
    elif today_type == "Infographic":
        secondary_post = generate_infographic_post()
    else:  # Motivation/Productivity
        secondary_post = generate_motivation_post()
    
    # Step 5: Save to file
    today = datetime.date.today().strftime('%Y%m%d')
    output_file = os.path.join(OUTPUT_DIR, f'linkedin_posts_{today}.txt')
    
    content = f"""==================================================
STREAM 1 — NEWS
==================================================
{news_post}

==================================================
STREAM 2 — {today_type.upper()}
==================================================
{secondary_post}
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✅ Posts saved to: {output_file}")
    print(f"\nSummary:")
    print(f"  Post 1: News ({len(news_post.split())} words)")
    print(f"  Post 2: {today_type} ({len(secondary_post.split())} words)")
    print(f"\nNext step: python3 update_post_history.py")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
