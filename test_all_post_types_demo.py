#!/usr/bin/env python3
"""
Demo test script - generates all 5 post types for testing when API is unavailable.
Perfect for local testing and validation of the full pipeline.
"""

import json
import os
import datetime

def create_test_posts():
    """Create demo posts for all 5 types"""
    
    posts = [
        {
            "stream": "1",
            "type": "News",
            "content": """Microsoft Announces New Azure AI Services for Enterprise Deployments

Microsoft has unveiled the latest advancements in Azure AI services, focusing on enterprise-grade machine learning capabilities. These new tools are designed to help organizations streamline their AI workflows and accelerate digital transformation initiatives.

Key highlights include:
- Enhanced model training acceleration
- Improved data privacy controls
- Better integration with existing enterprise systems
- Advanced monitoring and governance features

The announcement comes as businesses increasingly recognize the value of adopting AI technologies. According to recent data, organizations leveraging AI report 30% improvement in operational efficiency.

For enterprises looking to scale their AI initiatives, these updates represent a significant step forward in democratizing artificial intelligence.

#Azure #AI #Microsoft #Enterprise #MachineLearning"""
        },
        {
            "stream": "2", 
            "type": "Tips & Tricks",
            "content": """5 Quick Wins I Use Daily for Better AI Productivity

Over the past few months, I've discovered some game-changing productivity hacks when working with AI tools. Here are my top 5 that I recommend to everyone:

1. Prompt Engineering Checklists - I create reusable templates for common tasks. Saves me 15 mins daily.

2. Batch Processing - Process multiple requests together instead of one-by-one. About 3x faster.

3. Context Windows - Keep context organized and concise. Prevents token waste and improves accuracy.

4. Version Control - Track which prompts/models produced your best results. Sounds obvious but game-changing.

5. Feedback Loops - Build quick feedback mechanisms to validate outputs. This caught 80% of errors early.

The key insight: small systematic improvements compound. Start with one, master it, then add more.

#Productivity #AI #Tips #WorkSmarter"""
        },
        {
            "stream": "3",
            "type": "Carousel",
            "content": """Slide 1: AI Career Roadmap 2026 - Your Path to the Future
Thinking about transitioning into AI? Here's a reality check on what the market actually wants and where to focus your efforts for maximum impact.

Slide 2: Foundation Layer - Core Skills You Need
Start here: Python, Statistics, Linear Algebra. These aren't optional. They form the foundation for everything else. Spend 2-3 months building solid fundamentals.

Slide 3: ML Engineering - The Practical Skills
Machine learning fundamentals, model training, evaluation metrics. Kaggle competitions are your friend here. Real-world messy data teaches you more than theory.

Slide 4: Deep Learning - Going Deeper
Neural networks, transformers, computer vision. This is where things get interesting. Most jobs want practical deep learning skills, not just theory.

Slide 5: Production Skills - The Real World
Deployment, scaling, monitoring, debugging. Most bootcamps skip this. Real companies need engineers who can ship. Learn Docker, APIs, cloud platforms.

Slide 6: Specialization - Pick Your Path
Computer Vision? NLP? Reinforcement Learning? Agents? Pick one and go deep. Market rewards specialists over generalists.

Slide 7: The Reality Check
It takes 12-18 months of consistent work to become job-ready. No shortcuts. But the demand is real and salaries reflect that. Start now, be patient, stay consistent."""
        },
        {
            "stream": "4",
            "type": "Infographic",
            "content": """AI Skills That Actually Get Hired (2026 Data)

📊 Top In-Demand AI Skills:
- Python Programming: 92% of AI job postings
- Machine Learning: 85% of roles
- Deep Learning/Neural Networks: 78%
- Data Analysis: 75%
- PyTorch/TensorFlow: 68%

💼 Market Demand Growth:
- AI Engineer roles: +45% year-over-year
- ML Engineer roles: +38% year-over-year
- Data Scientist roles: +25% year-over-year

💰 Salary Insights:
- Entry-level AI Engineer: $110K-140K
- Mid-level: $150K-200K
- Senior/Staff: $220K-350K

⏱️ Time to Job-Ready:
- With bootcamp: 3-6 months
- With degree: 2 years
- Self-taught intensive: 12-18 months

🎯 Hiring Trends:
- 60% value portfolio/projects over credentials
- 45% hire for potential, train on specifics
- Portfolio projects: 3-5 significant projects

📈 Growth Forecast 2026-2027:
AI roles projected +50% growth overall"""
        },
        {
            "stream": "5",
            "type": "Motivation",
            "content": """The Compound Effect of 1% Daily Improvement

I learned this the hard way over the last year working with AI. It's not about the big breakthrough. It's about the tiny improvements that stack.

Here's what I mean:

Every day, I spent just 30 mins learning something new about AI. Not a course, not a whole project. Just 30 mins. On some days, just reading a paper. On others, tweaking a model parameter.

In month 1: Barely noticeable. Felt slow.
In month 3: People started noticing I could explain concepts better.
In month 6: Got asked to lead a project.
In month 12: Completely different career trajectory.

The math is simple: 1.01^365 = 37.78

But the psychology is harder. Your brain wants the big win. It doesn't celebrate the small daily win. So you quit before the magic happens.

Here's my insight: The people winning in AI aren't necessarily smarter. They're more consistent.

Start small. Stay consistent. Compound your efforts.

Your future self will thank you.

#Growth #Consistency #AICareer #PersonalDevelopment"""
        }
    ]
    
    return posts

def main():
    print("🧪 DEMO TEST: Generating all 5 post types...\n")
    
    posts = create_test_posts()
    
    # Save test posts
    today = datetime.date.today()
    output_file = f"test_posts_{today.strftime('%Y%m%d')}.txt"
    
    print(f"📝 Creating test posts...")
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, post in enumerate(posts, 1):
            f.write(f"{'='*80}\n")
            f.write(f"STREAM: {post['stream']}\n")
            f.write(f"TYPE: {post['type']}\n")
            f.write(f"{'='*80}\n")
            f.write(f"{post['content']}\n\n")
    
    print(f"✅ Created {len(posts)} test posts in: {output_file}")
    print("\n📋 Next steps:")
    print(f"1. python attach_images_to_posts.py")
    print(f"2. python generate_visual_posts.py")
    print(f"3. python post_to_linkedin_zernio.py")
    print(f"\n📌 This will post all 5 types to LinkedIn for testing!")
    
    return output_file

if __name__ == "__main__":
    main()
