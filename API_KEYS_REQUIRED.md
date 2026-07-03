# API Keys Required — Daily LinkedIn Posts Pipeline

## Summary: 1 API Key Needed (During Testing)

For the **2-post daily model**, you need **only 1 API key**:

| API Provider | Purpose | Cost | Status |
|---|---|---|---|
| **OpenRouter** | Generate News + rotating post (Text LLM) | ~$0.02–0.05/day | ✅ **PRIMARY** |
| Anthropic Claude | Fallback LLM (optional) | ~$0.10–0.15/day | Optional |
| Google Gemini | Alternative LLM (optional) | ~$0.02–0.04/day | Optional |

---

## OpenRouter (Recommended — Use This)

**Why OpenRouter?**
- Cheapest per-token pricing among all LLM providers
- Access to multiple models in one account (Claude, Llama, Mistral, etc.)
- No credit card required for free tier testing
- Easy API key setup

### Setup

1. **Go to:** https://openrouter.ai
2. **Sign up** (GitHub or email)
3. **Generate API key:** Settings → API Keys → Create new key
4. **Copy key** to `.env` file:

```env
OPENROUTER_API_KEY=sk-or-v1-YOUR_KEY_HERE
```

5. **Set spending limit** (optional, recommended for testing):
   - Settings → Billing → Monthly Limit: $1–5 USD

### Usage in Scripts

```python
import os
api_key = os.getenv("OPENROUTER_API_KEY")

response = requests.post(
    "https://api.openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://github.com/YOUR_USERNAME/daily-linkedin-posts",
        "X-Title": "LinkedIn Posts Pipeline"
    },
    json={
        "model": "openai/gpt-3.5-turbo",  # Cheapest option
        # OR "anthropic/claude-3.5-haiku" for better quality
        # OR "meta-llama/llama-3-70b-instruct" for longest context
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 1.0
    }
)
```

### Cost Estimate (2 Posts/Day)

- **Post 1 (News):** ~500 tokens × $0.00001 = **~$0.005**
- **Post 2 (Tips/Carousel/Infographic/Motivation):** ~600 tokens × $0.00001 = **~$0.006**
- **Total/day:** ~**$0.01** (11 cents)
- **Total/month:** ~**$0.30** (at 30 days)

✅ **OpenRouter is essentially free for daily testing.**

---

## Alternative APIs (Optional Fallback)

### Anthropic Claude

```env
ANTHROPIC_TOKEN=sk-ant-YOUR_KEY_HERE
```

**Setup:**
1. Go to: https://console.anthropic.com
2. API Keys → Create key
3. Cost: ~$0.03 per day at current token prices (3x more expensive than OpenRouter)

### Google Gemini

```env
GEMINI_API_KEY=YOUR_KEY_HERE
```

**Setup:**
1. Go to: https://ai.google.dev
2. Get API Key → Create new API key
3. Cost: Similar to OpenRouter, but slightly less competitive

---

## .env File Template

```env
# REQUIRED (pick one)
OPENROUTER_API_KEY=sk-or-v1-YOUR_KEY_HERE

# Optional (fallback only)
ANTHROPIC_TOKEN=sk-ant-YOUR_KEY_HERE
GEMINI_API_KEY=YOUR_KEY_HERE

# Storage (for testing phase — optional, no cloud upload)
SLACK_BOT_TOKEN=
SLACK_CHANNEL_ID=
```

---

## How to Add API Key to Scripts

### In Python files:

```python
import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env file

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY not set in .env file")
```

### In Node.js files (if needed):

```javascript
require('dotenv').config();

const apiKey = process.env.OPENROUTER_API_KEY;

if (!apiKey) {
    throw new Error("OPENROUTER_API_KEY not set in .env file");
}
```

---

## Testing Your API Key

### Quick test (Python):

```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

response = requests.post(
    "https://api.openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://github.com/test",
    },
    json={
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "Say 'Hello'"}]
    }
)

print(response.status_code)
print(response.json())
```

**Expected output:**
```
200
{'choices': [{'message': {'content': 'Hello'}}], ...}
```

If you get `401 Unauthorized`, double-check your API key in `.env`.

---

## Monitoring Usage

### OpenRouter Dashboard

Go to: https://openrouter.ai/activity

You'll see:
- Requests made (should increase by 2/day)
- Tokens used
- Cost in USD
- Model breakdown

### Example (1 week):

| Day | News Post | Secondary Post | Total Tokens | Cost |
|-----|-----------|---|---|---|
| Day 1 (News + Tips) | 520 tokens | 450 tokens | 970 | $0.01 |
| Day 2 (News + Carousel) | 520 tokens | 580 tokens | 1,100 | $0.01 |
| Day 3 (News + Infographic) | 520 tokens | 640 tokens | 1,160 | $0.01 |
| Day 4 (News + Motivation) | 520 tokens | 520 tokens | 1,040 | $0.01 |
| Day 5 (News + Tips) | 520 tokens | 450 tokens | 970 | $0.01 |
| **Weekly Total** | | | **~5,240** | **~$0.05** |

---

## No API Key Needed For

These do NOT require paid APIs:
- ✅ RSS feed fetching (`fetch_ai_news_rss.py`) — free, uses public RSS URLs
- ✅ Excel tracking (`update_post_history.py`) — local file, no API
- ✅ Carousel/Infographic rendering (`cap_infographic_today.js`) — local HTML/Puppeteer, no API
- ✅ Task Scheduler (Windows) — local scheduling, no API

---

## During Production (After Testing)

Once you move to **GitHub Actions for scheduling:**

1. Store API key in **GitHub Secrets** (not in `.env`)
2. GitHub Actions will use: `secrets.OPENROUTER_API_KEY`
3. No exposure of API key in the repository

---

## Summary Checklist

- [ ] Create account on https://openrouter.ai
- [ ] Generate API key from Settings → API Keys
- [ ] Copy `.env.example` → `.env` and add key
- [ ] Run test script above to verify key works
- [ ] Proceed with `generate_posts_via_openrouter.py`
- [ ] Check usage dashboard weekly to monitor costs

**You're all set! Proceed to generate 2 posts with** `python3 generate_posts_via_openrouter.py`
