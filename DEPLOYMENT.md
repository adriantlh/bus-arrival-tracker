# Deploy to Render.com

Follow these steps to deploy your Bus Arrival Tracker to Render.com.

## Prerequisites

1. GitHub account
2. LTA API key from https://datamall2.mytransport.sg/
3. Render.com account (free)

## Step 1: Initialize Git Repository

```bash
cd /Users/adrian/Projects/bus\ stop\ application
git init
git add .
git commit -m "Initial commit: Bus Arrival Tracker"
git branch -M main
```

## Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Create a new repository (e.g., `bus-arrival-tracker`)
3. Choose Public or Private
4. Don't initialize with README (we already have files)
5. Click "Create repository"

## Step 3: Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/bus-arrival-tracker.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Step 4: Deploy to Render

### Option A: Automatic Deployment (Recommended)

1. Go to https://dashboard.render.com/
2. Click "New +" → "Web Service"
3. Connect your GitHub account if not already connected
4. Find and select your `bus-arrival-tracker` repository
5. Render will detect the Python app automatically
6. Configure:
   - **Name**: `bus-arrival-tracker` (or your preferred name)
   - **Region**: Oregon (free tier) or Singapore (paid)
   - **Branch**: `main`
   - **Runtime**: Python 3.11
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -c gunicorn_config.py bus_arrival:app`
7. **Add Environment Variables**:
   - Click "+ Add Environment Variable"
   - Key: `LTA_API_KEY`
   - Value: `joeiPoPES9ypOHf8zoK3Fg==` (your actual API key)
8. Click "Create Web Service"

### Option B: Using render.yaml (Automatic Config)

If you created the `render.yaml` file, Render will use it automatically:

1. Go to https://dashboard.render.com/
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Render will read `render.yaml` and configure everything
5. You still need to add your `LTA_API_KEY` environment variable

## Step 5: Access Your App

- Render will build and deploy your app (takes 2-3 minutes)
- Once deployed, you'll get a URL like: `https://bus-arrival-tracker.onrender.com`
- Click the URL to view your live app!

## Managing Your Deployment

### View Logs
1. Go to your service in Render dashboard
2. Click "Logs" tab
3. Monitor deployment and runtime logs

### Redeploy
1. Make changes to your code
2. Push to GitHub: `git add . && git commit -m "Update" && git push`
3. Render will automatically detect and redeploy

### Manual Redeploy
1. Go to your service dashboard
2. Click "Manual Deploy" → "Deploy latest commit"

### Add Environment Variables
1. Go to your service dashboard
2. Scroll to "Environment Variables" section
3. Click "+ Add Environment Variable"
4. Add key and value, then click "Save Changes"

## Troubleshooting

### Build Failures
- Check the Logs tab for error messages
- Ensure all dependencies are in `requirements.txt`
- Verify `gunicorn_config.py` is present

### App Won't Start
- Check if port 5000 is exposed correctly
- Verify environment variables are set
- Check the "Logs" tab for Python errors

### API Errors
- Verify `LTA_API_KEY` is correct in environment variables
- Check if LTA API is accessible from Render's network

### Free Tier Limitations
- Render free tier spins down after 15 minutes of inactivity
- First request after spin-down may take 30-60 seconds
- Consider upgrading to paid tier for always-on service

## Updating Your App

1. Make changes locally
2. Commit and push:
```bash
git add .
git commit -m "Your commit message"
git push
```
3. Render automatically redeploy

## Useful Links

- Render Dashboard: https://dashboard.render.com/
- Your Service: https://dashboard.render.com/web/bus-arrival-tracker
- Render Docs: https://render.com/docs

## Custom Domain (Optional)

1. Go to your service dashboard
2. Scroll to "Custom Domains"
3. Click "Add Custom Domain"
4. Enter your domain (e.g., `buses.yourdomain.com`)
5. Update your DNS records as instructed by Render

## Monitoring

- View metrics in Render dashboard
- Monitor response times
- Check error rates
- Set up alerts for downtime

Congratulations! Your Bus Arrival Tracker is now live on Render.com! 🚌
