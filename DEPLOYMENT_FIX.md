# Deployment Fix - Action Required

## Problem Identified

✅ Local code: Has all updates (64,112 bytes)
✅ GitHub repo: Has all updates (64,112 bytes)
❌ Live Cloudflare site: OLD version (51,076 bytes) - **missing 13KB of new content**

**Root cause:** Cloudflare Pages webhook is not triggering on new commits.

## Solution Implemented

Created GitHub Actions workflow (`.github/workflows/deploy.yml`) to force Cloudflare deployments.

## Setup Required (5 minutes)

### 1. Get Cloudflare API Token

1. Go to https://dash.cloudflare.com/profile/api-tokens
2. Click **"Create Token"**
3. Use template: **"Edit Cloudflare Workers"**
4. Set permissions:
   - Account → Cloudflare Pages → Edit
5. Copy the token

### 2. Get Cloudflare Account ID

1. Go to https://dash.cloudflare.com
2. Click **Workers & Pages**
3. Look in right sidebar for **Account ID** (or URL: `dash.cloudflare.com/{ACCOUNT_ID}/`)
4. Copy the ID

### 3. Add Secrets to GitHub

1. Go to https://github.com/weave0/minnesotapeace/settings/secrets/actions
   - Name: `CLOUDFLARE_API_TOKEN` → Value: [token from step 1]
   - Name: `CLOUDFLARE_ACCOUNT_ID` → Value: [ID from step 2]

### 4. Commit and Push This Workflow

Once you run the commit command below, GitHub Actions will auto-deploy on every push to main.

### 5. Manual Deploy (If Needed)

Go to: https://github.com/weave0/minnesotapeace/actions
Click: **"Deploy to Cloudflare Pages"** → **"Run workflow"**

## Commands to Run

```powershell
cd "Z:\GFD\GFD Dev Projects\jamie-mediation"
git add .github/
git commit -m "ci: add GitHub Actions workflow for Cloudflare Pages deployment"
git push origin main
```

After setup, every push to main will trigger deployment within 2-3 minutes.
