# ⏰ Windows Task Scheduler Quick Start

Fast 5-minute setup for daily automated post generation.

---

## Prerequisites ✓

- [ ] 7-day manual testing completed (see DEPLOYMENT_GUIDE.md)
- [ ] Rotation logic verified (no consecutive repeats)
- [ ] All manual runs successful

---

## Step 1: Create Batch File (1 min)

Create a new file: `run-daily-posts.bat` in your project folder

**Copy this exactly:**

```batch
@echo off
cd /d C:\path\to\project
python3 fetch_ai_news_rss.py
python3 generate_posts_2post_model.py
python3 attach_images_to_posts.py
python3 update_post_history.py
echo %date% %time% - Success >> logs\execution_history.log
```

**Replace** `C:\path\to\project` with your actual folder (e.g., `C:\Users\YourName\Documents\daily-linkedin-posts`)

---

## Step 2: Open Task Scheduler (1 min)

1. Press **Windows Key + R**
2. Type: `tasksched.msc`
3. Press **Enter**

---

## Step 3: Create Task (2 min)

**Right sidebar → Create Basic Task**

| Field | Value |
|-------|-------|
| **Name** | Daily LinkedIn Posts |
| **Description** | Generates 2 posts daily at 8 AM |
| Click **Next** | – |
| **Trigger** | Select "Daily" |
| **Start date** | Tomorrow |
| **Time** | 8:00:00 AM |
| Click **Next** | – |
| **Action** | Select "Start a program" |
| **Program** | `cmd.exe` |
| **Arguments** | `/c "C:\path\to\project\run-daily-posts.bat"` |
| Click **Finish** | Done ✓ |

---

## Step 4: Test Task (1 min)

**In Task Scheduler:**

1. Find "Daily LinkedIn Posts" in the list
2. Right-click → **Run**
3. Watch for the command window (it will be fast)
4. Check files in your project folder:
   - [ ] `linkedin_posts_20260703.txt` created
   - [ ] `post_history.xlsx` updated
   - [ ] `logs/execution_history.log` shows success

---

## Done! ✅

The task will now run **every day at 8:00 AM** automatically.

---

## Verify It's Working

**Tomorrow morning (after 8 AM):**

```bash
# Windows PowerShell - Check today's posts
cat linkedin_posts_$(date +%Y%m%d).txt

# Or just look in your project folder for:
# - linkedin_posts_YYYYMMDD.txt (should be today's date)
# - post_history.xlsx (should have 2 new rows)
```

---

## Change Time (Optional)

Want to run at **6 AM** instead of 8 AM?

1. Open Task Scheduler
2. Find "Daily LinkedIn Posts"
3. Right-click → **Properties**
4. Click **Triggers** tab
5. Double-click the daily trigger
6. Change time to 6:00 AM
7. Click **OK**

---

## Troubleshooting

### Task ran but no files created

```batch
@echo off
cd /d C:\path\to\project
python3 fetch_ai_news_rss.py > logs\debug.txt 2>&1
python3 generate_posts_2post_model.py >> logs\debug.txt 2>&1
```

Then check `logs/debug.txt` for errors.

### Task won't run at all

1. Open Task Scheduler
2. Right-click "Daily LinkedIn Posts"
3. Click **Properties**
4. Check: "Run whether user is logged in or not" is ✓ checked

### "python3 not found" error

In `run-daily-posts.bat`, replace:
```batch
python3 fetch_ai_news_rss.py
```

With the full path to Python (find it with `where python`):
```batch
C:\Users\YourName\AppData\Local\Programs\Python\Python312\python.exe fetch_ai_news_rss.py
```

---

## Monitor Weekly

Every Sunday, check:

```bash
# View last 10 execution logs
Get-Content logs\execution_history.log -Tail 10

# Count rows in Excel (should be 14 after 7 days)
python3 -c "from openpyxl import load_workbook; print(f'Rows: {load_workbook(\"post_history.xlsx\").active.max_row}')"
```

---

**Next:** After 7 successful automated runs, consider GitHub Actions for cloud-based scheduling (see DEPLOYMENT_GUIDE.md)
