#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate realistic test posts for all 5 LinkedIn post types (demo/fallback).

Uses when OpenRouter API is unavailable. Creates:
  - Post 1: News post
  - Post 2: Tips & Tricks post  
  - Post 3: Carousel (7 slides)
  - Post 4: Infographic (6+ data points)
  - Post 5: Motivation post

Output: test_posts_YYYYMMDD.txt
"""

import sys
import os
import json
from datetime import datetime

# Add project root to Python path (for GitHub Actions)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from config.logger import get_logger
from config.constants import POST_TYPES, TODAY

logger = get_logger(__name__)


def create_test_posts():
    """Create 5 realistic test LinkedIn posts for all types."""
    
    posts = [
        {
            "stream": 1,
            "type": POST_TYPES[1],  # News
            "content": """🔬 Breakthrough: Microsoft Achieves New Record in AI Model Efficiency

Researchers at Microsoft AI Labs have demonstrated a 45% improvement in model efficiency through novel optimization techniques, reducing computational costs while maintaining accuracy.

Key findings:
• New attention mechanism reduces memory footprint by 35%
• Training time decreased from 72 to 40 hours for 7B parameter models
• Techniques applicable to existing model architectures

This advancement paves the way for more sustainable and cost-effective AI deployment in enterprise environments.

#AI #MachineLearning #Microsoft #Innovation #AISustainability"""
        },
        {
            "stream": 2,
            "type": POST_TYPES[2],  # Tips & Tricks
            "content": """💡 5 Essential Tips for Optimizing Your RAG Pipeline

Retrieval-Augmented Generation (RAG) systems are powerful, but often underperforming. Here's how to maximize their effectiveness:

1️⃣ Chunk wisely — Don't use fixed-size chunks. Use semantic boundaries for better context retention.

2️⃣ Rerank ruthlessly — Filter low-confidence retrievals with a reranker before feeding to LLM.

3️⃣ Cache embeddings — Pre-compute and cache all embeddings to reduce latency by 60%.

4️⃣ Hybrid search — Combine BM25 + dense search. BM25 catches keyword matches, dense catches semantic meaning.

5️⃣ Monitor hallucination — Track cases where LLM diverges from retrieved context. Retrain your ranker on these cases.

Pro tip: Start with #1 and #5. They give 80% of the value with 20% of the effort.

#RAG #LLMs #AIEngineering #MLOps #ProductionAI"""
        },
        {
            "stream": 3,
            "type": POST_TYPES[3],  # Carousel
            "content": """Slide 1: 🎯 The Complete Guide to Building Production RAG Systems

From concept to deployment — everything you need to know about Retrieval-Augmented Generation.

Slide 2: 📚 What is RAG?
Retrieval-Augmented Generation combines a retriever (to find relevant documents) with a generator (LLM) to produce grounded, factual responses. Why? LLMs hallucinate. RAG solves this.

Slide 3: 🔍 The Retriever
Converts queries into embeddings, searches vector DB for similar documents. Quality of retrieval = Quality of final answer. Choose good embeddings. Chunk intelligently.

Slide 4: 🧠 The Generator  
LLM takes retrieved context + query, generates response. Prompt engineering is critical. Include examples. Be explicit about constraints.

Slide 5: 🛠️ Common Pitfalls
• Chunking too aggressively (lose context)
• Using generic embeddings (not domain-specific)
• No reranking (garbage in = garbage out)
• Ignoring hallucination detection

Slide 6: 📊 Evaluation Metrics
• Retrieval recall: Did we find the right documents?
• Answer F1: How accurate is the generated response?
• Latency: Is this production-ready?

Slide 7: 🚀 Production Checklist
✓ Semantic chunking ✓ Multi-index hybrid search ✓ Reranking layer ✓ Caching strategy ✓ Monitoring/logging ✓ Fast fail mechanisms"""
        },
        {
            "stream": 4,
            "type": POST_TYPES[4],  # Infographic
            "content": """Top AI Skills in Demand 2026

Python: 92
Machine Learning: 85
Deep Learning: 78
LLM/Transformer Architecture: 88
Cloud Infrastructure (Azure/AWS): 76
Data Engineering: 82
RAG Systems: 79
MLOps & Deployment: 74"""
        },
        {
            "stream": 5,
            "type": POST_TYPES[5],  # Motivation
            "content": """🌟 The Compound Effect of Small Wins in Tech

Every commit matters.
Every bug fix matters.
Every documentation update matters.
Every test you write matters.
Every refactor for readability matters.

Alone, each seems insignificant. But over months and years, these small wins compound exponentially.

The engineer who ships 10 tiny improvements a week outpaces the engineer who waits for the perfect solution.

Focus on consistency, not perfection.

The compounding starts today. 🚀

#EngineeringMindset #DevCulture #Growth #TechLife #StartupLife"""
        }
    ]
    
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
