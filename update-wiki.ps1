# ========================================
# EPIC Wiki Update Script (PowerShell)
# Automatically stages, commits, and pushes wiki updates to GitHub
# ========================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  EPIC Wiki Update to GitHub" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Change to the script directory
Set-Location $PSScriptRoot

# Check if git is available
try {
    $null = git --version
} catch {
    Write-Host "ERROR: Git is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Git from https://git-scm.com/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if this is a git repository
try {
    $null = git rev-parse --git-dir 2>$null
} catch {
    Write-Host "ERROR: This is not a git repository" -ForegroundColor Red
    Write-Host ""
    $initChoice = Read-Host "Would you like to initialize git and set up the remote? (Y/N)"
    if ($initChoice -eq "Y" -or $initChoice -eq "y") {
        Write-Host ""
        Write-Host "Initializing git repository..." -ForegroundColor Yellow
        git init
        Write-Host ""
        Write-Host "Setting up remote repository..." -ForegroundColor Yellow
        git remote add origin https://github.com/WhaleCancer/ChooseYourOwnAdventure.git
        Write-Host ""
        Write-Host "Git repository initialized!" -ForegroundColor Green
        Write-Host "You can now run this script again to commit and push."
        Read-Host "Press Enter to exit"
        exit 0
    } else {
        Write-Host "Exiting..."
        exit 1
    }
}

# Show current status
Write-Host "Checking for changes..." -ForegroundColor Yellow
Write-Host ""
git status --short

# Check if there are changes
$hasChanges = $false
$status = git status --porcelain
if ($status) {
    $hasChanges = $true
}

if (-not $hasChanges) {
    Write-Host ""
    Write-Host "Everything is up to date! No changes to commit." -ForegroundColor Green
    Read-Host "Press Enter to exit"
    exit 0
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Staging all changes..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

git add .
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to stage files" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Files staged successfully!" -ForegroundColor Green
Write-Host ""

# Show what will be committed
Write-Host "Files to be committed:"
git status --short
Write-Host ""

# Prompt for commit message
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Commit Message" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Enter your commit message (or press Enter for default):"
Write-Host "Default: 'Update wiki content'" -ForegroundColor Gray

$commitMsg = Read-Host

if ([string]::IsNullOrWhiteSpace($commitMsg)) {
    $commitMsg = "Update wiki content"
}

Write-Host ""
Write-Host "Committing with message: '$commitMsg'" -ForegroundColor Yellow
Write-Host ""

git commit -m $commitMsg
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to create commit" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Commit created successfully!" -ForegroundColor Green
Write-Host ""

# Check if remote is set
try {
    $null = git remote get-url origin 2>$null
} catch {
    Write-Host "WARNING: No remote repository configured." -ForegroundColor Yellow
    Write-Host ""
    $addRemote = Read-Host "Would you like to add the remote now? (Y/N)"
    if ($addRemote -eq "Y" -or $addRemote -eq "y") {
        git remote add origin https://github.com/WhaleCancer/ChooseYourOwnAdventure.git
        Write-Host "Remote added!" -ForegroundColor Green
    } else {
        Write-Host "Skipping push. Run this script again after setting up the remote."
        Read-Host "Press Enter to exit"
        exit 0
    }
}

# Push to GitHub
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Pushing to GitHub..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Ensure we're on main branch
$currentBranch = git branch --show-current
if ($currentBranch -ne "main" -and $currentBranch -ne "master") {
    Write-Host "Renaming branch to 'main'..." -ForegroundColor Yellow
    git branch -M main
} elseif ($currentBranch -eq "master") {
    Write-Host "Renaming 'master' to 'main'..." -ForegroundColor Yellow
    git branch -M main
}

git push -u origin main
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Failed to push to GitHub" -ForegroundColor Red
    Write-Host ""
    Write-Host "Possible reasons:" -ForegroundColor Yellow
    Write-Host "  - Authentication required (GitHub username/password or token)"
    Write-Host "  - Network connection issue"
    Write-Host "  - Remote repository doesn't exist yet"
    Write-Host ""
    Write-Host "If this is your first push, make sure:" -ForegroundColor Yellow
    Write-Host "  1. The repository exists at: https://github.com/WhaleCancer/ChooseYourOwnAdventure"
    Write-Host "  2. You have write access to the repository"
    Write-Host "  3. You've set up authentication (username/password or Personal Access Token)"
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Success!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your wiki has been updated on GitHub!" -ForegroundColor Green
Write-Host "View it at: https://github.com/WhaleCancer/ChooseYourOwnAdventure" -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter to exit"

