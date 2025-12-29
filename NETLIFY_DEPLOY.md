# 🚀 Netlify Deployment Guide

## Prerequisites
✅ Backend deployed on Render (DONE)
✅ Database set up on Supabase (DONE)
- [ ] Netlify account created
- [ ] Your Render backend URL (e.g., `https://career-lab-api.onrender.com`)

---

## Step 1: Deploy to Netlify

### Option A: Deploy via Netlify Dashboard (Recommended)

1. **Go to [netlify.com](https://netlify.com)** and sign in with GitHub

2. **Click "Add new site"** → **"Import an existing project"**

3. **Choose "Deploy with GitHub"**
   - Authorize Netlify to access your GitHub account
   - Select your repository: `aiversehack01`

4. **Configure Build Settings:**
   ```
   Base directory:     frontend
   Build command:      npm run build
   Publish directory:  frontend/.next
   Branch to deploy:   main
   ```

5. **Add Environment Variables** (Click "Show advanced" → "New variable"):
   
   | Variable Name | Value |
   |--------------|-------|
   | `NEXT_PUBLIC_API_URL` | `https://YOUR-BACKEND.onrender.com` |
   | `NEXTAUTH_URL` | Leave blank for now (we'll update after deploy) |
   | `NEXTAUTH_SECRET` | Generate with: `openssl rand -base64 32` |

6. **Click "Deploy site"**
   - Wait 3-5 minutes for the build to complete
   - Netlify will give you a URL like: `https://random-name-123.netlify.app`

---

## Step 2: Update Environment Variables

### 2.1 Update Netlify
1. Go to **Site settings** → **Environment variables**
2. Update `NEXTAUTH_URL` to your actual Netlify URL:
   ```
   https://your-site-name.netlify.app
   ```
3. Click **"Save"**
4. Go to **Deploys** → **Trigger deploy** → **"Deploy site"**

### 2.2 Update Render Backend CORS
1. Go to your **Render Dashboard** → Your backend service
2. Go to **Environment** tab
3. Find `ALLOWED_ORIGINS` and update it to:
   ```
   https://your-site-name.netlify.app,http://localhost:3000
   ```
4. Click **"Save Changes"** (Render will auto-redeploy)

---

## Step 3: Test Your Deployment

1. **Visit your Netlify URL**
2. **Try to sign up/register**
3. **Upload a resume and LinkedIn URL**
4. **Check if data appears in Supabase:**
   - Go to Supabase Dashboard → **Table Editor**
   - Check `users` and `evidence` tables

---

## 🐛 Troubleshooting

### Build fails on Netlify
**Error:** `Module not found` or `npm install failed`
**Fix:** 
- Check that `package.json` is in the `frontend` directory
- Verify `base directory` is set to `frontend`

### Frontend can't connect to backend
**Error:** `Failed to fetch` or CORS errors
**Fix:**
- Verify `NEXT_PUBLIC_API_URL` is set correctly in Netlify
- Check that `ALLOWED_ORIGINS` includes your Netlify URL in Render
- Make sure both URLs use `https://` (not `http://`)

### NextAuth errors
**Error:** `[next-auth][error][SIGNIN_OAUTH_ERROR]`
**Fix:**
- Verify `NEXTAUTH_URL` matches your Netlify URL exactly
- Ensure `NEXTAUTH_SECRET` is set and not empty

---

## 📝 Quick Reference

### Your URLs (fill these in):
```
Frontend:  https://_____________.netlify.app
Backend:   https://_____________.onrender.com
Database:  Supabase Dashboard
```

### Environment Variables Summary

**Netlify (Frontend):**
```env
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
NEXTAUTH_URL=https://your-site.netlify.app
NEXTAUTH_SECRET=<generated-secret>
```

**Render (Backend):**
```env
ALLOWED_ORIGINS=https://your-site.netlify.app,http://localhost:3000
DATABASE_URL=postgresql://postgres.[project]:[password]@aws-0-region.pooler.supabase.com:6543/postgres
GEMINI_API_KEY=<your-key>
GIT_API=<your-github-token>
SECRET_KEY=<generated-secret>
ALGORITHM=HS256
```

---

## ✅ Final Checklist

- [ ] Netlify site deployed successfully
- [ ] Environment variables set on Netlify
- [ ] `NEXTAUTH_URL` updated with actual Netlify URL
- [ ] Netlify redeployed after env var update
- [ ] `ALLOWED_ORIGINS` updated on Render backend
- [ ] Can access frontend at Netlify URL
- [ ] Can sign up/login
- [ ] Can upload resume
- [ ] Data appears in Supabase tables

---

## 🎉 You're Done!

Your full-stack application is now live on:
- **Frontend**: Netlify
- **Backend**: Render
- **Database**: Supabase

All on **100% free tier**! 🚀
