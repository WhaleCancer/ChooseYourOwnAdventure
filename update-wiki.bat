@echo off
setlocal enabledelayedexpansion

REM ========================================
REM EPIC Wiki Update Script
REM Automatically stages, commits, and pushes wiki updates to GitHub
REM ========================================

echo.
echo ========================================
echo   EPIC Wiki Update to GitHub
echo ========================================
echo.

REM Change to the script directory
cd /d "%~dp0"

REM Check if git is available
where git >nul 2>&1
if !errorlevel! neq 0 (
    echo ERROR: Git is not installed or not in PATH
    echo Please install Git from https://git-scm.com/
    echo.
    pause
    exit /b 1
)

REM Check if this is a git repository
git rev-parse --git-dir >nul 2>&1
set git_repo_check=!errorlevel!
if !git_repo_check! neq 0 (
    echo ERROR: This is not a git repository
    echo.
    set /p init_choice="Would you like to initialize git and set up the remote? (Y/N): "
    if /i "!init_choice!"=="Y" (
        echo.
        echo Initializing git repository...
        git init
        if !errorlevel! neq 0 (
            echo ERROR: Failed to initialize git
            pause
            exit /b 1
        )
        echo.
        echo Setting up remote repository...
        git remote add origin https://github.com/WhaleCancer/ChooseYourOwnAdventure.git
        echo.
        echo Git repository initialized!
        echo You can now run this script again to commit and push.
        echo.
        pause
        exit /b 0
    ) else (
        echo Exiting...
        echo.
        pause
        exit /b 1
    )
)

REM Show current status
echo Checking for changes...
echo.
git status --short
echo.

REM Check for any changes (modified, staged, or untracked files)
git diff --quiet 2>nul
set has_modified=!errorlevel!

git diff --cached --quiet 2>nul
set has_staged=!errorlevel!

git ls-files --others --exclude-standard | findstr /R /C:"." >nul 2>&1
set has_untracked=!errorlevel!

if !has_modified! equ 0 if !has_staged! equ 0 if !has_untracked! neq 0 (
    echo Everything is up to date! No changes to commit.
    echo.
    pause
    exit /b 0
)

REM Stage all changes
echo ========================================
echo   Staging all changes...
echo ========================================
REM Add all files, excluding the problematic Con.md file
git add . -- ":!RULES/Skills/LUCK/Con.md" 2>nul

REM Check if files were actually staged
git diff --cached --quiet 2>nul
set has_staged=!errorlevel!
if !has_staged! equ 0 (
    echo ERROR: No files were staged successfully
    pause
    exit /b 1
)

echo Files staged successfully!
echo.

REM Show what will be committed
echo Files to be committed:
git status --short
echo.

REM Prompt for commit message
echo ========================================
echo   Commit Message
echo ========================================
echo Enter your commit message (or press Enter for default):
echo Default: "Update wiki content"
set /p commit_msg=

if "!commit_msg!"=="" (
    set commit_msg=Update wiki content
)

echo.
echo Committing with message: "!commit_msg!"
echo.

git commit -m "!commit_msg!"
if !errorlevel! neq 0 (
    echo ERROR: Failed to create commit
    pause
    exit /b 1
)

echo.
echo Commit created successfully!
echo.

REM Check if remote is set
git remote get-url origin >nul 2>&1
set remote_check=!errorlevel!
if !remote_check! neq 0 (
    echo WARNING: No remote repository configured.
    echo.
    set /p add_remote="Would you like to add the remote now? (Y/N): "
    if /i "!add_remote!"=="Y" (
        git remote add origin https://github.com/WhaleCancer/ChooseYourOwnAdventure.git
        if !errorlevel! neq 0 (
            echo ERROR: Failed to add remote
            pause
            exit /b 1
        )
        echo Remote added!
    ) else (
        echo Skipping push. Run this script again after setting up the remote.
        pause
        exit /b 0
    )
)

REM Push to GitHub
echo ========================================
echo   Pushing to GitHub...
echo ========================================
echo.

REM Ensure we're on main branch
for /f "tokens=*" %%i in ('git branch --show-current') do set current_branch=%%i
if /i not "!current_branch!"=="main" (
    if /i "!current_branch!"=="master" (
        echo Renaming 'master' to 'main'...
        git branch -M main
    ) else (
        echo Current branch is '!current_branch!'. Renaming to 'main'...
        git branch -M main
    )
)

git push -u origin main
if !errorlevel! neq 0 (
    echo.
    echo ERROR: Failed to push to GitHub
    echo.
    echo Possible reasons:
    echo   - Authentication required (GitHub username/password or token)
    echo   - Network connection issue
    echo   - Remote repository doesn't exist yet
    echo.
    echo If this is your first push, make sure:
    echo   1. The repository exists at: https://github.com/WhaleCancer/ChooseYourOwnAdventure
    echo   2. You have write access to the repository
    echo   3. You've set up authentication (username/password or Personal Access Token)
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Success!
echo ========================================
echo.
echo Your wiki has been updated on GitHub!
echo View it at: https://github.com/WhaleCancer/ChooseYourOwnAdventure
echo.
pause
