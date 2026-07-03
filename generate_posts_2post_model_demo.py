"""
Demo version of generate_posts_2post_model.py with simulated API responses
Used for testing when network is restricted
"""

import json
import os
from datetime import datetime
import re

# Simulate the post generation with mock data
MOCK_NEWS_POST = """🚀 **Azure AI Search Now Supports Multi-Turn Conversations**

Microsoft just launched multi-turn conversation support in Azure AI Search, letting you build conversational AI apps that remember context across interactions. 

This means your search-powered apps can now:
- Remember previous queries in a conversation
- Provide context-aware follow-ups
- Deliver more relevant results based on conversation history

Why it matters: Conversational AI is becoming the default UX. This closes the gap between simple search and truly intelligent assistants.

👉 If you're building with Azure AI, this changes your architecture options. What's your current approach to context management?

Source: Azure Updates Blog"""

MOCK_TIPS_POST = """💡 **Use Search Indexes to Speed Up RAG by 10x**

Most RAG implementations index everything—documents, PDFs, web pages. But here's what I learned:

Only index what you'll actually query.

If you're building customer support RAG, don't index your entire product documentation. Index only:
- FAQs (most common questions)
- Recent bug fixes
- Known issues
- API references

This cuts your search latency from 2-3 seconds to 200-400ms. It also reduces API costs by 80% because you're searching smaller indexes.

The tradeoff: Occasionally, users ask about something not indexed. But being fast 95% of the time beats being slow 100% of the time.

👉 What's in your RAG index? Are you being selective or indexing everything?"""

MOCK_CAROUSEL_POST = """📊 **Inside Microsoft's AI Search Architecture (7 slides)**

Slide 1: The problem - traditional search is keyword-based
Slide 2: Vector embeddings let you search by meaning
Slide 3: Hybrid search combines both (best of both worlds)
Slide 4: Azure AI Search implements this at scale
Slide 5: Real latency benchmarks (from our tests)
Slide 6: When to use each approach
Slide 7: How to get started

👉 Which search approach are you using in production?"""

MOCK_INFOGRAPHIC_POST = """📈 **AI Skills That Actually Get Hired (2026 Data)**

Based on 500+ LinkedIn profiles of AI engineers at FAANG:

Top 5 Skills by Frequency:
1. Python (89%)
2. LLMs / Prompt Engineering (76%)
3. Azure / Cloud (71%)
4. Vector Databases (64%)
5. MLOps / DevOps (58%)

The surprise: 89% know Python but only 34% can do proper MLOps. That's where the gap is.

Dataset source: AI skills audit from LinkedIn profiles in AI teams"""

MOCK_MOTIVATION_POST = """⚡ **The 3-Hour Productivity Hack That Changed My AI Work**

I started blocking my calendar: 9-12 AM for coding, 1-2 PM for meetings, 3-5 PM for thinking.

Before: Scattered focus, context switches every 30 min = 6 hours of "work" but only 2 hours of actual output.

After: Protected deep work, meetings clustered, time to reflect = 6 hours of "work" and 5 hours of actual output.

The output/hour improved by 150%.

If you're drowning in meetings and emails, this alone might be the fix. Your RAG pipeline, your vector database, your prompts—they all improve when you have time to think.

👉 What's your best productivity hack for AI work?"""

def get_today_post_type():
    """Get today's post type (rotating through types)"""
    post_types = ["Tips & Tricks", "Carousel", "Infographic", "Motivation"]
    
    log_file = "post-rotation-log.json"
    
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            log = json.load(f)
            if log:
                last_type = log[-1]["type"]
                # Find first type that's not the last type
                for ptype in post_types:
                    if ptype != last_type:
                        return ptype
    
    # Default to first type
    return post_types[0]

def update_rotation_log(post_type):
    """Update the rotation log"""
    log_file = "post-rotation-log.json"
    
    log_entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "type": post_type
    }
    
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            log = json.load(f)
    else:
        log = []
    
    # Keep only last 30 days
    if len(log) >= 30:
        log = log[-29:]
    
    log.append(log_entry)
    
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2)

def main():
    print("=" * 60)
    print("LinkedIn Daily Posts Generator (2-Post Model - DEMO)")
    print("=" * 60)
    
    # Get today's type
    secondary_type = get_today_post_type()
    print(f"\n✓ Today's post types: News + {secondary_type}")
    
    # Select mock post
    posts = []
    posts.append({
        "stream": "News",
        "content": MOCK_NEWS_POST,
        "source": "Azure Updates Blog"
    })
    
    if secondary_type == "Tips & Tricks":
        posts.append({
            "stream": secondary_type,
            "content": MOCK_TIPS_POST,
            "source": "AI Knowledge"
        })
    elif secondary_type == "Carousel":
        posts.append({
            "stream": secondary_type,
            "content": MOCK_CAROUSEL_POST,
            "source": "AI Architecture Guide"
        })
    elif secondary_type == "Infographic":
        posts.append({
            "stream": secondary_type,
            "content": MOCK_INFOGRAPHIC_POST,
            "source": "LinkedIn Skills Data"
        })
    else:  # Motivation
        posts.append({
            "stream": secondary_type,
            "content": MOCK_MOTIVATION_POST,
            "source": "Personal Experience"
        })
    
    # Save posts in the format expected by update_post_history.py
    today = datetime.now().strftime("%Y%m%d")
    output_file = f"linkedin_posts_{today}.txt"
    
    with open(output_file, "w", encoding="utf-8") as f:
        for i, post in enumerate(posts, 1):
            f.write(f"{'=' * 60}\n")
            f.write(f"STREAM {i} — {post['stream']}\n")
            f.write(f"{'=' * 60}\n\n")
            f.write(f"{post['content']}\n\n")
            f.write(f"Source: {post['source']}\n")
            f.write(f"Word count: {len(post['content'].split())}\n")
            f.write(f"Format: Text Post\n\n")
    
    print(f"✓ Generated 2 posts")
    print(f"✓ Saved to: {output_file}")
    
    # Update rotation log
    update_rotation_log(secondary_type)
    print(f"✓ Updated rotation log")
    
    # Show summary
    print(f"\n📊 Generated Posts:")
    for i, post in enumerate(posts, 1):
        word_count = len(post['content'].split())
        print(f"   {i}. {post['stream']} ({word_count} words)")

if __name__ == "__main__":
    main()
