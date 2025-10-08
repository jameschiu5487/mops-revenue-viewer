# Deploy to Render.com

## Step-by-Step Deployment Guide

### 1. Prepare Your GitHub Repository

1. Create a new repository on GitHub (e.g., `mops-revenue-viewer`)

2. Initialize git in your project folder:

```bash
cd "/Users/jameschiu/Downloads/上市公司營收公告"
git init
git add .
git commit -m "Initial commit"
```

3. Connect to GitHub and push:

```bash
git remote add origin https://github.com/YOUR_USERNAME/mops-revenue-viewer.git
git branch -M main
git push -u origin main
```

### 2. Deploy on Render.com

1. Go to [https://render.com](https://render.com)

2. Sign up or log in (you can use your GitHub account)

3. Click **"New +"** → **"Web Service"**

4. Connect your GitHub repository:

    - Click **"Connect account"** to link GitHub
    - Select your repository: `mops-revenue-viewer`

5. Configure the service:

    - **Name**: `mops-revenue-viewer` (or any name you like)
    - **Region**: Choose closest to you (e.g., Singapore)
    - **Branch**: `main`
    - **Runtime**: `Python 3`
    - **Build Command**: `pip install -r requirements.txt`
    - **Start Command**: `gunicorn app:app`

6. Select the **Free** plan

7. Click **"Create Web Service"**

### 3. Wait for Deployment

-   Render will automatically build and deploy your app
-   This usually takes 2-5 minutes
-   You'll see the build logs in real-time

### 4. Access Your App

Once deployed, you'll get a URL like:

```
https://mops-revenue-viewer.onrender.com
```

## Important Notes

### About CSV Files

-   CSV files will be stored in the `data/` folder on the server
-   ⚠️ **Files are temporary**: They will be deleted when the server restarts
-   Free tier servers sleep after 15 minutes of inactivity
-   When the server wakes up, all CSV files will be gone

### Free Tier Limitations

-   Server sleeps after 15 minutes of inactivity
-   First request after sleep takes 30-60 seconds to wake up
-   750 hours/month of runtime (enough for most personal use)
-   Files are ephemeral (not persistent)

### Automatic Deployments

-   Every time you push to GitHub, Render will automatically redeploy
-   You can disable this in the Render dashboard if needed

## Troubleshooting

### Build Failed

Check that all files are committed:

```bash
git status
git add .
git commit -m "Fix build issues"
git push
```

### App Not Loading

1. Check the logs in Render dashboard
2. Make sure `gunicorn` is in `requirements.txt`
3. Verify `app.py` has the correct configuration

### CORS Issues

If you get CORS errors, add this to `app.py`:

```python
from flask_cors import CORS
CORS(app)
```

And add to `requirements.txt`:

```
flask-cors==4.0.0
```

## Updating Your App

To update your deployed app:

```bash
# Make your changes
git add .
git commit -m "Description of changes"
git push
```

Render will automatically detect the push and redeploy!

## Alternative: Manual Deploy

If you don't want to use GitHub:

1. On Render dashboard, you can also deploy from a Git URL
2. Or use Render's CLI tool
3. Or connect to GitLab/Bitbucket instead

## Cost

-   **Free tier**: Perfect for personal projects
-   **Paid tier** ($7/month):
    -   No sleep
    -   Persistent disk (for CSV files)
    -   Better performance

## Questions?

Check Render's documentation: https://render.com/docs
