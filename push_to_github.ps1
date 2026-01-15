# Push to GitHub Script
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "   PUSH TO GITHUB - Interactive Script" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Get GitHub username
$username = Read-Host "Enter your GitHub username"

# Repository name
$reponame = "flipkart-recommendation-system"

Write-Host ""
Write-Host "Repository will be: https://github.com/$username/$reponame" -ForegroundColor Yellow
Write-Host ""

# Check if repository exists on GitHub
Write-Host "IMPORTANT: Make sure you have created this repository on GitHub first!" -ForegroundColor Red
Write-Host "Go to: https://github.com/new" -ForegroundColor Yellow
Write-Host ""
Write-Host "Repository settings:" -ForegroundColor Green
Write-Host "  - Name: $reponame" -ForegroundColor White
Write-Host "  - Description: ML-based product recommendation system" -ForegroundColor White
Write-Host "  - Public or Private: Your choice" -ForegroundColor White
Write-Host "  - DO NOT initialize with README" -ForegroundColor White
Write-Host ""

$continue = Read-Host "Have you created the repository on GitHub? (yes/no)"

if ($continue -ne "yes") {
    Write-Host ""
    Write-Host "Please create the repository first, then run this script again." -ForegroundColor Yellow
    Write-Host "Opening GitHub in browser..." -ForegroundColor Cyan
    Start-Process "https://github.com/new"
    exit
}

Write-Host ""
Write-Host "Removing old remote..." -ForegroundColor Cyan
git remote remove origin 2>$null

Write-Host "Adding new remote..." -ForegroundColor Cyan
git remote add origin "https://github.com/$username/$reponame.git"

Write-Host "Setting branch to main..." -ForegroundColor Cyan
git branch -M main

Write-Host ""
Write-Host "Pushing to GitHub..." -ForegroundColor Cyan
Write-Host "You may be asked for credentials:" -ForegroundColor Yellow
Write-Host "  - Username: Your GitHub username" -ForegroundColor White
Write-Host "  - Password: Use Personal Access Token (NOT your password)" -ForegroundColor White
Write-Host ""

git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host "   SUCCESS! Your project is now on GitHub!" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "View your repository at:" -ForegroundColor Cyan
    Write-Host "https://github.com/$username/$reponame" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Opening in browser..." -ForegroundColor Cyan
    Start-Process "https://github.com/$username/$reponame"
} else {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Red
    Write-Host "   PUSH FAILED" -ForegroundColor Red
    Write-Host "============================================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "1. Repository doesn't exist on GitHub" -ForegroundColor White
    Write-Host "2. Wrong username" -ForegroundColor White
    Write-Host "3. Authentication failed - use Personal Access Token" -ForegroundColor White
    Write-Host ""
    Write-Host "Get Personal Access Token at:" -ForegroundColor Cyan
    Write-Host "https://github.com/settings/tokens" -ForegroundColor Yellow
}

Write-Host ""
Read-Host "Press Enter to exit"