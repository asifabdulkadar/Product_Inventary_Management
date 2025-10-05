<#
Helper script to push this project to GitHub.

Usage (PowerShell):
  1. Open PowerShell at the project root (d:\flask)
  2. Run: .\push_to_github.ps1 -RepoName "Product_Inventary_Management" -Private:$true

This script will:
- initialize a local git repo if none exists
- create a remote GitHub repo using `gh repo create` (if GitHub CLI is installed and authenticated)
- push the local main branch to origin

If `gh` is not available, the script prints the git commands you can run manually.
#>

param(
    [string]$RepoName = "Product_Inventary_Management",
    [bool]$Private = $true,
    [string]$RemoteName = "origin"
)

function Run-Command($cmd) {
    Write-Host "> $cmd"
    iex $cmd
}

if (-not (Test-Path .git)) {
    Write-Host "Initializing git repository..."
    Run-Command "git init"
    Run-Command "git add ."
    Run-Command "git commit -m 'initial commit'"
} else {
    Write-Host "Git repository already exists." -ForegroundColor Yellow
}

$hasGh = (Get-Command gh -ErrorAction SilentlyContinue) -ne $null
if ($hasGh) {
    Write-Host "GitHub CLI detected — creating remote repository using gh..."
    $vis = if ($Private) { "--private" } else { "--public" }
    # Attempt to create the repo and push
    try {
        Run-Command "gh repo create $RepoName $vis --source=. --remote=$RemoteName --push"
        Write-Host "Repository created and pushed. Open it with: gh repo view --web" -ForegroundColor Green
    } catch {
        Write-Host "gh command failed. You can create the repo manually on GitHub and then run the git push commands below." -ForegroundColor Red
    }
} else {
    Write-Host "GitHub CLI (gh) not found. Use these commands to push manually:"
    Write-Host "1) Create a repository on GitHub (https://github.com/new) named: $RepoName"
    Write-Host "2) Run the following commands locally:" -ForegroundColor Cyan
    Write-Host "   git remote add $RemoteName https://github.com/<your-username>/$RepoName.git"
    Write-Host "   git branch -M main"
    Write-Host "   git push -u $RemoteName main"
}

Write-Host "Done." -ForegroundColor Green
