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

For the storefront site on GitHub Pages:
1. In your domain provider, add or update DNS records only after the domain is confirmed to be registered and active.
2. For a root domain, create four A records pointing to the GitHub Pages IPs `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, and `185.199.111.153`.
3. For a subdomain such as `www`, create a CNAME record pointing to `<YOUR_USERNAME>.github.io`.
4. In GitHub Pages settings, enter the custom domain only after the DNS change is live.
5. Wait for DNS propagation and then enable HTTPS.

If GitHub shows an invalid DNS error, it usually means one of these is true:
- the DNS record is still propagating,
- the domain was entered incorrectly,
- the CNAME or A record points to the wrong destination,
- the domain has not been fully registered yet.

For the backend API on Render:
1. Add a subdomain such as `api.yourdomain.com` in Render.
2. Create the corresponding DNS record at your provider, usually a CNAME to the Render-generated host or an A record if Render provides one.
3. Wait for propagation and then enable HTTPS.

## 4. Host the backend

Use Render, Railway, or Fly.io.

Recommended steps for Render:
1. Sign in to Render and create a new Web Service.
2. Connect the GitHub repository.
3. Select the repository that contains this project.
4. Set the build command to: `pip install -r requirements.txt`
5. Set the start command to: `python backend.py`
6. Add the environment variable `PORT` with value `10000` if required by the platform.
7. Deploy and copy the generated public URL.

### Render DNS and custom domain
1. In Render, open the service and go to Settings > Custom Domains.
2. Add your custom subdomain such as `api.yourdomain.com`.
3. Render will provide DNS values to add at your domain registrar.
4. After the DNS records propagate, enable the custom domain in Render.

## 5. Update the live backend URL

Edit [config.js](config.js) and change:

```javascript
window.MAISON_API_BASE_URL = '';
```

to:

```javascript
window.MAISON_API_BASE_URL = 'https://YOUR_BACKEND_URL';
```
