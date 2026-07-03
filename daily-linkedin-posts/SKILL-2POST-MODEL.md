---
name: daily-linkedin-posts-2post
description: Generates 2 LinkedIn posts daily (News + 1 rotating type). Pattern cycles through Tips, Carousel, Infographic, and Motivation. Never repeats same secondary type consecutively. Outputs to local folder only.
---

# Daily LinkedIn Content — 2 Posts (Rotating Type)

Generate today's 2-post batch and save to `linkedin_posts_YYYYMMDD.txt`. Update Excel history after each run.

**Post pattern (repeats daily):**
- Day 1: News + Tips & Tricks
- Day 2: News + Carousel (7 slides + PDF)
- Day 3: News + Infographic (1080×1080 PNG)
- Day 4: News + Motivation/Productivity
- Day 5: News + Tips & Tricks (repeats)

---

## STEP 0 — Load doctrine and voice

```bash
cat ./content-doctrine.md
cat ./voice-profile.md 2>/dev/null
```

North star: `content-doctrine.md` defines the Microsoft AI niche and topic filter (Relevance, Stakes, Accuracy, Practicality).

---

## STEP 1 — Determine today's post type

```python
import json, datetime, os

post_types = ["Tips & Tricks", "Carousel", "Infographic", "Motivation/Productivity"]
rotation_log_path = "./post-rotation-log.json"

# Load rotation log to prevent consecutive repeats
log = json.load(open(rotation_log_path)) if os.path.exists(rotation_log_path) else []

# Get last posted secondary type
last_type = log[-1]["type"] if log else None

# Cycle through types (skip last one if it was just used)
for post_type in post_types:
    if post_type != last_type:
        today_type = post_type
        break

print(f"Today's secondary post type: {today_type}")

# Save to log
today = str(datetime.date.today())
log.append({"date": today, "type": today_type})
log = log[-30:]  # Keep last 30 days
json.dump(log, open(rotation_log_path, 'w'), indent=2)
```

Output example:
```
Today's secondary post type: Tips & Tricks
```

**Note:** If today is Friday/weekend and you want to skip carousel/infographic generation, manually change `today_type` to "Tips & Tricks" or "Motivation/Productivity".

---

## STEP 2 — Fetch Microsoft AI news

```bash
python3 fetch_ai_news_rss.py
```

This writes `./ai_news_data.json` with the latest items from:
- Microsoft Tech Community - Azure AI
- Azure Updates Blog
- Microsoft AI Blog
- Microsoft 365 Blog
- GitHub Copilot Blog

---

## STEP 3 — Load deduplication logs

If today's type is **Carousel** or **Infographic**, load banned topics:

```bash
# Only if today_type == "Carousel"
cat ./carousel-hook-log.json 2>/dev/null || echo "[]"

# Only if today_type == "Infographic"
cat ./infographic-run-log.json 2>/dev/null || echo "[]"
```

Extract banned topics/hooks from last 7–14 entries to avoid repeats.

---

## STEP 4 — Generate 2 posts

### POST 1 — News (150–250 words, always)

Pick the single most significant Microsoft AI / Azure / Copilot story from today's news feed.
- Third-person observer voice
- Structure: Hook → What happened → Why it matters → Source reference → Question CTA
- Include source URL (Microsoft Blog or Azure Updates)
- No em-dashes, max 2 hashtags

### POST 2 — Rotating Type (varies daily)

#### IF TODAY IS "TIPS & TRICKS" (100–200 words)

Write one practical, actionable tip about Power Platform, Azure, Copilot Studio, or AI Search.
- First-person allowed ("Here is what I do...")
- Numbered steps (max 5)
- Must be replicable today
- End: "Try this and let me know how it goes."

#### IF TODAY IS "CAROUSEL" (7 slides + caption)

Pick a deep-dive Microsoft AI topic. Use `./skills/branded-carousel/FORMATS.md`.

**Slide structure:**
- Slide 1: Hook (6–8 words, curiosity gap)
- Slides 2–6: One key insight per slide, max 2 sentences each
- Slide 7: Summary + CTA

Caption: 50–80 words. Hook + what reader learns + question + CTA.

#### IF TODAY IS "INFOGRAPHIC" (1080×1080 PNG + caption)

Use WebSearch to find one Microsoft/Azure dataset (2025–2026) with 6–10 data points. Must NOT overlap with BANNED_INFOGRAPHIC_TOPICS.

Good targets:
- Microsoft Work Trend Index (Copilot adoption, productivity gains)
- Azure service adoption by industry
- Power Platform usage stats (citizen developer growth)
- Microsoft 365 Copilot ROI (hours saved)
- GitHub Copilot developer productivity
- Microsoft AI Foundry model usage

Pick format from `./skills/illustration-formats/SKILL.md`:
- Ranked list → `RANKED_BARS`
- Parts of whole → `DONUT_BREAKDOWN`
- Timeline → `TIMELINE_SHIFT`
- Head-to-head → `COMPARISON_SPLIT`
- Single big stat → `HERO_NUMBER`

**Caption (60–100 words):**
- Third-person voice
- Hook: most surprising number
- One context sentence
- One implication for reader
- Question CTA

**Design:**
- Background: `#F0F4FF` (light Microsoft blue-grey)
- Accent: `#0078D4` (Microsoft blue)
- Text: `#1A1A1A` (dark)
- Font: Inter
- Footer: "Abhinav Jain | Microsoft AI"

#### IF TODAY IS "MOTIVATION/PRODUCTIVITY" (150–250 words)

Write a practical AI productivity hack using Microsoft tools (Copilot, Power Automate, Teams, Loop, OneNote AI).
- First-person allowed
- Must include: specific tool + specific task it replaces + time saved (specific number)
- End: "To do this yourself: [1–3 steps]"
- CTA: "What is one thing you are still doing manually that Copilot could handle?"

---

## STEP 5 — Save posts file

```bash
python3 -c "
import datetime
today = datetime.date.today().strftime('%Y%m%d')
filename = f'linkedin_posts_{today}.txt'
print(filename)
"
```

Format:
```
==================================================
STREAM 1 — NEWS
==================================================
[post text]

Source: [URL]
Word count: [N]

==================================================
STREAM 2 — [TODAY'S TYPE]
==================================================
[post text]

Word count: [N]

[For carousel/infographic, note media file names]
```

---

## STEP 6 — Generate visual assets (if needed)

### If today_type == "Carousel":

```bash
cd carousel-routine && node cap_infographic_today.js && cd ..
```

Output: `./linkedin-infographic-$(date +%Y%m%d).png`

Update carousel-hook-log:
```python
import json, datetime
log = json.load(open("./carousel-hook-log.json")) if os.path.exists("./carousel-hook-log.json") else []
log.append({"date": str(datetime.date.today()), "hook": "YOUR_HOOK_HERE", "topic": "Carousel Topic"})
log = log[-30:]
json.dump(log, open("./carousel-hook-log.json", 'w'), indent=2)
```

### If today_type == "Infographic":

1. Generate carousel PDF:
```bash
cd carousel-routine
node screenshot_all.js
node compile_pdf.js
cd ..
```

Output: `./carousel-routine/output/$(date +%Y-%m-%d)/carousel-branded/*.pdf`

2. Update infographic-run-log:
```python
import json, datetime
log = json.load(open("./infographic-run-log.json")) if os.path.exists("./infographic-run-log.json") else []
log.append({"date": str(datetime.date.today()), "topic": "YOUR_TOPIC", "format": "RANKED_BARS"})
log = log[-30:]
json.dump(log, open("./infographic-run-log.json", 'w'), indent=2)
```

### If today_type == "Tips & Tricks" or "Motivation/Productivity":

No visual assets needed. Skip to Step 7.

---

## STEP 7 — Update Excel history

```bash
python3 update_post_history.py
```

This appends 2 rows to `post_history.xlsx`:
- Row 1: News post metadata
- Row 2: [Today's type] post metadata

Columns: Date | Stream | Post Text Preview | Full Text | Source URL | Word Count | Format | Notes

---

## STEP 8 — Verify outputs

```bash
YYYYMMDD=$(date +%Y%m%d)
echo "✓ Posts file:"
ls -lh linkedin_posts_${YYYYMMDD}.txt

echo ""
echo "✓ Excel history:"
ls -lh post_history.xlsx

if [ -f "linkedin-infographic-${YYYYMMDD}.png" ]; then
  echo "✓ Infographic PNG:"
  ls -lh linkedin-infographic-${YYYYMMDD}.png
fi

if [ -f "carousel-routine/output/*/carousel-branded/*.pdf" ]; then
  echo "✓ Carousel PDF:"
  ls -lh carousel-routine/output/*/carousel-branded/*.pdf
fi
```

---

## AUTOMATION: Windows Task Scheduler

To run this every day at 8:00 AM on your laptop (testing phase):

1. **Create a batch file** (`run-daily-posts.bat`):

```batch
@echo off
cd C:\Projects\WorkSpaceAJ\daily-linkedin-posts-pipeline
python3 generate_posts_via_openrouter.py
python3 update_post_history.py
echo Done - %date% %time% >> daily-posts-log.txt
```

2. **Add to Task Scheduler:**
   - Open Task Scheduler (search "Task Scheduler" in Windows)
   - Click "Create Basic Task"
   - Name: "Daily LinkedIn Posts"
   - Trigger: Daily at 8:00 AM
   - Action: Start a program → Select `run-daily-posts.bat`
   - Check "Run whether user is logged in or not"
   - Save

3. **Verify:**
   - `daily-posts-log.txt` shows timestamp each time it runs
   - `linkedin_posts_YYYYMMDD.txt` created each morning
   - `post_history.xlsx` has new rows

---

## Manual Run (Testing)

```bash
# Navigate to project folder
cd C:\Projects\WorkSpaceAJ\daily-linkedin-posts-pipeline

# Run the pipeline
python3 generate_posts_via_openrouter.py
python3 update_post_history.py

# Check outputs
ls -la linkedin_posts_*.txt
cat linkedin_posts_$(date +%Y%m%d).txt | head -20
```

---

## File Outputs (Local Folder Only)

All files stay in `C:\Projects\WorkSpaceAJ\daily-linkedin-posts-pipeline`:

| File | Generated | Frequency |
|------|-----------|-----------|
| `linkedin_posts_YYYYMMDD.txt` | Always | Daily |
| `post_history.xlsx` | Updated | Daily (appends 2 rows) |
| `post-rotation-log.json` | Updated | Daily |
| `linkedin-infographic-YYYYMMDD.png` | Conditionally | When today_type == "Infographic" |
| `carousel-routine/output/.../carousel.pdf` | Conditionally | When today_type == "Carousel" |
| `carousel-hook-log.json` | Updated | When carousel generated |
| `infographic-run-log.json` | Updated | When infographic generated |

**No Git push or cloud upload during testing phase.**

---

## Next Steps (After Testing)

1. ✅ Verify 2 posts generate correctly for 4 days (cycle through all types)
2. ✅ Check Excel history accumulates properly
3. ✅ Confirm PDFs/PNGs are created only on relevant days
4. ✅ Test Windows Task Scheduler for 1 week
5. ⏳ Once stable: Push to GitHub and set up Actions (future)

