# 📦 How to Share This Package

## For Users Who Receive It

### **Step 1: Extract the Package**
```bash
# Unzip the folder to your computer
# Example: C:\Users\YourName\LinkedIn-Posts\
```

### **Step 2: Install Dependencies** (2 minutes)
```bash
cd C:\path\to\package
pip install -r requirements.txt
```

### **Step 3: Get OpenRouter API Key** (2 minutes)
1. Go to: https://openrouter.ai
2. Click **Sign Up**
3. Go to **Settings → API Keys**
4. Click **Create Key**
5. Copy the key

### **Step 4: Configure API Key** (1 minute)
```bash
# Copy the template
copy .env.example .env

# Open .env in Notepad and paste your key:
# OPENROUTER_API_KEY=sk-or-v1-YOUR_KEY_HERE
```

### **Step 5: First Run** (Manual test)
```bash
python3 fetch_ai_news_rss.py
python3 generate_posts_2post_model.py
python3 update_post_history.py
```

✅ Check results:
- `linkedin_posts_YYYYMMDD.txt` exists?
- `post_history.xlsx` has 2 rows?
- No errors in console?

### **Step 6: Automate** (Optional, after testing)
See **README.md** → "Automate" section for Windows Task Scheduler setup.

---

## **Total Time: 5 minutes setup + 2 minutes first run = 7 minutes**

---

## 📋 What Each File Does

| File | Do I Need It? |
|------|---------------|
| `generate_posts_2post_model.py` | ✅ **YES** — Main script |
| `fetch_ai_news_rss.py` | ✅ **YES** — Gets news |
| `update_post_history.py` | ✅ **YES** — Tracks in Excel |
| `.env.example` | ✅ **YES** — Config template |
| `README.md` | 📖 Reference |
| `TESTING_GUIDE.md` | 📖 If stuck |
| `API_KEYS_REQUIRED.md` | 📖 If confused about APIs |
| `content-doctrine.md` | 📖 Optional (content rules) |
| `voice-profile.md` | 📖 Optional (writing style) |

---

## 🎯 One-Liner to Start Everything

```bash
python3 fetch_ai_news_rss.py && python3 generate_posts_2post_model.py && python3 update_post_history.py
```

That's it! 🚀

---

## 🚨 Common Issues

### "ModuleNotFoundError: No module named 'openpyxl'"
```bash
pip install -r requirements.txt
```

### "OPENROUTER_API_KEY not set"
1. Edit `.env` file
2. Add your key from https://openrouter.ai

### "ConnectionError" or "API error"
1. Check internet connection
2. Verify API key in `.env`
3. Wait 30 seconds and retry

### "File not found: linkedin_posts_YYYYMMDD.txt"
Make sure you ran Step 5 completely (both fetch and generate scripts).

---

## 📞 Need Help?

1. **Setup stuck?** → Read `TESTING_GUIDE.md`
2. **API issues?** → Read `API_KEYS_REQUIRED.md`
3. **How it works?** → Read `SKILL-2POST-MODEL.md`

---

## 💾 For Package Creators

### To Share This Package:

1. **Create a ZIP file:**
   ```
   daily-linkedin-posts-pipeline.zip
   ├── README.md                    ← User starts here
   ├── PACKAGE_GUIDE.md            ← This file
   ├── generate_posts_2post_model.py
   ├── fetch_ai_news_rss.py
   ├── update_post_history.py
   ├── .env.example
   ├── requirements.txt
   ├── content-doctrine.md
   ├── voice-profile.md
   ├── TESTING_GUIDE.md
   ├── API_KEYS_REQUIRED.md
   ├── CLEANUP_SUMMARY.md
   └── daily-linkedin-posts/
       └── SKILL-2POST-MODEL.md
   ```

2. **Include these instructions:**
   - Unzip
   - `pip install -r requirements.txt`
   - Get API key at https://openrouter.ai
   - Edit `.env` with your key
   - Run: `python3 fetch_ai_news_rss.py && python3 generate_posts_2post_model.py && python3 update_post_history.py`

3. **That's it!** Users don't need anything else.

---

## 📊 Package Contents Summary

- **3 Python scripts** (all they need to run)
- **1 Config template** (.env.example)
- **1 Dependencies file** (requirements.txt)
- **5 Documentation files** (optional but helpful)

**Total size:** ~150 KB  
**Setup time:** ~5 minutes  
**First run:** ~2 minutes  
**Cost to test:** ~10 cents for 7 days

---

**Happy sharing! 🎉**
