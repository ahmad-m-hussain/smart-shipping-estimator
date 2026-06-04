Write-Host "===== Git Auto Push Script ====="

# Ask for source folder
$source = Read-Host "Enter the SOURCE folder path"

# Check folder exists
if (!(Test-Path $source)) {
    Write-Host "Folder not found !!"
    exit
}

# Ask for repo URL
$repo = Read-Host "Enter the GIT repository URL"

# Ask for branch
$branch = Read-Host "Enter branch name (default: main)"
if ($branch -eq "") { $branch = "main" }

# Go to folder
Set-Location $source

# Initialize git if needed
if (!(Test-Path ".git")) {
    Write-Host "Initializing git repository..."
    git init
}

# Configure remote
git remote remove origin 2>$null
git remote add origin $repo

# Add files
Write-Host "Adding files..."
git add .

# Commit message
$message = Read-Host "Enter commit message"
if ($message -eq "") { $message = "Auto commit" }

git commit -m "$message"

# Push
Write-Host "Pushing to repository..."
git branch -M $branch
git push -u origin $branch

Write-Host "Done! Files pushed successfully..."