# Quick Start - Deploy to Render in 5 Minutes

## 📋 Prerequisites

-   GitHub account
-   Render.com account (free, sign up with GitHub)

## 🚀 Quick Deploy Steps

### Step 1: Push to GitHub (2 minutes)

```bash
# Navigate to project folder
cd "/Users/jameschiu/Downloads/上市公司營收公告"

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - MOPS Revenue Viewer"

# Create a new repository on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Render (3 minutes)

1. Go to **[render.com](https://render.com)** and sign in with GitHub

2. Click **"New +"** → **"Web Service"**

3. Click **"Connect account"** to link your GitHub

4. Find and select your repository

5. Render will auto-detect settings from `render.yaml`:

    - ✅ Name: `mops-revenue-viewer`
    - ✅ Build Command: `pip install -r requirements.txt`
    - ✅ Start Command: `gunicorn app:app`

6. Select **"Free"** plan

7. Click **"Create Web Service"**

8. Wait 2-3 minutes for deployment

9. Done! Your app will be live at: `https://YOUR-APP-NAME.onrender.com`

## 🎉 That's It!

Your MOPS Revenue Viewer is now live on the internet!

## 📝 Important Notes

### CSV Files Storage

-   CSV files are stored in `/data/` folder
-   ⚠️ Files are **temporary** - deleted when server restarts
-   Free tier servers sleep after 15 min inactivity
-   Perfect for on-demand queries

### Free Tier Info

-   ✅ 750 hours/month (plenty for personal use)
-   ⚠️ Server sleeps after 15 min idle
-   ⚠️ First request after sleep: 30-60 sec wake time
-   ⚠️ Files don't persist across restarts

### Update Your App

```bash
# Make changes
git add .
git commit -m "Update description"
git push
# Render auto-deploys!
```

## 🆘 Troubleshooting

**Build failed?**

-   Check Render logs
-   Verify all files are committed: `git status`

**App not loading?**

-   Check Render dashboard logs
-   Wait 60 seconds if server was sleeping

**Need persistent storage?**

-   Upgrade to Render paid plan ($7/month)
-   Or use external storage (Google Drive, S3)

## 📚 Full Documentation

See `DEPLOY.md` for detailed instructions and troubleshooting.
