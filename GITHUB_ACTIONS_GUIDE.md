# 🚀 Running GitHub Actions - Quick Guide

## Step-by-Step: Trigger Pipeline on GitHub

### 1️⃣ Open GitHub Actions
```
https://github.com/AJCodex/daily-linkedin-posts/actions
```

### 2️⃣ Select "Daily LinkedIn Posts" Workflow
- On the left sidebar, click: **Daily LinkedIn Posts**
- Button: **Run workflow** (top right)

### 3️⃣ Trigger Workflow
- Click dropdown: **Use workflow from** → **main**
- Button: **Run workflow** (green button)
- Status will show: 🟠 "Queued" → 🟡 "In progress" → ✅ "Completed"

### 4️⃣ Monitor Execution (2-3 minutes)
Click on the workflow run to see:
- ✅ Setup Python
- ✅ Install dependencies  
- ✅ Generate test posts (5 randomized)
- ✅ Attach images (Unsplash URLs)
- ✅ Generate visual composites (PNG files)
- ✅ Post to LinkedIn (Zernio API)

### 5️⃣ Check Zernio/LinkedIn (5 minutes after completion)

**Expected:**
- 📱 **5 new posts** appear in drafts/scheduled
- 📸 **All 5 have images** in media section
- 🎯 **Different content** each run (randomized)
- 🗓️ **Scheduling:**
  - News: 8:00 AM UTC (drafted)
  - Tips: 4:00 PM UTC (drafted)
  - Carousel/Infographic/Motivation: Immediate (posted)

---

## ⚙️ Environment Configuration

GitHub Secrets already configured:
- ✅ `ZERNIO_API_KEY` 
- ✅ `LINKEDIN_ACCOUNT_ID`
- ⚠️ `OPENROUTER_API_KEY` (optional - uses defaults if missing)

---

## 📊 What Gets Posted

### Stream 1: News (8 AM)
Randomized from 5 companies:
- Microsoft, Google, OpenAI, Meta, DeepSeek

### Stream 2: Tips (4 PM)
Randomized from 5 categories:
- RAG Pipelines, Prompt Engineering, Model Optimization, API Design, Testing Strategies

### Stream 3: Carousel (Now)
Randomized from 3 topics:
- Prompt Engineering Mastery, LLM Fine-Tuning Guide, Vector Database Essentials

### Stream 4: Infographic (Now)
Randomized from 4 datasets:
- LLM Adoption by Industry, AI Spending Trends, Model Performance Metrics, Cloud Adoption Rates

### Stream 5: Motivation (Now)
Randomized from 3 messages:
- Building in Public, Learning Together, Innovation Mindset

---

## 🔍 Verification Checklist

- [ ] GitHub Actions workflow completed ✅
- [ ] No errors in logs
- [ ] 5 posts created with post IDs
- [ ] Zernio/LinkedIn shows 5 new items
- [ ] All 5 have images (📸)
- [ ] Images are different each run
- [ ] Scheduling times correct (8 AM, 4 PM UTC)

---

## 🆘 Troubleshooting

**No posts appear?**
- Check secrets are set: Settings → Secrets → Actions
- Verify API keys are valid (no extra spaces)

**Posts without images?**
- Check Zernio media section specifically
- Verify Unsplash URLs are accessible (try in browser)

**Same images each time?**
- That's actually correct! Unsplash URLs are stable
- **Different is the post CONTENT** (randomized from libraries)

**Workflow failed?**
- Click workflow → see specific error
- Check logs for Python errors or API issues

---

## 📈 Expected Output Structure

```
✓ Daily LinkedIn Posts Workflow
  ├─ Generate Test Posts          ✅ (5 posts, randomized content)
  ├─ Attach Images                ✅ (Unsplash URLs)
  ├─ Generate Visual Composites   ✅ (PNG files for reference)
  └─ Post to LinkedIn             ✅ (5/5 successful)
     ├─ Stream 1: News [ID:...]   📸 with image
     ├─ Stream 2: Tips [ID:...]   📸 with image
     ├─ Stream 3: Carousel [ID:...]  📸 with image
     ├─ Stream 4: Infographic [ID:...]  📸 with image
     └─ Stream 5: Motivation [ID:...]  📸 with image
```

---

**✅ All systems ready! Hit "Run workflow" and watch your posts appear.** 🎉
