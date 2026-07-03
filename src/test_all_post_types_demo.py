#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate realistic test posts for all 5 LinkedIn post types (demo/fallback).

Uses when OpenRouter API is unavailable. Creates:
  - Post 1: News post (randomized)
  - Post 2: Tips & Tricks post (randomized)
  - Post 3: Carousel (7 slides, randomized topics)
  - Post 4: Infographic (6+ data points, randomized metrics)
  - Post 5: Motivation post (randomized messages)

Output: test_posts_YYYYMMDD.txt
Each run generates different content - no two runs are identical!
"""

import sys
import os
import json
import random
from datetime import datetime

# Add project root to Python path (for GitHub Actions)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from config.logger import get_logger
from config.constants import POST_TYPES, TODAY

logger = get_logger(__name__)

# ============================================================================
# Randomized Content Libraries
# ============================================================================

NEWS_TOPICS = [
    ("Microsoft", "Achieves New Record in AI Model Efficiency", "45%", "7B parameter models"),
    ("Google", "Releases Open-Source Benchmark for RAG Systems", "52%", "retrieval accuracy"),
    ("OpenAI", "Announces Multi-Modal Model with 10x Faster Inference", "38%", "latency reduction"),
    ("Meta", "Open-Sources New Foundation Model for Enterprise", "41%", "training efficiency"),
    ("Stanford", "Publishes Breakthrough in Efficient Transformers", "50%", "memory footprint"),
]

TIPS_TOPICS = [
    ("RAG Pipeline", ["Chunk wisely", "Rerank ruthlessly", "Cache embeddings", "Hybrid search", "Monitor hallucination"]),
    ("Vector Embeddings", ["Use domain-specific models", "Normalize vectors", "Cache aggressively", "Multi-index strategy", "Optimize dimensions"]),
    ("LLM Prompting", ["Use few-shot examples", "Be explicit about constraints", "Structure with sections", "Include reasoning steps", "Validate outputs"]),
    ("Production ML", ["Monitor data drift", "Version everything", "Automated testing", "Gradual rollouts", "Fast fail mechanisms"]),
    ("Data Engineering", ["Stream processing", "Data validation layers", "Incremental pipelines", "Error recovery", "Observability at scale"]),
]

CAROUSEL_TOPICS = [
    {
        "title": "Building Production RAG Systems",
        "slides": [
            "🎯 The Complete Guide to Building Production RAG Systems\n\nFrom concept to deployment — everything you need to know about Retrieval-Augmented Generation.",
            "📚 What is RAG?\nRetrieval-Augmented Generation combines a retriever (to find relevant documents) with a generator (LLM) to produce grounded, factual responses.",
            "🔍 The Retriever\nConverts queries into embeddings, searches vector DB for similar documents. Quality retrieval = Quality answer.",
            "🧠 The Generator\nLLM takes retrieved context + query, generates response. Prompt engineering is critical here.",
            "🛠️ Common Pitfalls\n• Chunking too aggressively\n• Using generic embeddings\n• No reranking layer\n• Ignoring hallucination",
            "📊 Evaluation Metrics\n• Retrieval recall\n• Answer F1 score\n• Latency metrics",
            "🚀 Production Checklist\n✓ Semantic chunking ✓ Hybrid search ✓ Reranking ✓ Caching ✓ Monitoring"
        ]
    },
    {
        "title": "AI Career Roadmap 2026",
        "slides": [
            "🎯 Your Path to AI Engineering Excellence\n\nNavigating the evolving landscape of AI roles and skills in 2026.",
            "🔵 Foundation Layer\nStrong fundamentals matter: Python, Linear Algebra, Probability, Statistics.",
            "🟢 Core Skills\nMachine Learning: Supervised, Unsupervised, Reinforcement Learning, Neural Networks.",
            "🟡 Advanced Topics\nDeep Learning, Transformers, LLMs, Computer Vision, NLP, Multi-modal models.",
            "🔴 Production Skills\nMLOps, Model Serving, Monitoring, A/B Testing, Cost Optimization.",
            "🟣 Specialization\nChoose: Research, Product, Infrastructure, Safety, or Entrepreneurship.",
            "📈 Growth Path\nContinuous learning, build in public, contribute to open source, ship projects."
        ]
    },
    {
        "title": "Prompt Engineering Mastery",
        "slides": [
            "🎯 The Art & Science of Prompt Engineering\n\nHow to get the most out of modern LLMs through strategic prompting.",
            "📝 Prompt Structure\nContext → Instruction → Constraints → Output Format → Examples.",
            "🔄 Few-Shot Learning\nProvide 2-3 examples of desired behavior before asking for the main task.",
            "❌ Negative Examples\nShow what NOT to do. This guides the model away from common mistakes.",
            "🏗️ Chain-of-Thought\nAsk LLM to 'think step by step'. This improves reasoning quality dramatically.",
            "🔍 Constraint Specification\nBe explicit: 'Respond in JSON', 'Keep answer under 100 words', 'Use technical language'.",
            "✅ Validation & Iteration\nTest, measure, refine. Small changes can have big impacts."
        ]
    }
]

INFOGRAPHIC_TOPICS = [
    {
        "title": "Top AI Skills in Demand 2026",
        "data": [("Python", 92), ("Machine Learning", 85), ("Deep Learning", 78), ("LLM Architecture", 88), ("Cloud Infrastructure", 76), ("Data Engineering", 82), ("RAG Systems", 79), ("MLOps", 74)]
    },
    {
        "title": "AI Model Size Comparison",
        "data": [("GPT-4", 1760), ("Claude 3", 1300), ("Llama 3", 405), ("Mistral", 123), ("Phi 3", 14), ("TinyLlama", 1)]
    },
    {
        "title": "LLM Adoption by Industry 2026",
        "data": [("Tech/Software", 89), ("Finance", 76), ("Healthcare", 68), ("Retail", 54), ("Manufacturing", 42), ("Government", 35)]
    },
    {
        "title": "RAG vs Fine-Tuning Tradeoffs",
        "data": [("Implementation Speed", 95), ("Cost Efficiency", 87), ("Knowledge Updates", 92), ("Customization", 65), ("Accuracy", 78)]
    }
]

MOTIVATION_MESSAGES = [
    "🌟 The Compound Effect of Small Wins in Tech\n\nEvery commit matters. Every bug fix matters. Every documentation update matters.\n\nAlone, each seems insignificant. But over months and years, these small wins compound exponentially.\n\nThe engineer who ships 10 tiny improvements a week outpaces the engineer who waits for the perfect solution.\n\nFocus on consistency, not perfection. 🚀",
    
    "💪 Building in Public\n\nSharing your journey isn't weakness—it's connection.\n\nWhen you share struggles, someone learns they're not alone.\nWhen you share wins, someone gets inspired to try.\nWhen you share failures, someone avoids your mistakes.\n\nThe best engineers are builders AND teachers.\n\nYour code matters. Your voice matters. 🎯",
    
    "🚀 Done is Better Than Perfect\n\nShip. Learn. Iterate. Repeat.\n\nWaiting for perfection is the #1 blocker for engineers.\n\n• Launch MVP today → Get feedback → Improve\n• Ship 80% solution today → Complete tomorrow if needed\n• Deploy to prod → Monitor → Fix issues in real-time\n\nSpeed of learning > Perfection of planning.\n\nMove fast. Break things intelligently. Ship. 🔥",
]




def create_test_posts():
    """Create 5 realistic test LinkedIn posts with RANDOMIZED content.
    
    Each run generates different carousel topics, infographic metrics, and tips.
    This ensures posts are unique and don't repeat across multiple runs!
    """
    
    # Randomly select topics
    news_company, news_title, news_pct, news_metric = random.choice(NEWS_TOPICS)
    tips_topic, tips_list = random.choice(TIPS_TOPICS)
    carousel_topic = random.choice(CAROUSEL_TOPICS)
    infographic_topic = random.choice(INFOGRAPHIC_TOPICS)
    motivation_msg = random.choice(MOTIVATION_MESSAGES)
    
    posts = [
        {
            "stream": 1,
            "type": POST_TYPES[1],  # News
            "content": f"""🔬 Breakthrough: {news_company} {news_title}

Researchers have demonstrated a {news_pct} improvement in {news_metric} through novel optimization techniques, reducing computational costs while maintaining accuracy.

Key findings:
• New approach improves performance metrics significantly
• Training efficiency increases across model families
• Techniques applicable to existing architectures

This advancement paves the way for more sustainable and cost-effective AI deployment in enterprise environments.

#AI #MachineLearning #Innovation #Breakthrough #AISustainability"""
        },
        {
            "stream": 2,
            "type": POST_TYPES[2],  # Tips & Tricks
            "content": f"""💡 Essential Tips for Optimizing Your {tips_topic}

These proven techniques will dramatically improve performance:

""" + "".join([f"{i+1}️⃣ {tip}\n" for i, tip in enumerate(tips_list[:5])]) + f"""
Pro tip: Start with #1 and #{random.randint(2,5)}. They give 80% of the value with 20% of the effort.

#Tips #Optimization #BestPractices #Engineering #TechCommunity"""
        },
        {
            "stream": 3,
            "type": POST_TYPES[3],  # Carousel
            "content": "Slide 1: 🎯 " + carousel_topic["title"] + "\n\n" + carousel_topic["slides"][0] + "\n\n" + "\n\n".join([f"Slide {i+2}:\n{slide}" for i, slide in enumerate(carousel_topic["slides"][1:])])
        },
        {
            "stream": 4,
            "type": POST_TYPES[4],  # Infographic
            "content": infographic_topic["title"] + "\n\n" + "\n".join([f"{label}: {value}" for label, value in infographic_topic["data"]])
        },
        {
            "stream": 5,
            "type": POST_TYPES[5],  # Motivation
            "content": motivation_msg + "\n\n#EngineeringMindset #DevCulture #Growth #TechCommunity #Inspiration"
        }
    ]
    
    logger.info(f"✓ Generated 5 randomized test posts (News: {news_company}, Tips: {tips_topic}, Carousel: {carousel_topic['title']}, Infographic: {infographic_topic['title']})")
    
    return posts


def save_test_posts(posts):
    """Save test posts to file."""
    
    output_file = f"test_posts_{TODAY}.txt"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for post in posts:
                f.write(f"STREAM: {post['stream']}\n")
                f.write(f"TYPE: {post['type']}\n")
                f.write("=" * 80 + "\n")
                f.write(post['content'] + "\n")
                f.write("=" * 80 + "\n\n")
        
        logger.info(f"✓ Generated {len(posts)} test posts -> {output_file}")
        return output_file
        
    except Exception as e:
        logger.error(f"Failed to save test posts: {e}")
        return None


def main():
    """Main entry point."""
    logger.info("Generating test posts (demo mode)...")
    
    posts = create_test_posts()
    output = save_test_posts(posts)
    
    if output:
        logger.info(f"Success! Test posts saved to {output}")
        logger.info(f"Next step: python src/attach_images_to_posts.py")
    else:
        logger.error("Failed to generate test posts")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
