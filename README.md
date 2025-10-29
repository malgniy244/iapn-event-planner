# IAPN Event Planner - Full Stack App

## What's This?
A full-featured event planning app with:
- ✅ Your exact HTML layout with drag-and-drop
- ✅ Backend API that saves data
- ✅ Shows HK time
- ✅ Free hosting on Render.com

## Files in This Package:
- `app.py` - Flask backend API
- `static/index.html` - Your original HTML (modified to use API)
- `requirements.txt` - Python dependencies
- `README.md` - This file

## How to Deploy (FREE on Render.com)

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `iapn-event-planner`
3. Make it **Public**
4. Click "Create repository"

### Step 2: Upload Files to GitHub

**Option A: Via GitHub Website (Easier)**
1. In your new repo, click "uploading an existing file"
2. Drag and drop ALL files from this folder:
   - `app.py`
   - `requirements.txt`
   - `static/` folder (with index.html inside)
3. Commit the files

**Option B: Via Git Command Line**
```bash
cd /path/to/this/folder
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/iapn-event-planner.git
git push -u origin main
```

### Step 3: Deploy on Render.com (FREE)

1. Go to https://render.com/
2. Sign up (use GitHub to login)
3. Click "New" → "Web Service"
4. Click "Connect a repository" → Find your `iapn-event-planner` repo
5. Configure:
   - **Name**: `iapn-planner` (or anything you want)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: `Free`
6. Click "Create Web Service"
7. Wait 3-5 minutes for deployment

### Step 4: Get Your URL

Once deployed, Render gives you a URL like:
```
https://iapn-planner-xxxx.onrender.com
```

**Share this URL with your team!** Everyone can use it together.

## How It Works

- **Frontend**: Your exact HTML with drag-and-drop
- **Backend**: Flask API saves data to `plan_data.json`
- **Data**: All changes auto-save to the server
- **Collaboration**: Everyone sees the same data

## Features

✅ All your IAPN 2027 data preloaded
✅ Drag and drop events between days
✅ Add/edit/delete events
✅ Add/remove days
✅ Auto-save (shows HK time)
✅ Export to CSV/JSON
✅ Currency toggle (HKD/USD)
✅ Works on mobile

## Notes

- **Free tier**: App sleeps after 15 min of no activity
- **First visit after sleep**: Takes 30-60 seconds to wake up
- **After that**: Instant, no delays
- **Upgrade to paid ($7/month)**: No sleep, always instant

## Troubleshooting

**App not loading?**
- Wait 60 seconds on first visit (free tier wakes up)
- Check Render dashboard for errors

**Data not saving?**
- Check browser console for errors (F12)
- Make sure you're using the Render URL, not localhost

**Want to test locally first?**
```bash
pip install -r requirements.txt
python app.py
# Visit http://localhost:5000
```

## Need Help?

Check Render docs: https://render.com/docs/web-services
