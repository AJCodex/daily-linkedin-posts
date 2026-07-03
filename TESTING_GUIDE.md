# Quick Start Guide — 2-Post Daily Model (Testing Phase)

> **Goal:** Generate 2 LinkedIn posts daily (News + rotating type) and save locally to Excel. No Git push yet.

---

## ✅ Prerequisites (5 min)

### 1. Install Python Dependencies

```bash
cd C:\Projects\WorkSpaceAJ\daily-linkedin-posts-pipeline

pip install --upgrade pip
pip install openpyxl requests python-dotenv
```

**Verify:**
```bash
python -c "import openpyxl, requests; print('✓ All dependencies installed')"
```

### 2. Get OpenRouter API Key (2 min)

1. Go to: https://openrouter.ai
2. Sign up (GitHub or email)
3. Settings → API Keys → **Create new key**
4. Copy the key (looks like: `sk-or-v1-...`)

### 3. Create .env File

```bash
# Navigate to project folder
cd C:\Projects\WorkSpaceAJ\daily-linkedin-posts-pipeline

# Copy the template
copy .env.example .env

# Edit .env and add your OpenRouter key
```

**Edit `.C:\Projects\WorkSpaceAJ\daily-linkedin-posts-pipeline\.env`:**
```env
OPENROUTER_API_KEY=sk-or-v1-YOUR_KEY_HERE
```

**Verify:**
```bash
type .env
```

You should see your API key there (keep it secret!).

---

## 🚀 First Run (Manual)

### Step 1: Fetch RSS News

```bash
python3 fetch_ai_news_rss.py
```

**Expected output:**
```
✓ Fetched 5 news items from Microsoft sources
✓ Saved ai_news_data.json
```

**File created:** `ai_news_data.json` (contains today's Microsoft AI news)

### Step 2: Generate 2 Posts

```bash
python3 generate_posts_2post_model.py
```

**Expected output:**
```
============================================================
LinkedIn Daily Posts Generator (2-Post Model)
============================================================

✓ Today's post types: News + Tips & Tricks
✓ Fetched 5 news items
📝 Generating News post...
📝 Generating Tips & Tricks post...

✅ Posts saved to: linkedin_posts_20260703.txt

Summary:
  Post 1: News (187 words)
  Post 2: Tips & Tricks (156 words)

Next step: python3 update_post_history.py
```

**File created:** `linkedin_posts_20260703.txt` (2 posts for today)

### Step 3: Check Posts File

```bash
# View the posts
type linkedin_posts_20260703.txt

# Should show:
# ==================================================
# STREAM 1 — NEWS
# ==================================================
# [Post text about Microsoft AI/Azure news]
# ...
# ==================================================
# STREAM 2 — TIPS & TRICKS
# ==================================================
# [Post text with practical tip]
```

### Step 4: Update Excel History

```bash
python3 update_post_history.py
```

**Expected output:**
```
✓ Extracted 2 posts from linkedin_posts_20260703.txt
  - Stream 1: News (187 words)
  - Stream 2: Tips & Tricks (156 words)
✓ Updated post_history.xlsx with 2 posts from 2026-07-03
  File has 2 total post records (Excel row 3 is last entry)
✓ All posts stored locally (no cloud upload)
```

**File created/updated:** `post_history.xlsx` (Excel file with post history)

### Step 5: Verify Excel File

Open `post_history.xlsx` in Excel:
- Column A: Date (2026-07-03)
- Column B: Stream (News | Tips & Tricks)
- Column C: Post Text Preview (first 500 chars)
- Column D: Full Post Text
- Column E: Source URL
- Column F: Word Count
- Etc.

---

## 📅 The 4-Day Rotation

After running the generator 4 consecutive days, you'll see the rotation cycle:

| Day | Post 2 Type | Generated File | Visual Assets |
|-----|---|---|---|
| Day 1 | Tips & Tricks | `linkedin_posts_20260703.txt` | None (text only) |
| Day 2 | Carousel | `linkedin_posts_20260704.txt` | `carousel-routine/output/.../carousel.pdf` |
| Day 3 | Infographic | `linkedin_posts_20260705.txt` | `linkedin-infographic-20260705.png` |
| Day 4 | Motivation/Productivity | `linkedin_posts_20260706.txt` | None (text only) |
| Day 5 | Tips & Tricks (repeats) | `linkedin_posts_20260707.txt` | None (text only) |

Check rotation log:
```bash
type post-rotation-log.json
```

Output:
```json
[
  {"date": "2026-07-03", "type": "Tips & Tricks"},
  {"date": "2026-07-04", "type": "Carousel"},
  {"date": "2026-07-05", "type": "Infographic"},
  {"date": "2026-07-06", "type": "Motivation/Productivity"},
  {"date": "2026-07-07", "type": "Tips & Tricks"}
]
```

---

## ⏰ Automated Scheduling (Windows Task Scheduler)

Once manual testing is successful, set up automatic daily runs:

### Option A: Run Every Morning at 8:00 AM

1. **Create batch file** (`C:\run-posts.bat`):

```batch
@echo off
cd /d C:\Projects\WorkSpaceAJ\daily-linkedin-posts-pipeline
python3 fetch_ai_news_rss.py
python3 generate_posts_2post_model.py
python3 update_post_history.py
echo %date% %time% - Posts generated successfully >> daily-posts-log.txt
```

2. **Add to Windows Task Scheduler:**
   - Open Task Scheduler (search "Task Scheduler" in Windows)
   - Right-click Task Scheduler Library → Create Basic Task
   - **Name:** "Daily LinkedIn Posts"
   - **Description:** "Generate 2 LinkedIn posts daily"
   - **Trigger:** Daily at 8:00 AM (or your preferred time)
   - **Action:** Start a program
     - Program/script: `C:\run-posts.bat`
     - Leave "Add arguments" blank
   - **Conditions:** 
     - ☐ Uncheck "Stop the task if it runs longer than..."
     - Check "Wake the computer to run this task" (optional)
   - **Settings:**
     - ☑ "Run the task as soon as possible after a scheduled start is missed"
     - ☑ "If the task fails, restart every 5 minutes"
     - Attempt to restart up to 3 times
   - **Click OK** and enter your Windows password

3. **Verify it's running:**
   - Open `daily-posts-log.txt` each morning to confirm execution
   - Check for new `linkedin_posts_YYYYMMDD.txt` files
   - Open `post_history.xlsx` to see new rows appended

### Option B: Manual Run Anytime

Just run this command:
```bash
python3 generate_posts_2post_model.py && python3 update_post_history.py
```

---

## 🔍 Troubleshooting

### Error: "OPENROUTER_API_KEY not set in .env file"

**Solution:**
1. Check `.env` file exists: `type .env`
2. Verify key is there: `OPENROUTER_API_KEY=sk-or-v1-...`
3. No spaces before/after `=`
4. Save file and run again

### Error: "API Error: 401 Unauthorized"

**Solution:**
1. Your OpenRouter key is invalid or expired
2. Go to https://openrouter.ai/activity and check key
3. Generate a new key and update `.env`
4. Test with:
   ```bash
   python3 -c "
   import os, requests
   from dotenv import load_dotenv
   load_dotenv()
   key = os.getenv('OPENROUTER_API_KEY')
   print(f'Key set: {bool(key)}')
   "
   ```

### Error: "openpyxl not installed"

**Solution:**
```bash
pip install openpyxl
python3 update_post_history.py
```

### Error: "linkedin_posts_YYYYMMDD.txt not found"

**Solution:**
1. Make sure you ran `generate_posts_2post_model.py` first
2. Check today's date is correct: `date`
3. List files in folder: `dir linkedin_posts_*.txt`

### Carousel/Infographic Not Generated

**Expected behavior:** Only generated on their rotation days (Day 2 and Day 3 of cycle).
- Day 1 (Tips & Tricks): Text only
- Day 2 (Carousel): Text + PDF generated (check `carousel-routine/output/`)
- Day 3 (Infographic): Text + PNG generated (check `linkedin-infographic-YYYYMMDD.png`)
- Day 4 (Motivation): Text only

---

## 💾 File Structure After Testing

After 1 week of daily runs:

```
daily-linkedin-posts-pipeline/
  ├── linkedin_posts_20260703.txt    (Day 1 - 2 posts)
  ├── linkedin_posts_20260704.txt    (Day 2 - 2 posts)
  ├── linkedin_posts_20260705.txt    (Day 3 - 2 posts)
  ├── linkedin_posts_20260706.txt    (Day 4 - 2 posts)
  ├── linkedin_posts_20260707.txt    (Day 5 - 2 posts)
  ├── post_history.xlsx              (Excel: 10 rows of posts)
  ├── ai_news_data.json              (Today's RSS news)
  ├── post-rotation-log.json         (Rotation state)
  ├── carousel-hook-log.json         (Carousel history - optional)
  ├── infographic-run-log.json       (Infographic history - optional)
  ├── linkedin-infographic-20260705.png  (Only on Day 3)
  ├── carousel-routine/output/...    (PDF files - only on Day 2)
  └── daily-posts-log.txt            (Task Scheduler log)
```

---

## ✅ Testing Checklist (7 Days)

Run this checklist after the first week:

- [ ] **Day 1:** `generate_posts_2post_model.py` generates News + Tips post
- [ ] **Day 1:** `post_history.xlsx` has 2 rows (headers + 2 posts)
- [ ] **Day 1:** Check `post-rotation-log.json` shows "Tips & Tricks"
- [ ] **Day 2:** `generate_posts_2post_model.py` generates News + Carousel post
- [ ] **Day 2:** Carousel PDF created in `carousel-routine/output/`
- [ ] **Day 2:** `post_history.xlsx` has 4 rows total (2 more posts added)
- [ ] **Day 3:** `generate_posts_2post_model.py` generates News + Infographic post
- [ ] **Day 3:** Infographic PNG created (`linkedin-infographic-YYYYMMDD.png`)
- [ ] **Day 3:** `post_history.xlsx` has 6 rows total
- [ ] **Day 4:** Motivation/Productivity post generated (no visuals)
- [ ] **Day 5:** Tips & Tricks post generated again (rotation repeats)
- [ ] **Task Scheduler:** Runs successfully without manual intervention
- [ ] **Excel history:** Growing properly, dates and streams correct
- [ ] **No errors** in daily-posts-log.txt

---

## Next: Deploying to GitHub (After Testing)

Once testing is complete and stable (1+ week):

1. Update `.github/workflows/daily-posts.yml` with GitHub Actions workflow
2. Push repo to GitHub
3. Add GitHub Secrets (API keys)
4. Enable workflow
5. Delete local Task Scheduler task

**But for now:** Local testing only ✓

---

## API Cost During Testing

**Example:** 7 days of posts

- Day 1-7: 2 posts/day = **14 posts**
- Average tokens: ~550 per post
- **Total tokens:** ~7,700
- **Cost:** ~$0.08–0.10 USD (10 cents)

✅ **Essentially free.**

---

## Questions?

Check these files:
- `API_KEYS_REQUIRED.md` — API key setup details
- `daily-linkedin-posts/SKILL-2POST-MODEL.md` — Full pipeline steps
- `content-doctrine.md` — What topics are allowed
- `voice-profile.md` — Writing style guidelines

Ready? **Run your first posts now:**

```bash
python3 fetch_ai_news_rss.py
python3 generate_posts_2post_model.py
python3 update_post_history.py
```

