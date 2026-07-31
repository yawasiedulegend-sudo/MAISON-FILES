# Maison Boutique Deployment Guide

## 1. Push to GitHub

1. Create a new GitHub repository.
2. Run:
   ```bash
   git remote add origin https://github.com/<YOUR_USERNAME>/<YOUR_REPO>.git
   git branch -M main
   git push -u origin main
   ```

## 2. Enable GitHub Pages

1. Open the repository on GitHub.
2. Go to Settings > Pages.
3. Choose the main branch.
4. Save and wait for the deployment URL.

## 3. Connect a custom domain

1. In your domain provider, add or update DNS records:
   - For a root domain, create an A record pointing to GitHub Pages IPs.
   - For a subdomain, create a CNAME record to <YOUR_USERNAME>.github.io.
2. In GitHub Pages settings, enter the custom domain and enable HTTPS.

## 4. Host the backend

Use Render, Railway, or Fly.io.

Recommended steps for Render:
1. Create a new Web Service.
2. Connect the GitHub repository.
3. Set the build command to: `pip install -r requirements.txt`
4. Set the start command to: `python backend.py`
5. Deploy.

## 5. Update the live backend URL

Edit [config.js](config.js) and change:

```javascript
window.MAISON_API_BASE_URL = '';
```

to:

```javascript
window.MAISON_API_BASE_URL = 'https://YOUR_BACKEND_URL';
```
