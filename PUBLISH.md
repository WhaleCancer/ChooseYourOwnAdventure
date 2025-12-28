# Publishing Your EPIC Wiki to GitHub

This guide will walk you through publishing your wiki to GitHub at: https://github.com/WhaleCancer/ChooseYourOwnAdventure

## Prerequisites

- Git is installed and configured
- You have a GitHub account (WhaleCancer)
- The repository exists at the URL above (or you'll create it)

## Step-by-Step Instructions

### Step 1: Stage All Files

First, stage the updated `.gitignore` and all your wiki files:

```powershell
cd "F:\Python Apps\EPIC"
git add .
```

This will add:
- All markdown files (`.md`) - your wiki content
- All images (`.png`) - illustrations
- PDFs - source documents
- JSON files - data files
- Python scripts and PowerShell scripts - development tools
- Everything else except what's in `.gitignore`

### Step 2: Make Your First Commit

```powershell
git commit -m "Initial commit: EPIC X-Files RPG Wiki"
```

Or if you want a more descriptive commit message:

```powershell
git commit -m "Initial commit: Complete EPIC wiki with rules, creatures, factions, locations, vehicles, and scenarios"
```

### Step 3: Connect to GitHub Repository

If the repository doesn't exist yet, create it on GitHub first:
1. Go to https://github.com/new
2. Repository name: `ChooseYourOwnAdventure`
3. Description: "EPIC - X-Files RPG Wiki - A tabletop RPG set in 1985 British Columbia"
4. Choose Public or Private
5. **DO NOT** initialize with README, .gitignore, or license (you already have these)
6. Click "Create repository"

Then connect your local repository:

```powershell
git remote add origin https://github.com/WhaleCancer/ChooseYourOwnAdventure.git
```

If you get an error that the remote already exists, use:
```powershell
git remote set-url origin https://github.com/WhaleCancer/ChooseYourOwnAdventure.git
```

### Step 4: Push to GitHub

Rename your branch to `main` (GitHub's default) and push:

```powershell
git branch -M main
git push -u origin main
```

You'll be prompted for your GitHub username and password (use a Personal Access Token if you have 2FA enabled).

### Step 5: Verify

Visit https://github.com/WhaleCancer/ChooseYourOwnAdventure to see your published wiki!

## Future Updates

When you make changes to your wiki:

```powershell
cd "F:\Python Apps\EPIC"
git add .
git commit -m "Update: [describe your changes]"
git push
```

## Enabling GitHub Pages (Optional)

If you want to view your wiki as a website:

1. Go to your repository on GitHub
2. Click **Settings** → **Pages**
3. Under "Source", select **main** branch and `/ (root)` folder
4. Click **Save**
5. Your wiki will be available at: `https://whalecancer.github.io/ChooseYourOwnAdventure/`

Note: Markdown files will render automatically on GitHub, so you might not need Pages unless you want a custom website.

## Troubleshooting

### Large File Warnings
If you get warnings about large files (>100MB):
- GitHub allows files up to 100MB
- Files between 50-100MB will generate warnings
- Consider using Git LFS for very large PDFs if needed

### Authentication Issues
If push fails due to authentication:
- Use a Personal Access Token instead of password
- Create one at: https://github.com/settings/tokens
- Select `repo` scope
- Use the token as your password when prompted

### Merge Conflicts
If you see merge conflicts:
```powershell
git pull origin main --rebase
# Fix any conflicts, then:
git push
```

## What Gets Published?

✅ **Included:**
- All `.md` files (wiki pages)
- All `.png`, `.jpg` images
- All `.pdf` files
- All `.json` data files
- All `.py` and `.ps1` scripts
- All `.txt` files

❌ **Excluded (via .gitignore):**
- `__pycache__/` - Python cache
- `venv/`, `env/` - Virtual environments
- `.vscode/`, `.idea/` - IDE settings
- `*.tmp`, `*.bak`, `*.log` - Temporary files
- `.DS_Store`, `Thumbs.db` - OS files

## Next Steps After Publishing

1. **Add repository description and topics** on GitHub for discoverability
2. **Create a `CONTRIBUTING.md`** if others will contribute
3. **Set up GitHub Actions** for automated checks (optional)
4. **Enable Discussions** for wiki-related questions
5. **Create Issues** for tracking improvements and bugs

---

Happy publishing! 🚀

