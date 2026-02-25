# IAPN Event Planner

A full-stack event planning app with drag-and-drop scheduling, revenue calculation, persistent database storage, and password protection.

## Features

- 🔐 Password-protected (password: `iapn2026`)
- 🗂 Drag events from the library onto any day
- 💰 Auto-calculates cost per day and total (HKD/USD)
- 💾 Auto-saves every change to PostgreSQL database
- ✏️ Edit day labels and notes inline
- ➕ Add/remove days dynamically
- 📱 Works on mobile

## Deploy on Render.com (Free)

### Step 1 — Create a GitHub Repository

1. Go to https://github.com/new
2. Name it `iapn-event-planner` (or anything you like)
3. Make it **Public**
4. Click **Create repository**
5. Upload all files from this folder

### Step 2 — Deploy on Render.com

1. Go to https://render.com and sign in with GitHub
2. Click **New +** → **Web Service**
3. Connect your `iapn-event-planner` repository
4. Configure:
   - **Name**: `iapn-planner`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: `Free`
5. Add **Environment Variables**:
   - `APP_PASSWORD` = `iapn2026`
   - `SECRET_KEY` = (any random string, e.g. `my-secret-key-2027`)
6. Click **Create Web Service**

### Step 3 — Add a PostgreSQL Database on Render

1. Click **New +** → **PostgreSQL**
2. Name it `iapn-db`
3. Plan: **Free**
4. Click **Create Database**
5. Copy the **Internal Database URL**
6. Go back to your web service → **Environment** → Add:
   - `DATABASE_URL` = (paste the Internal Database URL)
7. Click **Save Changes** — the service will redeploy

### Step 4 — Point planner.numisops.com to Render

1. In Render, go to your web service → **Settings** → **Custom Domains**
2. Add `planner.numisops.com`
3. Render will show you a CNAME value (e.g. `iapn-planner.onrender.com`)
4. In Cloudflare DNS, add:
   - Type: `CNAME`
   - Name: `planner`
   - Target: (the value Render gives you)
   - Proxy: **DNS only** (grey cloud)

Your app will be live at https://planner.numisops.com

## Notes

- **Free tier**: App sleeps after 15 min of inactivity. First visit after sleep takes ~30 seconds.
- **Data**: Stored in PostgreSQL — survives restarts and sleeps.
- **Upgrade to $7/month**: No sleep, always instant.
