@echo off
echo ============================================================
echo   PUSH TO GITHUB - Quick Upload Script
echo ============================================================
echo.

set /p username="Enter your GitHub username: "
set /p reponame="Enter repository name (default: flipkart-recommendation-system): "

if "%reponame%"=="" set reponame=flipkart-recommendation-system

echo.
echo Repository will be created at:
echo https://github.com/%username%/%reponame%
echo.
echo Please make sure you have created this repository on GitHub first!
echo Go to: https://github.com/new
echo.
pause

echo.
echo Adding remote origin...
git remote add origin https://github.com/%username%/%reponame%.git

echo.
echo Renaming branch to main...
git branch -M main

echo.
echo Pushing to GitHub...
git push -u origin main

echo.
echo ============================================================
echo   DONE! Your project is now on GitHub!
echo   Visit: https://github.com/%username%/%reponame%
echo ============================================================
echo.
pause