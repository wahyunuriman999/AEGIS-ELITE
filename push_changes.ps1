# PowerShell script to initialize git, commit, and push changes
# Usage: .\push_changes.ps1 -RemoteUrl 'https://github.com/owner/repo.git' -Branch 'main'
param(
  [Parameter(Mandatory=$true)]
  [string]$RemoteUrl,
  [string]$Branch = 'main'
)

if (-not (Test-Path .git)) {
  git init
  git add .
  git commit -m "CI: add Docker build/push, API hardening, tests, migrations, studio proxy"
  git branch -M $Branch
  git remote add origin $RemoteUrl
} else {
  git add .
  git commit -m "CI: add Docker build/push, API hardening, tests, migrations, studio proxy" || Write-Output "No changes to commit"
}

Write-Output "Pushing to $RemoteUrl ($Branch)..."
git push -u origin $Branch
