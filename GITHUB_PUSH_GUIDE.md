# GitHub Push Instructions for AJCodex User

## Quick Setup (3 steps)

### Step 1: Create Empty Repo on GitHub
1. Go to https://github.com/new
2. Fill in:
   - **Repository name:** `daily-linkedin-posts`
   - **Description:** "Daily automated LinkedIn posts using free Gemma model"
   - **Visibility:** Public (recommended for portfolio) or Private (your choice)
3. ⚠️ **Do NOT initialize with README, .gitignore, or license**
4. Click **Create repository**

### Step 2: Copy the HTTP URL
GitHub will show you:
```
https://github.com/AJCodex/daily-linkedin-posts.git
```

Copy this exact URL.

### Step 3: Push from Local

Replace `YOUR_GITHUB_TOKEN` with your personal access token (create at https://github.com/settings/tokens if needed), then run:

```powershell
git remote add origin https://github.com/AJCodex/daily-linkedin-posts.git
git branch -M main
git push -u origin main
```

---

## What This Does

- Connects local repo to GitHub (`git remote add`)
- Renames branch to `main` (GitHub default)
- Pushes all commits to GitHub (`git push`)

---

## After Push

You'll see:
```
✓ Branch 'main' set up to track 'origin/main'
✓ 20 files pushed to GitHub
```

Then your repo is live at: **https://github.com/AJCodex/daily-linkedin-posts**

---

## GitHub Actions (Optional - Already Prepared)

Once repo is on GitHub, you can optionally enable automated daily runs:
1. Go to repo → **Actions** tab
2. Copy `.github/workflows/daily-posts.yml` template (see DEPLOYMENT_GUIDE.md)
3. Create the workflow file in GitHub
4. Add `OPENROUTER_API_KEY` to repo secrets

---

## Troubleshooting

**"fatal: remote origin already exists"**
```powershell
git remote remove origin
git remote add origin https://github.com/AJCodex/daily-linkedin-posts.git
```

**"Authentication failed"**
- Use personal access token (not password)
- Create token at: https://github.com/settings/tokens/new
- Scopes needed: `repo` (all)

**"Permission denied"**
- Ensure you're logged in as AJCodex user on GitHub
- Check token has `repo` scope

---

**Status:** ✅ Local repo ready to push  
**Next:** Follow 3-step setup above  
**Questions?** Check git log with: `git log --oneline`
