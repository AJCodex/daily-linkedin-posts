# 🚀 Deployment & Scheduling Guide

Complete guide for deploying the 2-post daily LinkedIn pipeline and automating daily execution.

---

## 📋 Table of Contents

1. [Local Testing (7 Days)](#local-testing-7-days)
2. [Windows Task Scheduler (Daily Automation)](#windows-task-scheduler-daily-automation)
3. [GitHub Actions (Production Cloud)](#github-actions-production-cloud)
4. [Monitoring & Troubleshooting](#monitoring--troubleshooting)
5. [Cost Analysis](#cost-analysis)

---

## Local Testing (7 Days)

### Goal
Verify the pipeline works correctly before automating. Test rotation logic, Excel tracking, and image attachment.

### Timeline
- **Day 1-4:** Manual runs to see all 4 rotation types
- **Day 5-7:** Verify Excel has 14 rows (2/day), rotation never repeats consecutively

### Step 1: One-Time Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env with OpenRouter API key
copy .env.example .env
# Edit .env and add: OPENROUTER_API_KEY=sk-or-v1-YOUR_KEY

# 3. Verify setup
python3 -c "import openpyxl, requests, dotenv; print('✓ All dependencies OK')"
```

### Step 2: Daily Manual Run (Run each morning)

```bash
# Run all 3 scripts in order
python3 fetch_ai_news_rss.py
python3 generate_posts_2post_model.py
python3 attach_images_to_posts.py
python3 update_post_history.py
```

### Step 3: Verify Each Day

| Check | Command | What to Look For |
|-------|---------|------------------|
| **Posts Generated** | `cat linkedin_posts_YYYYMMDD.txt` | 2 posts with different types |
| **Rotation Working** | `cat post-rotation-log.json` | Last entry ≠ today's type |
| **Excel Updated** | Open `post_history.xlsx` | 2 rows added today |
| **Images Attached** | Open `output/posts_YYYYMMDD/posts/posts_with_images.html` | Both posts have images |

### 7-Day Checklist

```
Day 1 (Tips & Tricks):
  ✓ Posts generated
  ✓ Excel updated (row 2)
  ✓ post-rotation-log.json shows "Tips & Tricks"
  ✓ Images attached

Day 2 (Carousel):
  ✓ Posts generated (should NOT be Tips again)
  ✓ Excel updated (row 3)
  ✓ post-rotation-log.json shows "Carousel"
  ✓ Images attached

Day 3 (Infographic):
  ✓ Different from Day 2 ✓

Day 4 (Motivation):
  ✓ Different from Day 3 ✓

Day 5 (Tips & Tricks):
  ✓ Different from Day 4 ✓
  ✓ Excel now has 10 rows total (2 × 5 days)

Day 6-7:
  ✓ Continue pattern
  ✓ Verify no consecutive repeats
  ✓ Excel has 14 rows by end of day 7
```

---

## Windows Task Scheduler (Daily Automation)

### Goal
Automatically run the pipeline every day at 8:00 AM without manual intervention.

### Prerequisites
- ✓ 7-day manual testing completed
- ✓ Verified rotation logic works correctly
- ✓ All files generate as expected

### Step 1: Create Batch File

Create file: `C:\path\to\project\run-daily-posts.bat`

```batch
@echo off
REM LinkedIn Daily Posts Pipeline
REM Runs at 8:00 AM daily via Task Scheduler

cd /d C:\path\to\project

REM Fetch latest news
python3 fetch_ai_news_rss.py

REM Generate 2 posts
python3 generate_posts_2post_model.py

REM Attach images
python3 attach_images_to_posts.py

REM Update Excel history
python3 update_post_history.py

REM Log execution
echo %date% %time% - Pipeline executed successfully >> logs\execution_history.log

REM End
exit /b 0
```

**Replace** `C:\path\to\project` with your actual project folder.

### Step 2: Create Windows Task Scheduler Job

**Method A: GUI (Easy)**

1. Open **Task Scheduler** (Windows Search → "Task Scheduler")
2. Click **Create Basic Task**
3. Fill in:
   - **Name:** "Daily LinkedIn Posts"
   - **Description:** "Generates 2 LinkedIn posts daily at 8 AM"
   - **Trigger:** Daily at 8:00 AM
   - **Action:** Start a program
   - **Program:** `C:\Windows\System32\cmd.exe`
   - **Arguments:** `/c "C:\path\to\project\run-daily-posts.bat"`
   - **Start in:** `C:\path\to\project`

4. Click **Finish**

**Method B: PowerShell (Automated)**

```powershell
# Create the task
$taskName = "Daily LinkedIn Posts"
$taskPath = "\LinkedIn\"
$scriptPath = "C:\path\to\project\run-daily-posts.bat"

$action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$scriptPath`""
$trigger = New-ScheduledTaskTrigger -Daily -At 8:00AM
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Force
Write-Host "✓ Task created: $taskName runs daily at 8:00 AM"
```

### Step 3: Verify Task Setup

1. Open Task Scheduler
2. Find "Daily LinkedIn Posts" task
3. Right-click → **Run** (test immediately)
4. Check `logs\execution_history.log` for success

### Step 4: Monitor Execution

**View Task History:**
```powershell
Get-ScheduledTaskInfo -TaskName "Daily LinkedIn Posts"
```

**View Recent Runs:**
```powershell
Get-WinEvent -LogName "Microsoft-Windows-TaskScheduler/Operational" | Where-Object { $_.Message -like "*LinkedIn*" } | Select-Object TimeCreated, Message -First 10
```

---

## GitHub Actions (Production Cloud)

### Goal
Fully automated daily post generation and potential LinkedIn scheduling via cloud.

### Prerequisites
- ✓ GitHub repository created
- ✓ All testing completed locally
- ✓ 7-day manual testing validated

### Step 1: Prepare Repository

```bash
# 1. Create GitHub repo: daily-linkedin-posts
git clone https://github.com/YOUR_USERNAME/daily-linkedin-posts.git
cd daily-linkedin-posts

# 2. Add all project files
git add .
git commit -m "Initial commit: 2-post daily LinkedIn pipeline"

# 3. Push to GitHub
git push origin main
```

### Step 2: Create GitHub Actions Workflow

Create file: `.github/workflows/daily-posts.yml`

```yaml
name: Daily LinkedIn Posts

on:
  schedule:
    # Run every day at 8:00 AM UTC (adjust timezone as needed)
    - cron: '0 8 * * *'
  workflow_dispatch:  # Allow manual trigger

jobs:
  generate-posts:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Configure environment
      run: |
        echo "OPENROUTER_API_KEY=${{ secrets.OPENROUTER_API_KEY }}" > .env
    
    - name: Fetch news
      run: python3 fetch_ai_news_rss.py
    
    - name: Generate posts
      run: python3 generate_posts_2post_model.py
    
    - name: Attach images
      run: python3 attach_images_to_posts.py
    
    - name: Update Excel
      run: python3 update_post_history.py
    
    - name: Commit and push outputs
      run: |
        git config user.name "LinkedIn Bot"
        git config user.email "bot@example.com"
        git add linkedin_posts_*.txt post_history.xlsx output/ logs/
        git commit -m "Daily posts: $(date +%Y-%m-%d)" || echo "No changes to commit"
        git push
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  notify:
    runs-on: ubuntu-latest
    needs: generate-posts
    if: always()
    
    steps:
    - name: Notify success
      if: success()
      run: echo "✓ Daily LinkedIn posts generated successfully"
    
    - name: Notify failure
      if: failure()
      run: echo "✗ Pipeline failed - check logs"
```

### Step 3: Add API Key to GitHub Secrets

1. Go to **GitHub repo → Settings → Secrets and variables → Actions**
2. Click **New repository secret**
3. Name: `OPENROUTER_API_KEY`
4. Value: Your OpenRouter API key from https://openrouter.ai
5. Click **Add secret**

### Step 4: Enable Actions

1. Go to **GitHub repo → Actions**
2. Enable GitHub Actions (button may appear if disabled)
3. Workflow file should be visible: "Daily LinkedIn Posts"

### Step 5: Test Workflow

**Manual Trigger:**
1. Go to **Actions** tab
2. Click **Daily LinkedIn Posts**
3. Click **Run workflow** button
4. Watch logs in real-time

**Scheduled Run:**
- Workflow automatically runs daily at 8:00 AM UTC
- Check **Actions** tab for execution history

---

## Monitoring & Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **"OPENROUTER_API_KEY not set"** | Check `.env` file exists and has valid key |
| **"openpyxl module not found"** | Run `pip install -r requirements.txt` |
| **"No news items fetched"** | RSS feeds may be down; check `ai_news_data.json` |
| **Rotation log shows repeats** | Algorithm bug; check `post-rotation-log.json` format |
| **Excel file locked/corrupted** | Delete `post_history.xlsx` and run again |
| **Task Scheduler not running** | Check task history in Event Viewer |

### Monitoring Checklist

**Daily (Email Alert)**
- [ ] Check `linkedin_posts_YYYYMMDD.txt` created
- [ ] Check `post_history.xlsx` has 2 new rows
- [ ] Check images attached (open HTML preview)

**Weekly**
- [ ] Verify rotation never repeats consecutively
- [ ] Check Excel has 14 rows (2 × 7 days)
- [ ] Review post quality for content drift

**Monthly**
- [ ] Analyze cost: OpenRouter dashboard → https://openrouter.ai/activity
- [ ] Check API key hasn't hit rate limits
- [ ] Backup `post_history.xlsx` to cloud storage

### Logging

**Enable detailed logging:**

Add to scripts:
```python
import logging

logging.basicConfig(
    filename=f"logs/pipeline_{datetime.now().strftime('%Y%m%d')}.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
logger.info("Pipeline started")
```

**View logs:**
```bash
tail -f logs/pipeline_20260703.log  # Linux/Mac
Get-Content -Tail 50 logs/pipeline_20260703.log  # PowerShell
```

---

## Cost Analysis

### Local Testing (7 Days)
```
OpenRouter API Cost: ~$0.07
- 2 posts/day × 1,100 tokens/post ≈ $0.01/day
- 7 days × $0.01 = $0.07 total

RSS Feed Fetching: FREE (public feeds)
Image Fetching: FREE (Unsplash API)
Excel Operations: FREE (local only)

Total: ~$0.10 (including buffer)
```

### Monthly Production
```
OpenRouter API: ~$0.30
- 2 posts/day × $0.01/day × 30 days

Infrastructure: $0 (if using local Task Scheduler)
GitHub Actions: $0 (free tier includes 2,000 minutes/month)
  - Pipeline runs ~5 minutes/day × 30 = 150 minutes

Total: ~$0.30/month (only if using API)
```

### Optimization Tips

1. **Reduce API usage:**
   - Cache news items (reuse from yesterday if low quality)
   - Generate fewer posts (switch to 1/day model)
   - Use cheaper model: `gpt-3.5-turbo` vs `gpt-4`

2. **Optimize Excel operations:**
   - Archive old posts to separate sheet (don't let single sheet grow forever)
   - Compress `post_history.xlsx` monthly

3. **GitHub Actions optimization:**
   - Run during off-peak hours (schedule at 2 AM UTC instead of 8 AM)
   - Use matrix jobs for parallel execution if scaling

---

## Deployment Timeline

| Stage | Duration | Status | Trigger for Next |
|-------|----------|--------|------------------|
| **Local Setup** | 30 min | Manual | Dependency installation complete |
| **Manual Testing** | 7 days | Manual | All 4 rotation types verified |
| **Task Scheduler** | 7 days | Automated | 7 error-free automated runs |
| **GitHub Actions** | TBD | Cloud | Production readiness validated |

---

## Quick Reference

### One-Liner Commands

```bash
# Test pipeline locally
python3 fetch_ai_news_rss.py && python3 generate_posts_2post_model.py && python3 attach_images_to_posts.py && python3 update_post_history.py

# Check today's posts
cat linkedin_posts_$(date +%Y%m%d).txt

# View rotation log
cat post-rotation-log.json

# Check Excel has expected rows
python3 -c "from openpyxl import load_workbook; wb = load_workbook('post_history.xlsx'); print(f'Total rows: {wb.active.max_row}')"
```

### Scheduled Runs

- **Task Scheduler:** Every day at 8:00 AM (configurable)
- **GitHub Actions:** Every day at 8:00 AM UTC (configurable via cron)

---

## Support & Next Steps

1. **Run manual tests first** (7 days minimum)
2. **Set up Task Scheduler** (local automation)
3. **Push to GitHub & enable Actions** (cloud automation)
4. **Monitor execution logs** (daily first week, weekly after)
5. **Scale features later** (LinkedIn API integration, Slack notifications, etc.)

**Questions?** Check logs, verify `.env` config, and review test results in `TEST_RESULTS.md`.

---

**Generated by:** LinkedIn Posts Pipeline  
**Last Updated:** 2026-07-03  
**Version:** 2.0 (2-post daily model)
